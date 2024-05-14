"""
URL configuration for whistleblower project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls, name='admin'),
    # path("", views.default, name="index"),
    path("", views.auth, name='home'),
    path("form", views.upload_form, name='upload_form'),
    path("logout", views.logout_view, name='logout'),
    path("", include("allauth.urls"), name='all_auth'),
    path("files/", views.files, name='files'),
    path("files/<str:order>/", views.files, name='files_order'),

    path("file_view/<str:file_id>/", views.files_view, name='files_view'),

    path("my_submissions", views.my_submissions, name='my_submissions'),
    path('my_submissions/date_newest/', views.my_submissions_newest, name='my_submissions_newest'),
    path('my_submissions/date_oldest/', views.my_submissions_oldest, name='my_submissions_oldest'),
    path('delete_submission/<int:submission_id>/', views.delete_submission, name='delete_submission'),

    path("about", views.about_page, name='about_page'),
    path("reports", views.current_report, name='report'),
    path("reports/<str:order>/", views.current_report, name='report_order'),
]

handler404 = 'whistleblower.views.custom_404'
