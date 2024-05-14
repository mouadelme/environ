from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("whistleblower.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("form/", include("whistleblower.urls"))
]

handler404 = 'whistleblower.views.custom_404'



