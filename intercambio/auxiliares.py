# -*- coding: utf-8 -*-

CANT_REF= 12
NRO_PREG= 5
PJE_MAX= NRO_PREG*200

# MARCAS -----------------------------------------------------------------------
from scipy.stats import truncnorm # gaussianas truncadas a un rango
import random

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def set_marcas(resp_ini,r1,r2,step):

	ran= random.random()

	if ran<0.33:
		marcas= random.sample(range(r1,r2),CANT_REF)

	elif ran>=0.33 and ran<0.66:
		#a= (r2-r1)*0.25 + r1
		#marcas= [int(random.gauss(a, (a-r1)*0.3)) for i in range(10)]
		scale = (r2-r1)*0.25
		a = r1
		b = r1+ (r2-r1)*0.5

		marcas = get_truncated_normal(mean=r1+scale, sd=scale, low=a, upp=b).rvs(CANT_REF)
		marcas = marcas.round().astype(int)

		#print r1, r2
		#print a,b, scale
		#print marcas

	elif ran>=0.66 and ran<1:
		#b= r2- (r2-r1)*0.25
		#marcas= [int(random.gauss(b, (r2-b)*0.3)) for i in range(10)]
		scale = (r2-r1)*0.25
		b = r2
		a = r1+ (r2-r1)*0.5
		size = 10

		marcas = get_truncated_normal(mean=r2-scale, sd=scale, low=a, upp=b).rvs(CANT_REF)
		marcas = marcas.round().astype(int)

		#print r1, r2
		#print a,b, scale
		#print marcas

	# transformacion a porcentajes
	marcas_porc= [ str((marca-r1)*100.0/(r2-r1))+'%' for marca in marcas]


	return marcas_porc



# PUNTAJE ----------------------------------------------------------------------
def get_puntaje(resp, conf, correcta):

    # 1er intervalo de certeza
    if resp> correcta*0.99 and resp< correcta*1.01:
        if conf==2:
            return ["100+100",200]
        elif conf==1:
            return ["100+10",110]
        elif conf==0:
                return ["100+1",101]

    # 2do intervalo de certeza
    elif resp> correcta*0.9 and resp< correcta*1.1:
        if conf==2:
            return ["10+10",20]
        elif conf==1:
            return ["10+100",110]
        elif conf==0:
                return ["10+10",20]

    #3er intervalo de certeza
    elif resp> 0 and resp< correcta*2:
        if conf==2:
            return ["10+10",20]
        elif conf==1:
            return ["10+100",110]
        elif conf==0:
                return ["10+10",20]

    else:
        return ["0", 0]

import hashlib

def get_puntaje_final(jugador, puntaje_total):

    acu=0
    for elem in puntaje_total:
        acu+=elem[1]

    #genero hash

    h=hashlib.sha1()
    h.update("%s"% jugador)

    # porcentaje de puntaje respecto al maximo
    porc= acu*100.0/PJE_MAX

    return {'porc':porc,'hash':h.hexdigest(),'jugador': jugador, 'total':acu, 'data':puntaje_total}


# CERTIIFICADO PDF -------------------------------------------------------------

from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm

def get_certificado(datos, response):

    p = canvas.Canvas(response)

    # Draw things on the PDF.
    p.setFont("Courier", 18)
    p.drawString(50, 725, "Intercambio y manejo de Información")
    p.setFont("Courier", 14)
    p.drawString(50, 700, "Certificado de participación")
    p.setFont("Courier", 30)
    p.drawString(50, 650, "%s"%datos['jugador'])
    p.drawString(50, 600, "%s puntos"%datos['puntaje'])

    # codigo de barra
    barcode=code39.Extended39("%s"% datos['jugador'].split('.')[1],barWidth=0.5*mm,barHeight=20*mm)
    barcode.drawOn(p,30,480)
    #hash
    p.setFont("Courier", 20)
    p.drawString(50, 420, "%s"%datos['hash'])

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
