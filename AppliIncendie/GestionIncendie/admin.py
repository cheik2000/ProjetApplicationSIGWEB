from django.contrib import admin
from .models import DirectionProvinciale, Ccdrf, SecteurForestier, Incendie, PointEau, PosteVigie, TracheeParFeu

# Register your models here.
admin.site.register(DirectionProvinciale)
admin.site.register(Ccdrf)
admin.site.register(SecteurForestier)
admin.site.register(Incendie)
admin.site.register(PointEau)
admin.site.register(PosteVigie)
admin.site.register(TracheeParFeu)