"""
URL configuration for django_sirius project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tournaments.views import *
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'tournaments', TournamentViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'places', PlaceViewSet)

handler404 = 'tournaments.views.page_not_found'


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include((router.urls, 'tournaments_app'), namespace='api')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', UserRegistrationViewSet.as_view(), name='register'),
    path('', main_page, name='main_page'),
    path('tournament/<str:entity_id>/', tournament, name='tournament'),
    path('tournaments/', tournaments, name='tournaments'),
    path('teams/', teams, name='teams'),
    path('match/<str:entity_id>', match, name='match'),
    path('team/<str:entity_id>', team, name='team'),
    path('places/', places, name='places'),
    path('place/<str:entity_id>', place, name='place'),
    path('matches/', matches, name='matches'),
    path('login/', UserLoginViewSet.as_view(), name='login'),
    path('logout/', logout_page, name='logout'),
    path('delete/tournament/<str:entity_id>',
         tournament_delete, name='tournament_delete'),
    path('delete/team/<str:entity_id>', team_delete, name='team_delete'),
    path('delete/place/<str:entity_id>', place_delete, name='place_delete'),
    path('delete/match/<str:entity_id>', match_delete, name='match_delete'),
    path('create/tournament/', tournament_create, name='create_tournament'),
    path('create/team/', team_create, name='create_team'),
    path('create/place/', place_create, name='create_place'),
    path('create/match/', match_create, name='create_match'),
    path('update/tournament/<str:entity_id>',
         tournament_update, name='update_tournament'),
    path('update/team/<str:entity_id>', team_update, name='update_team'),
    path('update/place/<str:entity_id>', place_update, name='update_place'),
    path('update/match/<str:entity_id>', match_update, name='update_match'),
]
