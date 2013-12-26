from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

from datetime import datetime
import pytz
import json
from bs4 import BeautifulSoup
from guardian.shortcuts import assign, get_objects_for_user, get_perms

from whyqd.wiqi.models import Wiqi, DEFAULT_WIQISTACK_TYPE
from whyqd.wiqi.forms import WiqiForm, WiqiStackRangeForm, WiqiStackRevertForm
from whyqd.wiqi import wiqi as wiqid
from whyqd.snippets.shrtn import surl, lurs
from whyqd.snippets.diff2merge import mergediff

def view_wiqi_list(request, template_name="wiqi/list.html", nav_type="view"):
    ''' Temporary to see what we've got, covered by search later'''
    wiqi_list = get_list_or_404(Wiqi.wiqi_objects.all().published())
    page_title = "list"
    nav_set = None
    return render(request, template_name, locals())

def view_wiqi(request, wiqi_surl, wiqi_type=None, template_name="view.html", nav_type="view", permission="can_view"):
    """
    Doubles as the wiqistack list, and wiqistack view as well.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission, wiqi_type)
    #print "View: Wiqi ", wiqi_object, " -> Stack ", wiqi_object.stack, " -> Wiqi ",wiqi_object.stack.wiqi, " -> Stack ", wiqi_object.stack.wiqi.stack, " -> Wiqi ", wiqi_object.stack.wiqi.stack.wiqi
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    try:
        page_title = wiqi_object.stack.title
        wiqi_links = wiqi_object.stack
    except AttributeError:
        # It's from a wiqistack
        page_title = wiqi_object.title
        wiqi_links = wiqi_object
        nav_title = "stack"
    if nav_type == "stack":
        if request.method == "POST":
            range_form = WiqiStackRangeForm(request.POST)
            if range_form.is_valid():
                range_from = range_form.cleaned_data['range_from']
                range_to = range_form.cleaned_data['range_to']
                wiqi_stack = wiqi_object.stacklist.range(range_from=range_from, range_to=range_to)
        else:
            range_form = WiqiStackRangeForm()
            wiqi_stack = wiqi_object.stacklist
    if request.is_ajax():
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return render(request, template_name, locals())
    
@login_required
def edit_wiqi(request, wiqi_type=None, wiqi_surl=None, linked_wiqi_surl=None,
              template_name="edit.html", nav_type="edit", permission="can_edit"):
    """
    Edits existing or creates new wiqistack object.
    Performs fork from any wiqistack item.
    linked_wiqi_object offers a single wiqi link (e.g. an associated image)
    """
    linked_wiqi_object = None
    if linked_wiqi_surl is not None and linked_wiqi_surl != "None":
        linked_wiqi_object = wiqid.get_wiqi_object_or_404(lurs(linked_wiqi_surl), 
                                                          request.user, permission)
        linked_wiqistack_object = linked_wiqi_object.stack
    if nav_type == "create":
        if wiqi_type is None:
            wiqi_type = DEFAULT_WIQISTACK_TYPE
        wiqi_object = Wiqi()
        wiqistack_object = None
        page_title = None
    else:
        # Get the wiqi object to be edited or forked
        wiqistack_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission, wiqi_type)
        wiqi_object = wiqistack_object.wiqi
        wiqi_type = wiqi_object.get_class
        page_title = wiqistack_object.title
    usr_ip = wiqid.get_user_ip(request)
    now = pytz.UTC.localize(datetime.now())
    #nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    if request.is_ajax():
        # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
        kwargs = request.POST.dict()
        kwargs["title"] = BeautifulSoup(kwargs.get("title", "")[:250]).get_text().strip()
        kwargs["subtitle"] = BeautifulSoup(kwargs.get("subtitle","")).get_text().strip()
        kwargs["content"] = mergediff(kwargs.get("content", ""))
        kwargs["file"] = request.FILES.get("file", "")
        kwargs["creator"] = request.user
        kwargs["creator_ip"] = wiqid.get_user_ip(request)
        kwargs["linked_wiqi_object"] = linked_wiqi_object
        if nav_type == "create":
            kwargs["WiqiStack"] = wiqid.get_wiqi_or_404(wiqi_type)
        if nav_type == "fork":
            # get the new wiqi item as the new reference
            wiqi_object = wiqistack_object.fork(**kwargs)
            wiqistack_object = wiqi_object.stack
        elif nav_type != "create":
            # Test whether wiqistack_object is at the top of the stack
            if not wiqistack_object.is_top_of_stack:
                print "###################################"
                print wiqi_type, wiqi_object, wiqistack_object
                wiqistack_object.revert(**kwargs)
        else:
            # We're creating...
            wiqi_object.set(**kwargs)
        # Capture the wiqi after any changes made
        kwargs["wiqi"] = wiqi_object
        wiqi_object.update(**kwargs)
        # if wiqi_object is default, then ignore this step
        if wiqi_type != DEFAULT_WIQISTACK_TYPE and linked_wiqi_object is not None:
            kwargs["linked_wiqi_object"] = wiqi_object
            kwargs["wiqi"] = linked_wiqi_object
            linked_wiqi_object.update(**kwargs)
        nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        nav_set.update(json.loads(wiqi_object.jsonresponse))
        nav_set["view"] = wiqi_object.get_url()
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    # This is for a standard call to the non-ajax editing form
    WiqiStackForm = wiqid.get_wiqi_form(wiqi_type)
    #template_name="wiqi/edit.html"
    if request.method == "POST":
        wiqi_form = WiqiForm(request.POST)
        wiqistack_form = WiqiStackForm(request.POST, request.FILES)
        if wiqi_form.is_valid() and wiqistack_form.is_valid():
            # http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-as-a-single-expression
            kwargs = dict(wiqi_form.cleaned_data.items() + wiqistack_form.cleaned_data.items())
            kwargs["file"] = request.FILES.get("file", "")
            kwargs["creator"] = request.user
            kwargs["creator_ip"] = wiqid.get_user_ip(request)
            if nav_type == "create":
                kwargs["WiqiStack"] = wiqid.get_wiqi_or_404(wiqi_type)
            if nav_type == "fork":
                # get the new wiqi item as the new reference
                wiqi_object = wiqi_object.fork(**kwargs)
            else:
                wiqi_object.set(**kwargs)
            # capture the wiqi after any changes made
            kwargs["wiqi"] = wiqi_object
            wiqi_object.update(**kwargs)
            if nav_type != "edit" and request.user.is_subscribed:
                # assign all permissions to this wiqi to the user
                wiqi_object.assign_all_perm(request.user)   
            return redirect(wiqi_object)
    else:
        wiqi_form = WiqiForm(instance=wiqi_object)
        wiqistack_form = WiqiStackForm(instance=wiqistack_object, initial={"comment": ""})
    return render(request, template_name, locals())

@login_required
def compare_wiqi(request, wiqi_surl, template_name="compare.html", nav_type="compare", permission="can_view_stack"):
    """
    Compares two wiqis to each other and presents as html.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission)
    page_title = wiqi_object.stack.title
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    wiqi_a = request.GET.get('a', False)
    wiqi_b = request.GET.get('b', False)
    if not wiqi_a or not wiqi_b or wiqi_a == wiqi_b:
        return redirect(wiqi_object)
    # Already have permission to view the stack
    wiqi_a = wiqid.get_wiqi_object_or_404(lurs(wiqi_a), request.user, None, wiqi_object.get_class)
    wiqi_b = wiqid.get_wiqi_object_or_404(lurs(wiqi_b), request.user, None, wiqi_object.get_class)
    diff_wiqis = wiqid.compare_wiqis(wiqi_a.htmlresponse, wiqi_b.htmlresponse)
    # Queue up for view
    wiqi_links = wiqi_object.stack
    return render(request, template_name, locals())

@login_required
def revert_wiqi(request, wiqi_type, wiqi_surl, template_name="revert.html", nav_type="revert", permission="can_revert"):
    """
    Reverts wiqistack to previous version. Does so by creating a new wiqistack.
    """
    wiqistack_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission, wiqi_type)
    page_title = wiqistack_object.title
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqistack_object.wiqi)
    usr_ip = wiqid.get_user_ip(request)
    now = pytz.UTC.localize(datetime.now())
    kwargs = {}
    kwargs["creator"] = request.user
    kwargs["creator_ip"] = wiqid.get_user_ip(request)
    if request.is_ajax():
        wiqistack_object.revert(**kwargs)
        return wiqistack_object.wiqi
    if request.method == "POST":
        form = WiqiStackRevertForm(request.POST)
        if form.is_valid():
            wiqistack_object.revert(**kwargs)
            return redirect(wiqistack_object.wiqi)
    else:
        form = WiqiStackRevertForm()
    return render(request, template_name, locals())

def view_nav(request, wiqi_surl, template_name="wiqi/view.html", nav_type="view", permission="can_view"):
    """
    Fetch the current nav view ... returns only view page if not logged in.
    """
    if request.is_ajax():
        wiqi_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission)
        nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        nav_set["view"] = wiqi_object.get_url()
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return Http404