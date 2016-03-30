from django.conf.urls import patterns, include, url

# Django 1.9 url patterns
from whyqd.novel import views

urlpatterns = [
                # Create / Edit Novel
                url(r"^test/", views.test_novel,
                    {"template_name": "novel/test_novel.html"},
                    name="test_novel"),
                url(r"^create/", views.create_novel,
                    {"template_name": "novel/create_novel.html"},
                    name="create_novel"),
                # Organise the novel
                url(r"^organise/(?P<surl>[-\w]+)/", views.organise_novel,
                    {"template_name": "novel/create_novel.html", "permission":"can_edit"},
                    name="organise_novel"),
                # View the chapters
                url(r"^contents/(?P<surl>[-\w]+)/", views.view_chapters,
                    {"template_name": "novel/view_chapters.html"},
                    name="view_chapters"),
                # Set novel chapter pricing
                url(r"^pricing/(?P<surl>[-\w]+)/", views.price_novel,
                    {"template_name": "novel/price_novel.html", "permission":"can_edit"},
                    name="price_novel"),
                # Issue and Redeem tokens
                url(r"^tokens/issue/(?P<surl>[-\w]+)/", views.issue_tokens,
                    {"template_name": "novel/issue_tokens.html"},
                    name="issue_tokens"),
                url(r"^tokens/redeem/(?P<surl>[-\w]+)/", views.redeem_token,
                    {"template_name": "novel/redeem_token.html"},
                    name="redeem_token"),
                url(r"^tokens/refund/(?P<surl>[-\w]+)/", views.refund_token,
                    {"template_name": "novel/refund_token.html"},
                    name="refund_token"),
                url(r"^tokens/market/(?P<surl>[-\w]+)/", views.market_tokens,
                    name="market_tokens"),
                # Email token link to user
                url(r"^tokens/resend/(?P<surl>[-\w]+)/", views.resend_token,
                    {"template_name": "novel/issue_tokens.html"},
                    name="resend_token"),
                # Buy and bulk-buy novel
                url(r"^buy/", views.buy_novel,
                    {"template_name": "novel/buy_novel.html"},
                    name="buy_novel"),
                # Download books based on one-time link
                url(r"^download/(?P<surl>[-\w]+)/", views.download_novel,
                    {"template_name": "novel/download_novel.html"},
                    name="download_novel"),
                # JSONResponse settings
                url(r"^settings/", views.novel_settings,
                    name="novel_settings_pro"),
                url(r"^settings/(?P<surl>[-\w]+)/", views.novel_settings,
                    name="novel_settings"),
                url(r"^setcontents/(?P<surl>[-\w]+)/", views.set_chapters,
                    name="set_chapters"),
                # Upload Docx
                url(r"^docxtract/", views.upload_docx,
                    {"template_name": "novel/docxtract.html"},
                    name="upload_docx"),
                ## Administer novel
                # url(r"^sortit/", "administer_novel",
                #    {"template_name": "novel/administer_novel.html", "permission":"can_edit"},
                #    name="administer_novel"),
                ## View Novel
                #url(r"^(?P<surl>[-\w]+)/", "view_novel",
                #    {"template_name": "novel/view_novel.html"},
                #    name="view_novel"),
                ]