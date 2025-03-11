from django.urls import path
from mailapp.apps import MailappConfig
from mailapp.views import RecipientMailListViews, RecipientMailDetailViews, RecipientMailCreateViews, RecipientMailUpdateViews, RecipientMailDeleteViews

app_name = MailappConfig.name

urlpatterns = [
     path("recipient_mail_list/", RecipientMailListViews.as_view(), name='recipient_mail_list'),
     path("recipient_mail_detail/<int:pk>/", RecipientMailDetailViews.as_view(), name="recipient_detail"),
     path("create/", RecipientMailCreateViews.as_view(), name="recipient_create"),
     path("/<int:pk>/update/", RecipientMailUpdateViews.as_view(), name="recipient_update"),
     path("/<int:pk>/delete/", RecipientMailDeleteViews.as_view(), name='recipient_delete'),
]