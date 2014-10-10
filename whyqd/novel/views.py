from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.forms.models import modelformset_factory
from django.conf import settings

import stripe
import json
from decimal import Decimal
from guardian.shortcuts import get_objects_for_user

from whyqd.novel.models import Novel, Token
from whyqd.novel.forms import NovelForm, TokenForm, BulkBuyForm
from whyqd.wiqi.models import Wiqi
from whyqd.wiqi.forms import WiqiPriceForm
from whyqd.wiqi import wiqi as wiqid
from whyqd.snippets.diff2merge import docxtract, xtractemail

def view_novel(request, surl, template_name="novel/view_novel.html"):
    novel_object = get_object_or_404(Novel, surl=surl)
    page_title = novel_object.title
    return render(request, template_name, locals())

def buy_novel(request, surl=None, template_name="novel/buy_novel.html"):
    if surl:
        novel_object = get_object_or_404(Novel, surl=surl)
    else:
        novel_object = get_list_or_404(Novel)[0]
    page_title = novel_object.title
    stripe_key = settings.TEST_PUBLISHABLE_KEY
    if request.method == "POST":
        # Set your secret key: remember to change this to your live secret key in production
        stripe.api_key = settings.TEST_SECRET_KEY
        # Get the credit card details submitted by the form or via ajax
        data = request.POST
        # Process and test emails
        stripe_emails = xtractemail(data["stripeEmails"])
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=data["stripePrice"], # amount in pence
                currency="gbp",
                card=data["stripeToken"],
                description=data["stripeDescription"],
                statement_description=novel_object.title,
              )   
        except stripe.CardError, e:
          # The card has been declined
          pass
        # Create a Token and associate this charge with it for each email recipient
        kwargs = {}
        kwargs["creator_ip"] = wiqid.get_user_ip(request)
        kwargs["novel"] = novel_object
        kwargs["charge"] = charge
        kwargs["is_purchased"] = True
        if request.user.is_authenticated():
            kwargs["creator"] = request.user
        else:
            kwargs["creator"] = None
        for e in stripe_emails:
            kwargs["recipient"] = e
            kwargs["price"] = Decimal(float(data["stripePrice"])/len(stripe_emails)/100)
            token_object = Token()
            token_object.issue(**kwargs)
    if request.is_ajax():
        HttpResponse(json.dumps({}), content_type="application/json")
    return render(request, template_name, locals())

def novel_settings(request):
    if request.is_ajax():
        novel_object = get_list_or_404(Novel)[0]
        if request.user.can_read(novel_object) == "owns":
            response_dict = {'settings': {
                'stripe_key': settings.TEST_PUBLISHABLE_KEY,
                'bulk_discount': settings.BULK_DISCOUNT,
                'bulk_volume': settings.BULK_VOLUME,
                'bulk_price': str(novel_object.sentinal.price),
                'novel_title': novel_object.title,
                'user_email': request.user.email,
                }
            }
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
    return Http404

@login_required
def resend_novel(request, surl, template_name="novel/issue_tokens.html"):
    novel_object = get_object_or_404(Novel, surl=surl)
    page_title = novel_object.title
    return render(request, template_name, locals())

@login_required
def issue_tokens(request, surl, template_name="novel/issue_tokens.html"):
    """
    Issue and manage a list of tokens to users identified by book owner:
        - Lend up to TOKEN_LIMIT copies of novel;
        - Bulk-buy an unlimited amount, unlocking BULK_DISCOUNT at specified BULK_VOLUME;
        - Resend, reallocate and rename valid tokens;
        - Refund valid and purchased tokens;
    """
    novel_object = get_object_or_404(Novel, surl=surl)
    if not request.user.can_read(novel_object) == "owns":
        return Http404
    page_title = novel_object.title
    token_list = Token.query.issued_list(request.user)
    tokens_remaining = settings.TOKEN_LIMIT - len(token_list)
    total_duration = settings.TOKEN_DELTA
    total_tokens = settings.TOKEN_LIMIT
    stripe_key = settings.TEST_PUBLISHABLE_KEY
    bulk_discount = settings.BULK_DISCOUNT
    bulk_volume = settings.BULK_VOLUME
    bulk_price = settings.BULK_PRICE
    TokenFormSet = modelformset_factory(Token, form=TokenForm, extra=tokens_remaining)
    if request.method == "POST":
        # http://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
        if "stripeToken" in request.POST:
            formset = TokenFormSet(queryset=token_list.all())
            #if request.is_ajax():
            #    return HttpResponse(json.dumps({'token': token_object.surl}), content_type="application/json")
        elif "issue_tokens" in request.POST:
            formset = TokenFormSet(request.POST, queryset=token_list.all())
            if formset.is_valid():
                kwargs = {}
                kwargs["creator"] = request.user
                kwargs["creator_ip"] = wiqid.get_user_ip(request)
                kwargs["novel"] = novel_object                
                for form in formset.cleaned_data:
                    if form:
                        if not form['id']:
                            kwargs['recipient'] = form['recipient']
                            token_object = Token()
                            token_object.issue(**kwargs)
                            tokens_remaining -= 1
                        elif form['id'].is_valid and form['id'].recipient != form['recipient']:
                            form['id'].recipient = form['recipient']
                            form['id'].save()
                #if request.is_ajax():
                #    return HttpResponse(json.dumps({'token': token_object.surl}), content_type="application/json")
    else:
        formset = TokenFormSet(queryset=token_list.all())
    return render(request, template_name, locals())

def redeem_token(request, surl, template_name="novel/redeem_token.html"):
    token_object = get_object_or_404(Token, surl=surl)
    if not token_object.is_purchased:
        days = settings.TOKEN_DELTA
    if request.user.is_authenticated():
        if token_object.is_valid:
            kwargs = request.POST.dict()
            kwargs["redeemer"] = request.user
            kwargs["redeemer_ip"] = wiqid.get_user_ip(request)
            token_object.redeem(**kwargs)
        page_message = request.user.can_read_terms(token_object.novel)
    page_title = token_object.novel.title
    return render(request, template_name, locals())

@login_required
def create_novel(request, template_name="novel/create_novel.html"):
    """
    Create the novel but does not yet populate the chapters.
    """
    if not request.user.is_superuser:
        return Http404
    if request.method == "POST":
        novel_form = NovelForm(request.POST)
        if novel_form.is_valid():
            kwargs = request.POST.dict()
            kwargs["creator"] = request.user
            kwargs["creator_ip"] = wiqid.get_user_ip(request)
            novel_object = Novel()
            novel_object.set(**kwargs)
            novel_object.assign_all_perm(request.user)
            if request.is_ajax():
                return HttpResponse(json.dumps({'novel': novel_object.surl}), content_type="application/json")
    else:
        novel_form = NovelForm()
    return render(request, template_name, locals())

@login_required
def upload_docx(request, template_name="novel/create_novel.html"):
    """
    Receive a file and return the components necessary for the user to organise and save it.
    """
    if not request.user.is_superuser:
        return Http404
    usr_ip = wiqid.get_user_ip(request)
    if request.is_ajax():
        # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
        kwargs = request.POST.dict()
        kwargs["file"] = request.FILES.get("file", "")
        tree = docxtract(kwargs["file"])
        return HttpResponse(json.dumps(tree), content_type="application/json")
    return render(request, template_name, locals())

# Next too https://docs.djangoproject.com/en/dev/topics/auth/default/#the-permission-required-decorator
@login_required
def organise_novel(request, surl, template_name="novel/create_novel.html", permission="can_edit"):
    """
    By default, permits the review of the Book wiqi, reorganising of chapter order,
    rights management and that sort of thing. With time, perhaps, this can be
    extended to the other wiqis...
    """
    if not request.user.is_superuser:
        return Http404
    novel_object = get_object_or_404(Novel, surl=surl)
    if not request.user.has_perm(permission, novel_object):
        raise Http404
    if request.method == "POST":
        if request.is_ajax():
            kwargs = json.loads(request.body)
            kwargs["common"] = {"creator": request.user,
                                "creator_ip": wiqid.get_user_ip(request),
                                "WiqiStack": wiqid.get_wiqi_or_404('text')
                                }
            novel_object = novel_object.add_chapters(**kwargs)
            return HttpResponse(json.dumps(novel_object.jsonresponse), content_type="application/json")
    return render(request, template_name, locals())

@login_required
def price_novel(request, surl, template_name="novel/price_novel.html", permission="can_edit"):
    """
    Set the price and view permissions required for each chapter.
    """
    if not request.user.is_superuser:
        return Http404
    novel_object = get_object_or_404(Novel, surl=surl)
    if not request.user.has_perm(permission, novel_object):
        raise Http404
    # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#model-formsets
    WiqiPriceFormSet = modelformset_factory(Wiqi, form=WiqiPriceForm, extra=0)
    if request.method == "POST":
        formset = WiqiPriceFormSet(request.POST, queryset=novel_object.chapterlist.all())
        if formset.is_valid():
            formset.save()
            return redirect(novel_object)
    else:
        formset = WiqiPriceFormSet(queryset=novel_object.chapterlist.all())
    return render(request, template_name, locals())

@login_required
def administer_novel(request, template_name="novel/administer_novel.html", permission="can_edit"):
    """
    Present a list of novels and permit actions.
    """
    if not request.user.is_superuser:
        return Http404
    novel_objects = get_objects_for_user(request.user, permission, klass=Novel)
    return render(request, template_name, locals())