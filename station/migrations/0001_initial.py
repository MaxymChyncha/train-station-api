# Generated by Django 5.0.3 on 2024-03-23 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=63)),
                ('last_name', models.CharField(max_length=63)),
                ('position', models.CharField(choices=[('station_master', 'Master Station'), ('train_driver', 'Train Driver'), ('ticket_inspector', 'Ticket Inspector'), ('platform_attendant', 'Platform Attendant'), ('train_dispatcher', 'Train Dispatcher'), ('security_guard', 'Security Guard'), ('cleaning_staff', 'Cleaning Staff'), ('other', 'Other')], max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'verbose_name': 'Train Type',
                'verbose_name_plural': 'Train Types',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.PositiveIntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_routes', to='station.station')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_routes', to='station.station')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('cargo_num', models.PositiveIntegerField()),
                ('places_in_cargo', models.PositiveIntegerField()),
                ('train_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trains', to='station.traintype')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='station.route')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='station.train')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.PositiveIntegerField()),
                ('seat', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='station.order')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='station.trip')),
            ],
            options={
                'ordering': ['cargo', 'seat'],
                'unique_together': {('trip', 'cargo', 'seat')},
            },
        ),
    ]
