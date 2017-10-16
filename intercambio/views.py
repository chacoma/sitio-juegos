# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import FormJugador
from .models import DatosJugador, Preguntas, Datos, Puntajes

import time,random, hashlib
from auxiliares import *


# Vistas ----------------------------------------------------------------------
def inicio(request):
    return render(request, 'intercambio/index.html', {})

def intercambio_index(request):
	return render(request, 'intercambio/intercambio_index.html', {})

@csrf_exempt
def registro(request):

    if request.method== 'POST':

        form_jugador= FormJugador(request.POST)

        if form_jugador.is_valid():

            datos= form_jugador.cleaned_data

            nombre= datos.get("nombre")
            edad= datos.get("edad")
            estudio=  datos.get("estudio")
            usuario = str(time.time())
            tiempo= time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())  # en formato timefield
            # print datos, tiempo
            # print NRO_PREG


            # Guardo los datos del usuario
            db= DatosJugador()
            db.nombre	= nombre
            db.edad	= edad
            db.estudio	= estudio
            db.usuario	= usuario
            db.save()


            # Seteo de Variables globales
            request.session.clear()
            request.session['user']=usuario
            request.session['jugador'] = nombre + '.' +usuario
            request.session['Npreg']=1

            request.session['puntaje_total']=[]

            request.session['flag']=0
            # seteo un vector aux con los ordenes de preguntas
            request.session['preguntas_orden']= [i for i in range(NRO_PREG)]
            #elijo la  pregunta
            request.session['idp']= random.choice(request.session['preguntas_orden'])
            #elimino la pregunta que saque
            request.session['preguntas_orden'].remove(request.session['idp'])

            # tomo las preguntas de la db
            preg= Preguntas.objects.values()
            request.session['preguntas']= list(preg)

            return HttpResponseRedirect('/intercambio/preguntas/1/', {})


    else:
        form_jugador= FormJugador()


    return render(request, 'intercambio/registro.html', {"form":form_jugador})

@csrf_exempt
def preguntas(request):

    if request.method== 'POST':

        # Recupero los datos ingresados
        datos= request.POST
        # print datos

        # ESTOS DATOS SE CORRESPONDEN A LA RESPUESTA SIN INFLUENCIA
        db= Datos()
        db.usuario= 	request.session['user']
        db.idp= 	request.session['idp']+1
        db.instancia= 1
        db.respuesta= datos['resp']
        db.confianza= datos['conf']
        db.marcas= ''
        db.save()
        #------------------------------------------------------------

        # guardo la respuesta que dio para setear la ronda 2
        request.session['resp_ini']= datos['resp']
        request.session['conf_ini']= datos['conf']
        request.session['flag']=1


        # redirijo a la vista donde seteo las marcas
        return HttpResponseRedirect('/intercambio/preguntas/2/', {})


    else:
        # Tomo los datos de la pregunta para el render
        data= request.session['preguntas'][request.session['idp']]

        #Agrego datos iniciales de las barras
        data['resp_ini']= random.randint(data['r1'],data['r2'])
        data['conf_ini']= random.randint(0,2)

        #tomo el nro de pregunta de la var global
        data['Npreg']= request.session['Npreg']
        print "data en get", data

        return render_to_response('intercambio/preguntas.html', data)

@csrf_exempt
def preguntas2(request):

    if request.method== 'POST':

        datos= request.POST
        # print datos

        # ESTOS DATOS SE CORRESPONDEN A LA RESPUESTA CON INFLUENCIA
        db= Datos()
        db.usuario= 	request.session['user']
        db.idp= 	request.session['idp']+1
        db.instancia= 2
        db.respuesta= float(datos['resp'])
        db.confianza= int(datos['conf'])

        db.marcas= ''.join(datos.getlist('marcas'))
        db.save()

        #------------------------------------------------------------


        # Aca todo lo asociado al cambio de pregunta --------------------------
        request.session['Npreg']+=1	#incremento nro de pregunta

        #puntaje
        puntaje= get_puntaje(float(datos['resp']), int(datos['conf']), float(datos['correcta']))

        request.session['puntaje_total'].append(puntaje)

        if request.session['preguntas_orden']:
        	#elijo la  pregunta
        	request.session['idp']= random.choice(request.session['preguntas_orden'])
        	#elimino la pregunta que saque
        	request.session['preguntas_orden'].remove(request.session['idp'])
        	return HttpResponseRedirect('/intercambio/preguntas/1/', {})

        else:
            data= request.session['puntaje_total']
            return HttpResponseRedirect('/intercambio/puntaje/', data)


    else:

        # Tomo los datos de la pregunta para el render
        data= request.session['preguntas'][request.session['idp']]

        #Agrego datos iniciales de las barras
        data['resp_ini']= request.session['resp_ini']
        data['conf_ini']= request.session['conf_ini']

        #tomo el nro de pregunta de la var global
        data['Npreg']= request.session['Npreg']

        # Agrego las marcas de informacion
        if request.session['flag']==1:
            data['marcas'] =set_marcas(request.session['resp_ini'], data['r1'], data['r2'], data['step'])
            #data['marcas'] =['0%','50%','60%','100%']

        request.session['flag']=2

        #print "datos en get de 2", data
        return render_to_response('intercambio/preguntas.html', data)

@csrf_exempt
def final(request):

    if request.method== 'POST':

        datos= request.POST
        #print datos
        #guardo datos en base de datos
        db= Puntajes()
        db.usuario	    = datos['jugador'].split(".")[1]+datos['jugador'].split(".")[2]
        db.jugador	= datos['jugador']
        db.sc	    = datos['hash']
        db.puntaje	= datos['puntaje']
        db.tf	= str(time.time())
        db.save()

        #armado del pdf como comprobante
        response = HttpResponse(content_type ='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=puntuacion.pdf'

        get_certificado(datos, response)

        return response

    else:

        # calculo el puntaje total
        data_pjeFinal= get_puntaje_final(request.session['jugador'],request.session['puntaje_total'])

        #elimina las Variables sessio para que el user no pueda volver
        request.session.flush()

        return render_to_response('intercambio/final.html', data_pjeFinal)


def probar(request):
    return render(request, 'intercambio/probar.html', {})

def reglamento(request):
    return render(request, 'intercambio/reglamento.html', {})
