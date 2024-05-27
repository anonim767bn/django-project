from .models import *

PAGES = {
    'Tournament': {
        'entity_link': ['Турнир', 'tournament'],
        'list_link': ['Турниры', 'tournaments'],
        'model': Tournament,
        'fields': {
            'Название': 'title',
            'Описание': 'description',
            'Начало': 'start',
            'Конец': 'end'
        },
        'primary_fields': {
            'Название': 'title',
        },
        'foreigns': None
    },
    'Match': {
        'entity_link': ['Матч', 'match'],
        'list_link': ['Матчи', 'matches'],
        'model': Match,
        'fields': {
            'Время проведения': 'match_date_time',
        },
        'primary_fields': {
            'Время проведения': 'match_date_time'
        },
        'foreigns': {
            'Команда 1': ['team1_id', 'team'],
            'Команда 2': ['team2_id', 'team'],
            'Место': ['place_id', 'place'],
            'Турнир': ['tournament_id', 'tournament'],
        }
    },
    'Place': {
        'entity_link': ['Место', 'place'],
        'list_link': ['Места', 'places'],
        'model': Place,
        'fields': {
            'Название': 'title',
            'Адрес': 'address',
        },
        'primary_fields': {
            'Название': 'title',
        },
        'foreigns': None
    },
    'Team': {
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
        'foreigns': None
    },
}
