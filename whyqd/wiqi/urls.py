from django.conf.urls import patterns, include, url

urlpatterns = patterns("whyqd.wiqi.views",
                       url(r'^$', 'index', {"template_name": "wiqi/index.html", "nav_type":"view"}, name='index'),
                       # process_docx: upload, download and organise to create a book
                       url(r"^docxtract/", "upload_docx", {"template_name": "wiqi/docxtract.html", "nav_type":"view"}, name="upload_docx"),
                       url(r"^list/", "view_wiqi_list", {"template_name": "wiqi/list.html", "nav_type":"view"}, name="view_wiqi_list"), # Temporary simply to have something to see
                       # edit_wiqi: create, edit, branch
                       url(r"^create/(?P<wiqi_type>[-\w]+)/(?P<previous_wiqi>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None}, name="create_previous_wiqi"),
                       url(r"^create/(?P<wiqi_type>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None}, name="create_wiqi"),                       
                       url(r"^create/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None}, name="create_default_wiqi"),
                       url(r"^write/(?P<wiqi_type>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/book.html", "nav_type":"create", "permission":None}, name="create_book"),   
                       #url(r"^edit/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/(?P<linked_wiqi_surl>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"edit", "permission":"can_edit"}, name="edit_wiqi"),
                       url(r"^edit/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"edit", "permission":"can_edit"}, name="edit_wiqi"),
                       url(r"^branch/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"branch", "permission":"can_branch"}, name="branch_wiqi"),
                       url(r"^compare/(?P<wiqi_surl>[-\w]+)/", "compare_wiqi", {"template_name": "wiqi/view.html", "nav_type":"compare", "permission":"can_view_stack"}, name="compare_wiqi"),
                       url(r"^revert/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", "revert_wiqi", {"template_name": "wiqi/revert.html", "nav_type":"revert", "permission":"can_revert"}, name="revert_wiqi"),
                       #url(r"^merge/(?P<wiqistack_surl>[-\w]+)/", "merge_wiqi", {"template_name": "wiqi/merge.html", "nav_type":"merge", "permission":"can_merge"}, name="merge_wiqi"),
                       # view_wiqi: view, stack, viewstack
                       url(r"^stack/(?P<wiqi_surl>[-\w]+)/", "view_wiqi", {"template_name": "wiqi/liststack.html", "nav_type":"stack", "permission":"can_view_stack"}, name="view_wiqistacklist"),
                       url(r"^view/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", "view_wiqi", {"template_name": "wiqi/view.html", "nav_type":"viewstack", "permission":"can_view_stack"}, name="view_wiqistack"),
                       url(r"^view/(?P<wiqi_surl>[-\w]+)/", "view_wiqi", {"template_name": "wiqi/view.html", "nav_type":"view", "permission":"can_view"}, name="view_wiqi_full"),
                       url(r"^nav/(?P<nav_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", "view_nav", {"template_name": "wiqi/view.html", "permission":"can_view"}, name="view_nav"),
                       url(r"^embed/(?P<wiqi_surl>[-\w]+)/", "view_wiqi", {"template_name": "wiqi/embed.html", "nav_type":"view", "permission":"can_view"}, name="embed_wiqi"),
                       url(r"^(?P<wiqi_surl>[-\w]+)/", "view_wiqi", {"template_name": "wiqi/view.html", "nav_type":"view", "permission":"can_view"}, name="view_wiqi"),
                       )