from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.conf import settings

import json
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

from whyqd.wiqi.models import Wiqi, DEFAULT_WIQISTACK_TYPE
from whyqd.wiqi.forms import WiqiForm, WiqiStackRangeForm, WiqiStackRevertForm
from whyqd.wiqi import wiqi as wiqid
from whyqd.novel.models import Novel
from whyqd.snippets.forex import get_forex

def index(request, template_name="wiqi/index.html", nav_type="view"):
    '''
    We're assuming one site, one novel ... this could change in future ...
    '''
    novel_object = Novel.objects.all()
    if not novel_object:
        return redirect("create_novel")
    novel_object = novel_object[0]
    page_title = novel_object.title
    page_subtitle = "Start Reading"
    show_buy = True
    if request.user.is_authenticated():
        if request.user.can_read(novel_object) == "owns":
            show_buy = False
    nav_set = None
    # forex settings
    fx = get_forex()
    fxd = settings.DEFAULT_CURRENCY
    if request.is_ajax():
        HttpResponse(json.dumps({}), content_type="application/json")
    return render(request, template_name, locals())

def view_wiqi_list(request, template_name="wiqi/list.html", nav_type="view"):
    ''' Temporary to see what we've got, covered by search later'''
    wiqi_list = get_list_or_404(Wiqi.wiqi_objects.all().published())
    page_title = "list"
    nav_set = None
    return render(request, template_name, locals())

def view_wiqi(request, wiqi_surl, wiqi_type=None, template_name="wiqi/view.html", nav_type="view"):
    """
    Return wiqi view, or the view of the stack (item or list) from the wiqi.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, wiqi_type, None, nav_type)
    if wiqi_object:
        # If no wiqi object, user has no rights to view, and must login or buy...
        nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        template_name = "wiqi/view_%s.html" % wiqi_object.get_class
        try:
            chapter_title = wiqi_object.stack.title
            # Kludge for novel title
            novel_object = wiqi_object.stack.wiqi.novel_chapterlist.all()[0]
        except AttributeError:
            # It's from a wiqistack
            chapter_title = wiqi_object.title
            novel_object = wiqi_object.wiqi.novel_chapterlist.all()[0]
            nav_title = "stack"
        page_title = novel_object.title
        page_subtitle = chapter_title
        # Prepare for viewing next_wiqi
        next_wiqi = wiqi_object.next_wiqi
        if next_wiqi:
            can_read_next = False
            if request.user.is_authenticated():
                can_read_next = request.user.can_read(next_wiqi)
            if not can_read_next:
                can_read_next = next_wiqi.read_if
        # forex settings
        fx = get_forex()
        fxd = settings.DEFAULT_CURRENCY
    else:
        return redirect('index')
    if request.is_ajax():
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return render(request, template_name, locals())

def view_wiqistacklist(request, wiqi_surl, wiqi_type=None, template_name="wiqi/view.html", nav_type="view",
                       permission="can_view"):
    """
    Return wiqi list view from the wiqi.
    """
    wiqi_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, wiqi_type, permission)
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    template_name = "wiqi/viewstack_%s.html" % wiqi_object.get_class
    # The wiqi must not be a stack pointer
    page_title = wiqi_object.stack.title
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
              template_name="wiqi/edit", nav_type="edit", permission="can_edit"):
    """
    Edit existing or create new wiqistack object.
    Performs branch from any wiqistack item.
    """
    if wiqi_type is None and nav_type == "create":
        wiqi_type = DEFAULT_WIQISTACK_TYPE
    if wiqi_type is None:
        # Strictly enforce wiqi type binding to any editing or branching behaviour, ensures always in WiqiStack
        return Http404
    # Set the template
    if request.GET.get('j', None):
        template_name = "wiqi/view_%s.html" % wiqi_type
    else:
        template_name = "wiqi/edit_%s.html" % wiqi_type
    if nav_type == "create":
        # Create wiqi_object
        wiqi_object = Wiqi()
        wiqistack_object = None
        page_title = None
    else:
        # Get the wiqi object to be edited or branched
        wiqistack_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, wiqi_type, permission)
        wiqi_object = wiqistack_object.wiqi
        page_title = wiqistack_object.title
    # This is for a standard call to the non-ajax editing form
    WiqiStackForm = wiqid.get_wiqi_form(wiqi_type)
    if request.method == "POST":
        kwargs = wiqid.get_wiqi_kwargs(request, wiqi_type, WiqiStackForm)
        if not kwargs:
            wiqistack_form = WiqiStackForm(request.POST, request.FILES)
            return render(request, template_name, locals())
        if nav_type == "branch":
            # Get the new wiqi item as the new reference
            wiqi_object = wiqistack_object.branch(**kwargs)
            wiqistack_object = wiqi_object.stack
        if nav_type == "edit" and not wiqistack_object.is_top_of_stack:
            # Test whether wiqistack_object is at the top of the stack
            # Revert it to the top if it isn't, then make changes below
            wiqistack_object.revert(**kwargs)
        if nav_type == "create":
            # Create the Wiqi with kwargs
            wiqi_object.set(**kwargs)
        if nav_type != "branch":
            # Update the wiqi to link Wiqi to Stack
            wiqi_object.update(**kwargs)
        if nav_type != "edit" and request.user.is_subscribed:
            # assign all permissions to this wiqi to the user
            wiqi_object.assign_all_perm(request.user)
        # Assign the previous wiqi to this wiqi, if it exists
        if previous_wiqi:
            previous_wiqi_object, wiqi_object = wiqid.link_previous_wiqi(request, wiqi_object, previous_wiqi, permission)
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
    wiqi_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, None, permission)
    page_title = wiqi_object.stack.title
    nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
    wiqi_a = request.GET.get('a', False)
    wiqi_b = request.GET.get('b', False)
    if not wiqi_a or not wiqi_b or wiqi_a == wiqi_b:
        return redirect(wiqi_object)
    # Already have permission to view the stack
    wiqi_a = wiqid.get_wiqi_object_or_404(wiqi_a, request.user, wiqi_object.get_class)
    wiqi_b = wiqid.get_wiqi_object_or_404(wiqi_b, request.user, wiqi_object.get_class)
    diff_wiqis = wiqid.compare_wiqis(wiqi_a.htmlresponse, wiqi_b.htmlresponse)
    # Queue up for view
    return render(request, template_name, locals())

@login_required
def revert_wiqi(request, wiqi_type, wiqi_surl, template_name="revert.html", nav_type="revert", permission="can_revert"):
    """
    Reverts wiqistack to previous version. Does so by creating a new wiqistack.
    """
    wiqistack_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, permission, wiqi_type)
    kwargs = {"creator": request.user, "creator_ip": wiqid.get_user_ip(request)}
    wiqistack_object.revert(**kwargs)
    if request.is_ajax():
        return wiqistack_object.wiqi
    else:
        return redirect(wiqistack_object.wiqi)

def view_nav(request, wiqi_surl, template_name="wiqi/view.html", nav_type="view", permission="can_view"):
    """
    Fetch the current nav view ... returns only view page if not logged in.
    """
    if request.is_ajax():
        wiqi_object = wiqid.get_wiqi_object_or_404(wiqi_surl, request.user, permission)
        nav_set = wiqid.get_wiqi_nav(request, nav_type, wiqi_object)
        nav_set["wiqi"] = wiqi_object.jsonresponse
        return HttpResponse(json.dumps(nav_set), content_type="application/json")
    else:
        return Http404