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
                       url(r"^tokens/refund/(?P<surl>[-\w]+)/", "refund_token",
                           {"template_name": "novel/refund_token.html"},
                           name="refund_token"),
                       url(r"^tokens/market/(?P<surl>[-\w]+)/", "market_tokens",
                           name="market_tokens"),
                       # Email token link to user
                       url(r"^tokens/resend/(?P<surl>[-\w]+)/", "resend_token",
                           {"template_name": "novel/issue_tokens.html"},
                           name="resend_token"),
                       # Buy and bulk-buy novel
                       url(r"^buy/", "buy_novel",
                           {"template_name": "novel/buy_novel.html"},
                           name="buy_novel"),
                       # Download books based on one-time link
                       url(r"^download/(?P<surl>[-\w]+)/", "download_novel",
                           {"template_name": "novel/download_novel.html"},
                           name="download_novel"),
                       # JSONResponse settings
                       url(r"^settings/", "novel_settings",
                           name="novel_settings"),
                       # Upload Docx
                       url(r"^docxtract/", "upload_docx",
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
                       )