from django.contrib import admin
from Standards.models import Summons, SummonsRequest

# Register models to appear in the Django Admin DB Site
admin.site.register(Summons)
admin.site.register(SummonsRequest)