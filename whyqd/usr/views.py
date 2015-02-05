from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib.auth import logout

import json

from whyqd.usr.forms import SubscribeForm
from whyqd.snippets.diff2merge import xtractemail

def logout(request, next_page="/"):
    logout(request)

@login_required
def usr_update(request):
    """
    Update the details for this user.
    """
    if request.method == "POST":
        if request.is_ajax():
            usr_response = {'response': 'failure'}
            data = request.POST
            # Process and test emails
            usr_email = xtractemail(data["email"])[0]
            usr_name = data["name"]
            if usr_email and usr_name:
                request.user.email = usr_email
                request.user.facebook_name = usr_name
                request.user.optout = False
                if data["optout"] == "true":
                    request.user.optout = True
                request.user.save()
            usr_response = {'response': 'success'}
            return HttpResponse(json.dumps(usr_response), content_type="application/json")
    raise Http404 


def register(request, template_name="usr/register.html"):
    """ view displaying customer registration form """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = RegistrationForm(postdata)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)  # new
            user.email = postdata.get('email','')  # new
            user.save()  # new
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    page_title = 'User Registration'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def my_account(request, template_name="registration/my_account.html"):
    page_title = 'My Account'
    name = request.user.username
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def subscribe(request, template_name="usr/subscribe.html"):
    """
   
    """
    page_title = "User Subscription"
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            request.user.profile.is_subscribed_to = form.cleaned_data['subscribe_to']
            request.user.profile.save()
            return redirect("view_wiqi_list", wiqi_type="content")
    else:
        form = SubscribeForm()
    return render(request, template_name, locals())