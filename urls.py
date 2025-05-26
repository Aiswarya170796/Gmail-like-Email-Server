from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('send_email/', views.send_email, name='send_email'),
    # path('emails/<str:folder>/', views.get_emails, name='get_emails'),
    # path('email/<int:email_id>/', views.email_detaail, name='email_detail'),
    path('email_list/', views.email_list, name='email_list'),
    path('email_search/', views.email_search, name='email_search'),
     path('compose/', views.compose_email, name='compose_email'),
    #   path('emails/<str:folder>/', views.get_emails_by_folder, name='get_emails_by_folder'),
    # path('emails/<int:email_id>/', views.email_detail, name='email_detail'),
    path('send_email/', views.send_email, name='send_email'),
    path('email_list/', views.email_list, name='email_list'),
    path('email_search/', views.email_search, name='email_search'),
    path('emails/<str:folder_name>/', views.email_list, name='email_list'),
     path('delete-emails/',views.delete_emails, name='delete_emails'),
    # path('delete-email/<int:email_id>/',views.delete_emails, name='delete_email'),
     path('email/<int:email_id>/',views.read_email, name='read_email'),
]
