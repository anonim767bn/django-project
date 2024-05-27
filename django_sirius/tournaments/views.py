from rest_framework import viewsets
from .models import Tournament, Match, Team, Place
from .serializers import TournamentSerializer, MatchSerializer, TeamSerializer, PlaceSerializer
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from .permissions import UserAdminPermission
from .config import PAGES


def get_entity_page(entity_name, file_path='entity.html', page_info=PAGES):
    entity = page_info[entity_name]
    def entity_page(request, entity_id):
        return render(request, file_path, context={
            'title': entity['entity_link'][0], 
            'link': entity['list_link'],
            'fields': entity['fields'], 
            'foreigns': entity['foreigns'], 
            'object' : entity['model'].objects.get(id=entity_id)
            })
    return entity_page

tournament = get_entity_page('Tournament')
match = get_entity_page('Match')
place = get_entity_page('Place')
team = get_entity_page('Team')


def get_list_page(entity_name, file_path='list.html', page_info=PAGES):
    entity = page_info[entity_name]
    def list_page(request):
        return render(request, file_path, context={'entities': entity['model'].objects.all(), 'title': entity['list_link'][0], 'fields': entity['primary_fields'], 'link': entity['entity_link'][1], 'entity_name' : entity['entity_link'][0]})
    return list_page

tournaments = get_list_page('Tournament')
matches = get_list_page('Match')
places = get_list_page('Place')
teams = get_list_page('Team')


def get_viewset(model, serializer):
    class ViewSet(viewsets.ModelViewSet):
        permission_classes = [UserAdminPermission]
        queryset = model.objects.all()
        serializer_class = serializer

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)
    return ViewSet

TournamentViewSet = get_viewset(Tournament, TournamentSerializer)
MatchViewSet = get_viewset(Match, MatchSerializer)
TeamViewSet = get_viewset(Team, TeamSerializer)
PlaceViewSet = get_viewset(Place, PlaceSerializer)


class UserRegistrationViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def get(self, request):
        return render(request, 'register.html')


def main_page(request):
    page = {PAGES[key]['list_link'][0]: PAGES[key]['list_link'][1] for key in PAGES.keys()}
    page.update({'Регистрация': 'register'})
    return render(request, 'main.html', context={'pages': page})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


