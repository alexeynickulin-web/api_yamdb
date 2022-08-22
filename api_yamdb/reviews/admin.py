from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User

admin.site.register(User, UserAdmin)
UserAdmin.list_display = ('email', 'username', 'first_name',
                          'last_name', 'role', 'bio', 'is_superuser')
