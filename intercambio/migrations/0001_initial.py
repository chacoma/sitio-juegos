# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idp', models.IntegerField(default=1)),
                ('instancia', models.IntegerField(default=1)),
                ('respuesta', models.FloatField(max_length=200)),
                ('confianza', models.IntegerField(default=1)),
                ('marcas', models.CharField(default='', max_length=500)),
                ('usuario', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DatosJugador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('edad', models.IntegerField(default=1)),
                ('estudio', models.IntegerField(default=1)),
                ('tiempo', models.DateTimeField(default=django.utils.timezone.now)),
                ('usuario', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Preguntas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
                ('resp_correcta', models.FloatField(max_length=200)),
                ('r1', models.IntegerField()),
                ('r2', models.IntegerField()),
                ('step', models.FloatField(default=1)),
                ('unit', models.CharField(default='km', max_length=10)),
                ('arch_img', models.CharField(default='intercambio/img/', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Puntajes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugador', models.CharField(max_length=20)),
                ('sc', models.CharField(max_length=100)),
                ('puntaje', models.IntegerField(default=0)),
                ('usuario', models.CharField(max_length=20)),
            ],
        ),
    ]
