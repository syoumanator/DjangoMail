from django.urls import path
from mailapp.apps import MailappConfig
from mailapp.views import RecipientMailListViews, RecipientMailDetailViews, RecipientMailCreateViews, \
     RecipientMailUpdateViews, RecipientMailDeleteViews, MailMessageListViews, MailMessageDetailViews, \
     MailMessageCreateViews, MailMessageUpdateViews, MailMessageDeleteViews, MailingListViews, MailingDetailViews, \
     MailingCreateViews, MailingUpdateViews, MailingDeleteViews

app_name = MailappConfig.name

urlpatterns = [
     path("recipient/", RecipientMailListViews.as_view(), name="recipient_list"),
     path("recipient/detail/<int:pk>/", RecipientMailDetailViews.as_view(), name="recipient_detail"),
     path("recipient/create/", RecipientMailCreateViews.as_view(), name="recipient_create"),
     path("recipient/update/<int:pk>/", RecipientMailUpdateViews.as_view(), name="recipient_update"),
     path("recipient/delete/<int:pk>/", RecipientMailDeleteViews.as_view(), name="recipient_delete"),

     path("message/", MailMessageListViews.as_view(), name="mail_message_list"),
     path("message/detail/<int:pk>/", MailMessageDetailViews.as_view(), name="message_detail"),
     path("message/create/", MailMessageCreateViews.as_view(), name="message_create"),
     path("message/update/<int:pk>/", MailMessageUpdateViews.as_view(), name="message_update"),
     path("message/delete/<int:pk>/", MailMessageDeleteViews.as_view(), name="message_delete"),

     path("mailing/", MailingListViews.as_view(), name="mailing_list"),
     path("mailing/detail/<int:pk>/", MailingDetailViews.as_view(), name="mailing_detail"),
     path("mailing/create/", MailingCreateViews.as_view(), name="mailing_create"),
     path("mailing/update/<int:pk>/", MailingUpdateViews.as_view(), name="mailing_update"),
     path("mailing/delete/<int:pk>/", MailingDeleteViews.as_view(), name="mailing_delete"),
]
