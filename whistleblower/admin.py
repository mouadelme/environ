from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from whistleblower.models import UploadFile
from .models import User


admin.site.register(UploadFile)
admin.site.register(User, UserAdmin)

