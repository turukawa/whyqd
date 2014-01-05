from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import logout

from whyqd.usr.forms import SubscribeForm

def logout(request, next_page="/"):
    logout(request)

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