from rest_framework import viewsets
from .models import Tournament, Match, Team, Place
from .serializers import TournamentSerializer, MatchSerializer, TeamSerializer, PlaceSerializer
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserAdminPermission(permissions.BasePermission):
    _safe_methods = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        # Разрешить все запросы от аутентифицированных пользователей
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы всем
        if request.method in self._safe_methods:
            return True
        # Разрешить запросы от владельца объекта или администратора
        return obj.owner == request.user or request.user.is_staff

class TournamentViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MatchViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserRegistrationViewSet(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)




# Create your views here.
