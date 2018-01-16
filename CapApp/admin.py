from django.contrib import admin
from CapApp.models import Grant, Grant_Publication, Publication, Keyword, Related_grant
# Register your models here.
admin.site.register(Grant)
admin.site.register(Grant_Publication)
admin.site.register(Publication)
admin.site.register(Keyword)
admin.site.register(Related_grant)
