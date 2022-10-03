from django.contrib import admin

from api.models import Movie, AdditionalInfo, Review, Actor

admin.site.register(Movie)
admin.site.register(AdditionalInfo)
admin.site.register(Review)
admin.site.register(Actor)
