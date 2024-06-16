"""Views for tournaments app."""
from typing import Callable, Optional

from django.contrib.auth import login, logout, models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import authtoken, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .config import PAGES
from .forms import MatchForm, PlaceForm, TeamForm, TournamentForm
from .models import Match, Place, Team, Tournament
from .permissions import UserAdminPermission
from .serializers import (MatchSerializer, PlaceSerializer, TeamSerializer,
                          TournamentSerializer)

Token = authtoken.models.Token
STR_LIST_LINK = 'list_link'
STR_TITLE = 'title'
STR_ENTITY_LINK = 'entity_link'
STR_USER = 'user'
STR_LINK = 'link'
STR_MODEL = 'model'

TOURNAMENT = 'Tournament'
MATCH = 'Match'
PLACE = 'Place'
TEAM = 'Team'


def get_entity_page(
    entity_name: str,
    file_path: Optional[str] = 'entity.html',
    page_info: Optional[dict] = PAGES,
):
    """Generate entity page view.

    Args:
        entity_name (str): name of entity (like in config)\
            to generate entity page.
        file_path (str, optional): path to enitty html file.\
            Defaults to 'entity.html'.
        page_info (dict, optional): configuration dict.\
            Defaults to PAGES in config.py.

    Returns:
        Callable: entity page view
    """
    entity = page_info[entity_name]

    def entity_page(request, entity_id):
        return render(request, file_path, context={
            STR_TITLE: entity[STR_ENTITY_LINK][0],
            STR_LINK: entity[STR_LIST_LINK],
            'fields': entity['fields'],
            'foreigns': entity['foreigns'],
            'object': entity[STR_MODEL].objects.get(id=entity_id),
            STR_USER: request.user,
            'id': entity_id,
            'delete_page': entity['delete_page'],
            'edit_page': entity['form_link'][1],
        })
    return entity_page


tournament = get_entity_page(TOURNAMENT)
match = get_entity_page(MATCH)
place = get_entity_page(PLACE)
team = get_entity_page(TEAM)


def get_list_page(entity_name, file_path='list.html', page_info=PAGES):
    """list_page view generator.

    Args:
        entity_name (str): like in config.py.
        file_path (str, optional): path to html file. Defaults to 'list.html'.
        page_info (dict, optional): config dict in config.py.\
            Defaults to PAGES.

    Returns:
        Callable: function list_page.
    """
    entity = page_info[entity_name]

    def list_page(request):
        return render(
            request,
            file_path,
            context={
                'entities': entity[STR_MODEL].objects.all(),
                STR_TITLE: entity[STR_LIST_LINK][0],
                'fields': entity['primary_fields'],
                STR_LINK: entity[STR_ENTITY_LINK][1],
                'entity_name': entity[STR_ENTITY_LINK][0],
                STR_USER: request.user,
                'create': entity['form_link'][0],
            },
        )
    return list_page


tournaments = get_list_page(TOURNAMENT)
matches = get_list_page(MATCH)
places = get_list_page(PLACE)
teams = get_list_page(TEAM)


def get_delete_page(entity_name: str, page_info: Optional[dict] = PAGES):
    """delete_page view generator.

    Args:
        entity_name (str): like in config.py.
        page_info (dict, optional): config dict in config.py.\
            Defaults to PAGES.

    Returns:
        Callable: function to create_page.
    """
    entity = page_info[entity_name]

    def delete_page(request, entity_id):
        object_for_del = entity[STR_MODEL].objects.get(id=entity_id)
        if object_for_del.owner == request.user or request.user.is_staff:
            object_for_del.delete()
        return redirect(entity[STR_LIST_LINK][1])
    return delete_page


tournament_delete = get_delete_page(TOURNAMENT)
match_delete = get_delete_page(MATCH)
place_delete = get_delete_page(PLACE)
team_delete = get_delete_page(TEAM)


def get_create_page(
    entity_name: str,
    form_class: type,
    file_path: Optional[str] = 'form.html',
    page_info: Optional[dict] = PAGES,
) -> Callable:
    """Create_page view generator.

    Args:
        entity_name (str): like in config.py.
        form_class (type): ModelForm class.
        file_path (str, optional): path to html file. Defaults to 'form.html'.
        page_info (dict, optional): config dict in config.py.\
            Defaults to PAGES.

    Returns:
        Callable: function to create_page.
    """
    entity = page_info[entity_name]
    list_link = entity[STR_LIST_LINK][1]

    def create_page(request):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.owner = request.user
                form.save()
                return redirect(list_link)
        else:
            form = form_class()
        return render(request, file_path, context={
            'form': form,
            STR_TITLE: entity[STR_ENTITY_LINK][0],
            STR_LINK: list_link,
            STR_USER: request.user,
        })
    return create_page


tournament_create = get_create_page(TOURNAMENT, TournamentForm)
match_create = get_create_page(MATCH, MatchForm)
place_create = get_create_page(PLACE, PlaceForm)
team_create = get_create_page(TEAM, TeamForm)


def get_update_page(
    entity_name: str,
    form_class: type,
    file_path: Optional[str] = 'form.html',
    page_info: Optional[dict] = PAGES,
) -> Callable:
    """Update_page view generator.

    Args:
        entity_name (str): like in config.py.
        form_class (type): ModelForm class.
        file_path (str, optional): path to html file. Defaults to 'form.html'.
        page_info (dict, optional): config dict in config.py.\
            Defaults to PAGES.

    Returns:
        Callable: function to update_page.
    """
    entity = page_info[entity_name]

    def update_page(request, entity_id):
        object_for_update = get_object_or_404(entity[STR_MODEL], id=entity_id)
        is_owner = object_for_update.owner == request.user
        has_permission = request.user.is_staff or is_owner
        if not has_permission:
            return redirect(entity[STR_LIST_LINK][1])
        if request.method == 'POST':
            form = form_class(request.POST, instance=object_for_update)
            if form.is_valid():
                form.save()
                return redirect(entity[STR_LIST_LINK][1])
        else:
            form = form_class(instance=object_for_update)
        return render(request, file_path, context={
            'form': form,
            STR_TITLE: entity[STR_ENTITY_LINK][0],
            STR_LINK: entity[STR_LIST_LINK][1],
            STR_USER: request.user,
        })
    return update_page


tournament_update = get_update_page(TOURNAMENT, TournamentForm)
match_update = get_update_page(MATCH, MatchForm)
place_update = get_update_page(PLACE, PlaceForm)
team_update = get_update_page(TEAM, TeamForm)


def get_viewset(model_class: type, serializer: type) -> type:
    """Generate viewset for model_clas.

    Args:
        model_class (type): model_class.
        serializer (type): serializer class.

    Returns:
        type: viewset class.
    """
    class ViewSet(viewsets.ModelViewSet):
        permission_classes = [UserAdminPermission]
        queryset = model_class.objects.all()
        serializer_class = serializer

        def perform_create(self, serializer_class):
            serializer_class.save(owner=self.request.user)
    return ViewSet


TournamentViewSet = get_viewset(Tournament, TournamentSerializer)
MatchViewSet = get_viewset(Match, MatchSerializer)
TeamViewSet = get_viewset(Team, TeamSerializer)
PlaceViewSet = get_viewset(Place, PlaceSerializer)


class UserRegistrationViewSet(APIView):
    """Register user view."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> HttpResponse:
        """Register user.

        Args:
            request (HttpRequest): request.data must contain \
            'username' and 'password'

        Returns:
            HttpResponse: 409 if user with this username already exists, \
                400 if username or password is not provided, \
                201 if user was created successfully
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {
                    'error': 'Please provide both username and password',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if models.User.objects.filter(username=username).exists():
            return Response(
                {
                    'error': 'User with this username already exists',
                },
                status=status.HTTP_409_CONFLICT,
            )
        user = models.User.objects.create_user(
            username=username,
            password=password,
        )
        login(request, user)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render registration page.

        Args:
            request (HttpRequest): The request object that Django received.

        Returns:
            HttpResponse: registration page.
        """
        return render(request, 'register.html')


class UserLoginViewSet(APIView):
    """Login user view."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> HttpResponse:
        """Login user.

        Args:
            request (HttpRequest): must contain 'username' and 'password'

        Returns:
            HttpResponse: 400 if username or password is not provided, \
            401 if user with this username or password is incorrect, \
            200 if user was logged in successfully
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {
                    'error': 'Please provide both username and password',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = models.User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response(
                {
                    'Error': 'Invalid username or password',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
        else:
            token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render login page.

        Args:
            request (HttpRequest): The request object that Django received.

        Returns:
            HttpResponse: login page.
        """
        return render(request, 'login.html', context={STR_TITLE: 'Войти'})


def logout_page(request: HttpRequest) -> HttpResponseRedirect:
    """Logout user.

    Args:
        request (HttpRequest): user must be authenticated

    Returns:
        HttpResponseRedirect: redirect to main page
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('main_page')


def main_page(request: HttpRequest) -> HttpResponse:
    """Render main page.

    Args:
        request (HttpRequest): The request object that Django received.

    Returns:
        HttpResponse: An HttpResponse that renders the main.html template.
    """
    page = {}
    for name in PAGES.keys():
        page_key = PAGES[name][STR_LIST_LINK][0]
        page_value = PAGES[name][STR_LIST_LINK][1]
        page[page_key] = page_value
    return render(
        request,
        'main.html',
        context={
            STR_TITLE: 'Главная страница',
            'pages': page,
            STR_USER: request.user,
        },
    )


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render 404 page.

    Args:
        request (HttpRequest): The request object that Django received.
        exception (Exception): The exception that was raised.

    Returns:
        HttpResponse: An HttpResponse that renders the 404.html \
              template with a status code of 404.
    """
    return render(
        request,
        '404.html',
        status=status.HTTP_404_NOT_FOUND,
    )
