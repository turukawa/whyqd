from django.conf.urls import patterns, include, url

# Django 1.9 url patterns
from whyqd.wiqi import views

urlpatterns = [
                # General
                url(r'^$', views.index, {"template_name": "wiqi/list.html"},
                    name='index'),
                # Create Wiqi
                url(r"^create/(?P<wiqi_type>[-\w]+)/(?P<previous_wiqi>[-\w]+)/", views.edit_wiqi,
                    {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None},
                    name="create_previous_wiqi"),
                url(r"^create/(?P<wiqi_type>[-\w]+)/", views.edit_wiqi,
                    {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None},
                    name="create_wiqi"),
                url(r"^create/", views.edit_wiqi,
                    {"template_name": "wiqi/edit.html", "nav_type":"create", "permission":None},
                    name="create_default_wiqi"),
                # Edit Wiqi
                #url(r"^edit/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/(?P<linked_wiqi_surl>[-\w]+)/", "edit_wiqi", {"template_name": "wiqi/edit.html", "nav_type":"edit", "permission":"can_edit"}, name="edit_wiqi"),
                url(r"^edit/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", views.edit_wiqi,
                    {"template_name": "wiqi/edit.html", "nav_type":"edit", "permission":"can_edit"},
                    name="edit_wiqi"),
                # Branch Wiqi
                url(r"^branch/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", views.edit_wiqi,
                    {"template_name": "wiqi/edit.html", "nav_type":"branch", "permission":"can_branch"},
                    name="branch_wiqi"),
                # History of Wiqi
                url(r"^stack/(?P<wiqi_surl>[-\w]+)/", views.view_wiqistacklist,
                    {"template_name": "wiqi/viewstack.html", "nav_type":"stack", "permission":"can_view_stack"},
                    name="view_wiqistacklist"),
                # Compare Wiqi history
                url(r"^compare/(?P<wiqi_surl>[-\w]+)/", views.compare_wiqi,
                    {"template_name": "wiqi/view.html", "nav_type":"compare", "permission":"can_view_stack"},
                    name="compare_wiqi"),
                # Revert from Wiqi history
                url(r"^revert/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", views.revert_wiqi,
                    {"template_name": "wiqi/revert.html", "nav_type":"revert", "permission":"can_revert"},
                    name="revert_wiqi"),
                # Merge a branched Wiqi
                #url(r"^merge/(?P<wiqistack_surl>[-\w]+)/", "merge_wiqi",
                # {"template_name": "wiqi/merge.html", "nav_type":"merge", "permission":"can_merge"},
                # name="merge_wiqi"),
                # Manage

                # Delete
                
                # View Wiqi List
                url(r"^list/", views.view_wiqi_list,
                    {"template_name": "wiqi/list.html", "nav_type":"view"},
                    name="view_wiqi_list"), # Temporary simply to have something to see
                # View Wiqi
                url(r"^view/(?P<wiqi_type>[-\w]+)/(?P<wiqi_surl>[-\w]+)/", views.view_wiqi,
                    {"template_name": "wiqi/view.html", "nav_type":"viewstack", "permission":"can_view_stack"},
                    name="view_wiqistack"),
                url(r"^view/(?P<wiqi_surl>[-\w]+)/", views.view_wiqi,
                    {"template_name": "wiqi/view.html", "nav_type":"view"},
                    name="view_wiqi_full"),
                url(r"^(?P<wiqi_surl>[-\w]+)/", views.view_wiqi,
                    {"template_name": "wiqi/view.html", "nav_type":"view"},
                    name="view_wiqi"),
              ]