from django.contrib import admin
from CapApp.models import Grant, Grant_Publication, Publication, Keyword, Keyword_grant
# Register your models here.
admin.site.register(Grant)
admin.site.register(Grant_Publication)
admin.site.register(Publication)
admin.site.register(Keyword)
admin.site.register(Keyword_grant)
