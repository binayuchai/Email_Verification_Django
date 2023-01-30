from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from email_verify_app.models import Profile,User
# Register your models here.

admin.site.register(User,UserAdmin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","auth_token","is_verified","created_at")
