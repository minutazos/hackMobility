#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cozmo
import math
import csv,operator
from xml.dom import minidom
import xml.etree.ElementTree as ET

def leerCsv(data):
    # Leer un archivo csv como lista de diccionarios con DictReader() y
    # mostrar sólo datos de algunas columnas:

    root = ET.parse(data)
    entries = root.findall("body/precioseessterrestres/listaeessprecio/eessprecio")
    content = ""
    i = 0
    sids = []
    direccions = []
    for entry in entries:
        sid = entry.find("codigoPostal").text
        print("hi")
        sids.append(sid)
        direccion = entry.find("dir")
        direccions.append(direccion)
        latitud = entry.find("latitud")
        longitud = entry.find("longitud_x0020__x0028_wgs84_x0029_")
        ++i

    i = 0
    for entry in entries:
        print("c.p.:%s " % sids[i].data)
        print("dirección: %s" % direccions[i].firstChild.data)
        print("latitud:%s" % latitud.firstChild.data)
        print("longitud:%s \n" % longitud.firstChild.data)
        ++i

leerCsv("files/petrol.xml")

class coche:
    pos = []
    oil = 0
    nearStations = []
    to = []
    stationsOnWay = []

class petrolStation:
    name = ""
    pos = []
    streetAddress = ""
    postalCode = ""
    stationBrand = ""
    diesel = ""
    dieselA = ""
    petrol95 = ""
    petrol98 = ""
    naturalGasComp = ""
    naturalGasLiq = ""
    schedule = ""
    timestamp = ""

def ordenarLista():
    return

def getStations():
    return

def getStationsOnWay():
    return




def calcularDist(myPos,stPos):
    return math.sqrt(math.pow(myPos[0]-stPos[0],2) + math.pow(myPos[1]-stPos[1],2))
