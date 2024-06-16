from .models import Match, Place, Team, Tournament

TEST_PASSWORD = '12345'

PAGES = {
    'Tournament': {
        'delete_page': 'tournament_delete',
        'entity_link': ['Турнир', 'tournament'],
        'list_link': ['Турниры', 'tournaments'],
        'model': Tournament,
        'fields': {
            'Название': 'title',
            'Описание': 'description',
            'Начало': 'start',
            'Конец': 'end',
        },
        'primary_fields': {
            'Начало': 'start',
            'Конец': 'end',
        },
        'foreigns': None,
        'form_link': ['create_tournament', 'update_tournament'],
    },
    'Match': {
        'delete_page': 'match_delete',
        'entity_link': ['Матч', 'match'],
        'list_link': ['Матчи', 'matches'],
        'model': Match,
        'fields': {
            'Время проведения': 'match_date_time',
        },
        'primary_fields': {
            'Время проведения': 'match_date_time',
        },
        'foreigns': {
            'Команда 1': ['team1', 'team'],
            'Команда 2': ['team2', 'team'],
            'Место': ['place', 'place'],
            'Турнир': ['tournament', 'tournament'],
        },
        'form_link': ['create_match', 'update_match'],
    },
    'Place': {
        'delete_page': 'place_delete',
        'entity_link': ['Место', 'place'],
        'list_link': ['Места', 'places'],
        'model': Place,
        'fields': {
            'Название': 'title',
            'Адрес': 'address',
        },
        'primary_fields': {
            'Адрес': 'address',
        },
        'foreigns': None,
        'form_link': ['create_place', 'update_place'],
    },
    'Team': {
        'delete_page': 'team_delete',
        'entity_link': ['Команда', 'team'],
        'list_link': ['Команды', 'teams'],
        'model': Team,
        'fields': {
            'Название': 'title',
            'Дата основания': 'founding',
        },
        'primary_fields': {
            'Название': 'title',
        },
        'foreigns': None,
        'form_link': ['create_team', 'update_team'],
    },
}
