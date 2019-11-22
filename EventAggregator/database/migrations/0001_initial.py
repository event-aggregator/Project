# Generated by Django 2.2.5 on 2019-11-22 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EventLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Events')),
                ('language_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Languages')),
            ],
        ),
        migrations.CreateModel(
            name='EventCities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Cities')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Events')),
            ],
        ),
        migrations.CreateModel(
            name='EventAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Areas')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Events')),
            ],
        ),
        migrations.CreateModel(
            name='ClientLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Languages')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('events_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Events')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientCities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Cities')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Areas')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
    ]
