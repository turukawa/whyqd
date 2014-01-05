from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

import json
from guardian.shortcuts import assign, get_objects_for_user, get_perms

from whyqd.wiqi.models import Wiqi, DEFAULT_WIQISTACK_TYPE
from whyqd.wiqi.forms import WiqiForm, WiqiStackRangeForm, WiqiStackRevertForm
from whyqd.wiqi import wiqi as wiqid
from whyqd.snippets.shrtn import surl, lurs
from whyqd.snippets.diff2merge import docxtract

def index(request, template_name="wiqi/index.html", nav_type="view"):
    ''' Temporary to see what we've got, covered by search later'''
    page_title = "Home"
    nav_set = None
    if request.is_ajax():
        HttpResponse(json.dumps({}), content_type="application/json")
    return render(request, template_name, locals())

def view_wiqi_list(request, template_name="wiqi/list.html", nav_type="view"):
    ''' Temporary to see what we've got, covered by search later'''
    wiqi_list = get_list_or_404(Wiqi.wiqi_objects.all().published())
    page_title = "list"
    nav_set = None
    return render(request, template_name, locals())

def view_wiqi(request, wiqi_surl, wiqi_type=None, template_name="wiqi/view.html", nav_type="view", permission="can_view"):
    """
    Doubles as the wiqistack list, and wiqistack view as well.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission, wiqi_type)
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    try:
        page_title = wiqi_object.stack.title
    except AttributeError:
        # It's from a wiqistack
        page_title = wiqi_object.title
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
def edit_wiqi(request, wiqi_type=None, wiqi_surl=None, previous_wiqi=None,
              template_name="wiqi/edit.html", nav_type="edit", permission="can_edit"):
    """
    Edits existing or creates new wiqistack object.
    Performs branch from any wiqistack item.
    """
    #check if there was a javascript call
    j_template = request.GET.get('j', None)
    if j_template:
        template_name = "wiqi/%s.html" % j_template
    if request.GET.get('lw', False):
        linked_wiqi = wiqid.get_wiqi_object_or_404(lurs(request.GET['lw']), request.user, permission)
    if nav_type == "create":
        if wiqi_type is None:
            wiqi_type = DEFAULT_WIQISTACK_TYPE
        wiqi_object = Wiqi()
        wiqistack_object = None
        page_title = None
    else:
        # Get the wiqi object to be edited or branched
        wiqistack_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission, wiqi_type)
        wiqi_object = wiqistack_object.wiqi
        wiqi_type = wiqi_object.get_class
        page_title = wiqistack_object.title
    # This is for a standard call to the non-ajax editing form
    WiqiStackForm = wiqid.get_wiqi_form(wiqi_type)
    if request.method == "POST":
        if request.is_ajax():
            # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
            kwargs = request.POST.dict()
        else:
            wiqistack_form = WiqiStackForm(request.POST, request.FILES)
            if wiqistack_form.is_valid(): # and wiqi_form.is_valid()  
                # http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-as-a-single-expression
                #kwargs = dict(wiqi_form.cleaned_data.items() + wiqistack_form.cleaned_data.items())
                kwargs = wiqistack_form.cleaned_data
            else:
                return render(request, template_name, locals())
        kwargs["file"] = request.FILES.get("file", "")
        kwargs["creator"] = request.user
        kwargs["creator_ip"] = wiqid.get_user_ip(request)
        if nav_type == "create":
            kwargs["WiqiStack"] = wiqid.get_wiqi_or_404(wiqi_type)
        if nav_type == "branch":
            # get the new wiqi item as the new reference
            wiqi_object = wiqistack_object.branch(**kwargs)
            wiqistack_object = wiqi_object.stack
            kwargs["branching"] = True
        elif nav_type != "create":
            # Test whether wiqistack_object is at the top of the stack
            # Revert it to the top if it isn't, then make changes below
            if not wiqistack_object.is_top_of_stack:
                print "###################################"
                print wiqi_type, wiqi_object, wiqistack_object
                wiqistack_object.revert(**kwargs)
        else:
            # We're creating...
            wiqi_object.set(**kwargs)
        # Capture the wiqi after any changes made
        wiqi_object.update(**kwargs)
        if nav_type != "edit" and request.user.is_subscribed:
            # assign all permissions to this wiqi to the user
            wiqi_object.assign_all_perm(request.user)
        # Assign the previous wiqi to this wiqi, if it exists
        if previous_wiqi:
            previous_wiqi_object = wiqid.get_wiqi_object_or_404(lurs(previous_wiqi), request.user, permission)
            if wiqi_object.previous_wiqi != previous_wiqi_object:
                wiqi_object.previous_wiqi = previous_wiqi_object
                if previous_wiqi_object.next_wiqi:
                    wiqi_object.next_wiqi = previous_wiqi_object.next_wiqi
                    previous_wiqi_object.next_wiqi.previous_wiqi = wiqi_object
                    previous_wiqi_object.next_wiqi.save()
                wiqi_object.save()
                previous_wiqi_object.next_wiqi = wiqi_object
                previous_wiqi_object.save()
        # Update any linked wiqis through the standard handler
        if request.GET.get('lw', False):
            linked_wiqi.stack.update_link(wiqi_object)
        if request.is_ajax():
            nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
            nav_set['wiqi'] = wiqi_object.jsonresponse
            return HttpResponse(json.dumps(nav_set), content_type="application/json")
        else:
            return redirect(wiqi_object)
    else:
        wiqistack_form = WiqiStackForm(instance=wiqistack_object)
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

@login_required
def upload_docx(request, template_name="wiqi/view.html", nav_type="view"):
    '''
    Receive a file and return the components necessary for the user to organise and save it.    
    '''
    nav_set = None #wiqid.get_wiqi_nav(request, nav_type, wiqistack_object.wiqi)
    usr_ip = wiqid.get_user_ip(request)
    if request.is_ajax():
        # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
        kwargs = request.POST.dict()
        kwargs["file"] = request.FILES.get("file", "")
        tree = docxtract(kwargs["file"])
        return HttpResponse(json.dumps(tree), content_type="application/json")
    return render(request, template_name, locals())

def view_nav(request, wiqi_surl, template_name="wiqi/view.html", nav_type="view", permission="can_view"):
    """
    Fetch the current nav view ... returns only view page if not logged in.
    """
    if request.is_ajax():
        wiqi_object = wiqid.get_wiqi_object_or_404(lurs(wiqi_surl), request.user, permission)
        nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        nav_set["wiqi"] = wiqi_object.jsonresponse
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return Http404