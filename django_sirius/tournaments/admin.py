from django.contrib import admin
from .models import Team, Tournament, Match

admin.site.register([Team, Tournament, Match])
# Register your models here.
