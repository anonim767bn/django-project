# Generated by Django 5.0.3 on 2024-04-25 18:03

import django.db.models.deletion
import tournaments.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True, verbose_name='title')),
                ('founding', models.DateField(blank=True, null=True, validators=[tournaments.models.check_founding], verbose_name='founding')),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
                'db_table': '"tournament"."team"',
                'ordering': ['founding'],
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('start', models.DateField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateField(blank=True, null=True, verbose_name='end')),
            ],
            options={
                'verbose_name': 'tournament',
                'verbose_name_plural': 'tournaments',
                'db_table': '"tournament"."tournament"',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='TournamentTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.team', verbose_name='team id')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament', verbose_name='tournament id')),
            ],
            options={
                'verbose_name': 'relationship tournament team',
                'verbose_name_plural': 'relationships tournament teams',
                'db_table': '"tournament"."tournament_team"',
                'ordering': ['tournament'],
                'unique_together': {('tournament', 'team')},
            },
        ),
        migrations.AddField(
            model_name='tournament',
            name='teams',
            field=models.ManyToManyField(through='tournaments.TournamentTeam', to='tournaments.team', verbose_name='teams'),
        ),
        migrations.AddField(
            model_name='team',
            name='tournaments',
            field=models.ManyToManyField(through='tournaments.TournamentTeam', to='tournaments.tournament', verbose_name='tournaments'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('place', models.TextField(blank=True, null=True, verbose_name='place')),
                ('match_date_time', models.DateTimeField(blank=True, null=True, verbose_name='match date and time')),
                ('team_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mathces_as_team_1', to='tournaments.team', verbose_name='team 1')),
                ('team_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mathces_as_team_2', to='tournaments.team', verbose_name='team 2')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament', verbose_name='tournament id')),
            ],
            options={
                'verbose_name': 'match',
                'verbose_name_plural': 'matches',
                'db_table': '"tournament"."match"',
                'ordering': ['tournament'],
                'unique_together': {('tournament', 'team_1', 'team_2')},
            },
        ),
    ]