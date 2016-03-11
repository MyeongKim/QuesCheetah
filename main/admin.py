from django.contrib import admin
from main.models import User, ApiKey, Domain

# Register your models here.
admin.site.register(User)
admin.site.register(ApiKey)
admin.site.register(Domain)
