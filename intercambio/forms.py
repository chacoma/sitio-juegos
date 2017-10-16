# -*- coding: utf-8 -*-

from django import forms
#import floppyforms as forms
from django.core.validators import MaxValueValidator, MinValueValidator

OPCIONES= (('1','Cs Exáctas'),('2','Ingeniería'),('3','Cs Sociales'),('4','Cs Económicas'),('5','Otra'))

class FormJugador(forms.Form):

	nombre	= forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), required= True )
	edad	= forms.IntegerField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), required= True, validators=[MaxValueValidator(99), MinValueValidator(0)])
	estudio = forms.ChoiceField(widget=forms.Select, choices=OPCIONES)
