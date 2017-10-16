# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now


class DatosJugador(models.Model):

	nombre	= models.CharField(max_length=20)
	edad	= models.IntegerField(default=1)
	estudio = models.IntegerField(default=1)
	tiempo	= models.DateTimeField(default=now)
	usuario	=  models.CharField(max_length=20)

class Puntajes(models.Model):

	jugador = models.CharField(max_length=20)
	sc		= models.CharField(max_length=100)
	puntaje	= models.IntegerField(default=0)
	usuario=  models.CharField(max_length=20)
	tf = models.CharField(max_length=50,default=str(now))


class Preguntas(models.Model):

	idp =  models.IntegerField(default=1)
	texto= models.CharField(max_length=200)
	resp_correcta= models.FloatField(max_length=200)

	r1= models.IntegerField()
	r2= models.IntegerField()
	step= models.FloatField(default=1)
	unit= models.CharField(max_length=10,default='km')
	arch_img= models.CharField(max_length=20, default='intercambio/img/')

class Datos(models.Model):

	idp =  models.IntegerField(default=1)
	instancia= models.IntegerField(default=1)
	respuesta = models.FloatField(max_length=200)
	confianza = models.IntegerField(default=1)
	marcas= models.CharField(max_length=500,default='')
	usuario=  models.CharField(max_length=20)
