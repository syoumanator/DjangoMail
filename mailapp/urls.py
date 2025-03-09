from django.urls import path
from . import views
from mailapp.apps import MailappConfig

app_name = MailappConfig.name

urlpatterns = [
     path('', views.RecipientMailListViews.as_view(), name='recipient_mail_list'),
     path('create/', views.RecipientMailCreateViews.as_view(), name='recipient_mail_create'),
     path('<int:pk>/update/', views.RecipientMailUpdateViews.as_view(), name='recipient_mail_update'),
     path('<int:pk>/delete/', views.RecipientMailDeleteViews.as_view(), name='recipient_mail_delete'),
     ]