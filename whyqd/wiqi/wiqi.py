from django.template import  RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.http import Http404
from django.core.urlresolvers import reverse

from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

from whyqd.wiqi.models import Wiqi, Text, WIQI_TYPE_DICT, DEFAULT_WIQISTACK_TYPE #, Geomap, Image
from whyqd.wiqi.forms import TextForm, WIQI_FORM_TYPE_DICT#, GeomapForm, ImageForm
from whyqd.snippets import html2text 
from whyqd.snippets.diff_match_patch import diff_match_patch

import markdown2

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_wiqi_or_404(wiqi_type):
    """
    Return appropriate Wiqi class
    :param wiqi_type:
    :return:
    """
    try:
        return WIQI_TYPE_DICT[wiqi_type]
    except KeyError:
        raise Http404

def has_permission(wiqi_object, usr, permission):
    if permission:
        try:
            return wiqi_object.can_do(usr, permission)
        except AttributeError:
            # it's in the stack, so check the wiqi for permissions
            return wiqi_object.wiqi.can_do(usr, permission)
    return True

def get_user_view_rights(usr, wiqi_object):
    """
    Test the user viewing rights and update the current view for later reference;
    If viewing free while logged in, update price to current maximum;
    :param usr:
    :param wiqi_object:
    :return:
    """
    if wiqi_object.read_if == "open":
        return wiqi_object
    if usr.is_authenticated():
        if wiqi_object.read_if == "login" \
                or (wiqi_object.read_if == "own" and usr.can_read(wiqi_object)):
            if wiqi_object.price > usr.current_price:
                usr.current_price = wiqi_object.price
            usr.current_view = wiqi_object.surl
            usr.save()
            return wiqi_object
    # If user is not authenticated, or has no viewing rights,
    # return False to force redirect to register/login, or to buy
    return False

def get_wiqi_object_or_404(wiqi_surl, usr, wiqi_type=None, permission=None, nav_type=False):
    """
    Get wiqi object and check that user has permissions to perform task
    Any user can view a public object (protected or not)
    Any logged-in user can create a wiqi
    :rtype : wiqi
    """
    if wiqi_type:
        WiqiStack = get_wiqi_or_404(wiqi_type)
        wiqi_object = get_object_or_404(WiqiStack, surl=wiqi_surl)
    else:
        wiqi_object = get_object_or_404(Wiqi, surl=wiqi_surl)
        if nav_type == "view":
            return get_user_view_rights(usr, wiqi_object)
    if not has_permission(wiqi_object, usr, permission):
        raise Http404
    return wiqi_object

def get_wiqi_kwargs(request, wiqi_type, WiqiStackForm, **kwargs):
    """
    Update an existing wiqi with supplied kwargs
    :param request:
    :param WiqiStackForm:
    :return:
    """
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
            return False
    kwargs["file"] = request.FILES.get("file", "")
    kwargs["creator"] = request.user
    kwargs["creator_ip"] = get_user_ip(request)
    kwargs["WiqiStack"] = get_wiqi_or_404(wiqi_type)
    return kwargs

def link_previous_wiqi(request, wiqi_object, previous_wiqi, permission):
    """
    Receive the current wiqi and link it to a previous wiqi in a chain of wiqis;
    :param request:
    :param wiqi_object:
    :param previous_wiqi:
    :param permission:
    :return:
    """
    previous_wiqi_object = get_wiqi_object_or_404(previous_wiqi, request.user, None, permission)
    if wiqi_object.previous_wiqi != previous_wiqi_object:
        wiqi_object.previous_wiqi = previous_wiqi_object
        if previous_wiqi_object.next_wiqi:
            wiqi_object.next_wiqi = previous_wiqi_object.next_wiqi
            previous_wiqi_object.next_wiqi.previous_wiqi = wiqi_object
            previous_wiqi_object.next_wiqi.save()
        wiqi_object.save()
        previous_wiqi_object.next_wiqi = wiqi_object
        previous_wiqi_object.save()
    return previous_wiqi_object, wiqi_object

def process_linked_wiqi_or_404(request, permission, wiqi_object):
    """
    Any wiqi can have a linked wiqi, however, it will not be updated with new
    data through this call.
    All that will happen is that - if it exists - the updating/creating wiqi will
    be passed to it and it must then process this in its own way.
    This linked wiqi id will be passed in a request.GET of lw
    It will perform the processing and return True/False depending on the result
    NOTE: lw and wiqi_object must be Wiqi, not WiqiStack
    """
    lw = request.GET.get("lw", False)
    if lw:
        linked_wiqi = get_wiqi_object_or_404(lw, request.user, None, permission)
        linked_wiqi.stack.update_link(wiqi_object)
        return True
    else:
        return False
    
def get_wiqi_form(wiqistack_type):
    try:
        return WIQI_FORM_TYPE_DICT[wiqistack_type]
    except KeyError:
        raise Http404

def get_wiqi_nav(request, nav_type, wiqi_object):
    """
    Convert list of nav-types and nav-permissions into set of nav-types and links.
    """
    nav_response = []
    nav_set_true = {"view": ["edit"],
                    "edit": ["edit", "stack", "branch", "create"],
                    "can_edit": True
                    }
    nav_set_false = {"view": ["branch"],
                     "edit": ["branch", "stack", "create"],
                    "can_edit": False
                     }
    nav_set = nav_set_false
    nav_loop = ["view"]
    try:
        if request.user == wiqi_object.creator:
            nav_set = nav_set_true
    except AttributeError:
        return {"nav": nav_response.append([nav_type, None])}
    # Navigation Set: [link_function, link_permission]
    else:
    # if nav_type not view, then return either of edit or branch
    # else, return either of view edit or branch
        if nav_type == "view":
            nav_loop.extend(nav_set["view"])
        else:
            nav_loop.extend(nav_set["edit"])
        nav_get = {"view": [wiqi_object.get_url(), "can_view"],
                   "edit": [wiqi_object.get_edit_url(), "can_edit"],
                   "stack": [wiqi_object.get_stacklist_url(),"can_view_stack"],
                   #"share": [wiqi_object.get_share_url,"can_share"],
                   #"revert": [wiqi_object.get_revert_url(),"can_revert"], 
                   "branch": [wiqi_object.get_branch_url(),"can_branch"],
                   "create": [reverse('create_previous_wiqi', kwargs={'wiqi_type': wiqi_object.get_class, 'previous_wiqi': wiqi_object.surl}), "can_create"],
                   #"merge": [wiqi_object.get_merge_url,"can_merge"],
                   }
        for nav_item in nav_loop:
            nav_url, nav_permission = nav_get[nav_item]
            if not has_permission(wiqi_object, request.user, nav_permission):
                continue
            #if not nav_set["can_edit"] and nav_item == "branch":
            #    nav_item = "edit"
            nav_response.append([nav_item, nav_url])
    return {"nav": nav_response}
    
def compare_wiqis(wiqi1, wiqi2):
    """
    Create an html report based on the differences between wiqi1 and wiqi2.
    """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(html2text.html2text(wiqi1), html2text.html2text(wiqi2))
    dmp.diff_cleanupSemantic(diffs)
    html = []
    for (op, text) in diffs:
        if op == dmp.DIFF_INSERT:
            html.append("<ins class=\"whyqd-diff-inserted\">%s</ins>" % text)
        elif op == dmp.DIFF_DELETE:
            html.append("<del class=\"whyqd-diff-deleted\">%s</del>" % text)
        elif op == dmp.DIFF_EQUAL:
            html.append("%s" % text)
    return markdown2.markdown("".join(html))