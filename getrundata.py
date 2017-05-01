#! /usr/bin/python

import urllib, urllib2
import json
import time
import xml.etree.ElementTree as ET

def getrundv(r):
	
	multiplo = 2
	total = 0
	for reverso in reversed(r):
		total += int(reverso) * multiplo

		if multiplo == 7:
		    multiplo = 2
		else:
		    multiplo += 1

		modulus = total % 11

	verificador = 11 - modulus

	if verificador == 10:
	    div = "K"
	elif verificador == 11:
	    div = "0"
	else:
	    if verificador < 10:
		div = verificador

	return str(div)

def getnombre(r):
	url    = 'http://rutificador.cl/informacion/datos/empresas-personas-rut-nombre/dotsvt'
	values = {'rut_or_name':r,'entity':'persona','entity':'empresa','box':'BOGetRutificadorXML','type':'0' }

	data   = urllib.urlencode(values)
	req    = urllib2.Request(url,data)

	req.add_header("Content-type", "application/x-www-form-urlencoded;")
	req.add_header("Content-Length", str(len(data)))
	req.add_header("Cookie", "JSESSIONID=2C7C903401EBD1B8EAC62D9B9147875D")
	

	response = urllib2.urlopen(req)

	x = response.read()    
	root = ET.fromstring(x)

	for r in root.iter('registers'):
		if r.text == '1':
			for f in root.iter('field'):
				x = f.text
				return x
		else:
			return ""

	

def getescencosud(rdv):
	url = 'https://www.puntosuerte.cl/saveRut.php'
	values = {'rut': rdv}
	
	data   = urllib.urlencode(values)
	req    = urllib2.Request(url,data)

	req.add_header("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")
	req.add_header("Content-Length", str(len(data)))
	req.add_header("Cookie", "PHPSESSID=61d4764f3adff0d47536849e7c33ec6c;")
	

	response = urllib2.urlopen(req)

	x = response.read()    
	if x == 'Exito_viejo':
		return "1"

	return "0"


#############################################################
# Incoporar titulo en variable y nueva columna en una funcion
#
print("\nRUNDATA v1.0 - www.incode.cl\n")
print("\nObteniendo datos desde el RUN 1.000.000 al 25.000.000...\n")

f = open("datos-por-run-" + time.strftime("%d%m%Y%H%M%S") + ".csv","w")

titulos = "RUT;DV;NOMBRE;ES_CLIENTE_CENCOSUD\n"

f.write(titulos)


for run in range(1000000,25000000):
#run = "1000005"
	runx = str(run)
	f.write(runx + ";")

	dv = getrundv(runx)
	f.write(dv + ";")

	n =  getnombre(runx + "-" + dv)
	f.write(n + ";")

	c = getescencosud(runx + "-" + dv)
	f.write(c + ";\n")


f.close()
print ("\nDatos descargados correctamente. Tarea finalizada.\n")
