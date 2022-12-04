from urllib.parse import ParseResultBytes
from DAL import File
from Clases.Meta import Meta
from datetime import datetime
import calendar

goalList = list()

def cargar_Mis_Metas():
    'Carga las metas guardadas y las guarda en una lista'
    global goalList
    goalList = []
    myGoals = File.ObtieneMetasJSON()
    for goal in myGoals:
        meta = Meta()
        meta.nombre = goal['nombre']
        meta.cantidad = goal['cantidad']
        meta.descripcion = goal['descripcion']
        meta.tipo = goal['tipo']
        meta.fechaRegistro = goal['fechaRegistro']
        meta.id = goal['id']
        goalList.append(meta)
    return goalList

def meta_Existe(meta):
    'Verifica que el tipo de meta no este ya registrado'
    for goal in goalList:
        if meta.tipo == goal.tipo:
            return True
    return False

def meta_Alcanzada(meta, informe) -> bool:
    'Retorna True si la meta se alcanzo, de lo contrario retorna False'
    #Se tiene que buscar que tipo de meta es para llamar a la funcion respectiva
    #en la clase Informe
    #El parametro informe es un diccionario con los resultados del informe
    return informe[meta.tipo] >= meta.cantidad

def calcula_Progreso_Meta(meta, avance) -> dict:
    currentDate = datetime.now()
    diaActual = currentDate.day
    #Funcion interna para obtener el total de dias que tiene el mes actual
    def total_Dias_Mes_Actual():
        return calendar.monthrange(currentDate.year, currentDate.month)[1]

    porcentajeDias = diaActual / total_Dias_Mes_Actual()
    cantidadEsperada = porcentajeDias * meta.cantidad
    sobranteFaltante = avance[meta.tipo] - cantidadEsperada
    try:
        porcentajeLogro = avance[meta.tipo] / round(cantidadEsperada)
    except ZeroDivisionError:
        porcentajeLogro = 0
    
    valores = dict()
    valores['CantActual'] = avance[meta.tipo]
    valores['CantEsperada'] = round(cantidadEsperada)
    valores['SobranteFaltante'] = round(sobranteFaltante)
    valores['PorcLogro'] = round(porcentajeLogro * 100)
    return valores

#Funciones que se encargan de la persistencia
def GuardaMetaJSON(meta):
    'Incluye la nueva meta en la lista de metas y en el archivo JSON'
    goalList.append(meta)
    File.GuardaMetaJSON(goalList)

def EliminaMeta(id):
    #Se busca cual meta tiene el ID enviado y se elimina de la lista
    for i in range(0, len(goalList)):
        if goalList[i].id == id:
            del goalList[i]
            #Se tiene que actualizar el archivo JSON
            File.GuardaMetaJSON(goalList)  

def BorraJSONMetas():
    File.BorraJSONMetas()

