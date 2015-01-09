from django.conf.urls import patterns, include, url

urlpatterns = patterns("whyqd.novel.views",
                       # Create / Edit Novel
                       url(r"^create/", "create_novel",
                           {"template_name": "novel/create_novel.html"},
                           name="create_novel"),
                       # Organise the novel
                       url(r"^organise/(?P<surl>[-\w]+)/", "organise_novel",
                           {"template_name": "novel/create_novel.html", "permission":"can_edit"},
                           name="organise_novel"),
                       # Upload Docx
                       url(r"^docxtract/", "upload_docx",
                           {"template_name": "novel/docxtract.html"},
                           name="upload_docx"),
                       # Set novel chapter pricing
                       url(r"^pricing/(?P<surl>[-\w]+)/", "price_novel",
                           {"template_name": "novel/price_novel.html", "permission":"can_edit"},
                           name="price_novel"),
                       # Issue and Redeem tokens
                       url(r"^tokens/issue/(?P<surl>[-\w]+)/", "issue_tokens",
                           {"template_name": "novel/issue_tokens.html"},
                           name="issue_tokens"),
                       url(r"^tokens/redeem/(?P<surl>[-\w]+)/", "redeem_token",
                           {"template_name": "novel/redeem_token.html"},
                           name="redeem_token"),
                       # Buy and bulk-buy novel
                       url(r"^buy/", "buy_novel",
                           {"template_name": "novel/buy_novel.html"},
                           name="buy_novel"),
                       # JSONResponse settings
                       url(r"^settings/", "novel_settings",
                           name="novel_settings"),
                       # Email token link to user
                       url(r"^resend/", "resend_novel",
                           {"template_name": "novel/issue_tokens.html"},
                           name="resend_novel"),
                       # Download books based on one-time link
                       url(r"^download/(?P<surl>[-\w]+)/", "download_novel",
                           {"template_name": "novel/download_novel.html"},
                           name="download_novel"),
                       # Administer novel
                        url(r"^sortit/", "administer_novel",
                           {"template_name": "novel/administer_novel.html", "permission":"can_edit"},
                           name="administer_novel"),
                       # View Novel
                       url(r"^(?P<surl>[-\w]+)/", "view_novel",
                           {"template_name": "novel/view_novel.html"},
                           name="view_novel"),
                       )