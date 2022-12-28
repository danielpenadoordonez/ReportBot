from DAL import File
from Clases.Dia import Dia
from datetime import datetime
from Services.Log import Log

daysRegistered = list()

def carga_Dias_Registrados():
    'Carga los dias que esten guardados en el JSON'
    global daysRegistered
    daysRegistered = []
    for day in File.ObtieneDiasRegistrados():
        dia = Dia()
        dia.month = day['month']
        dia.horas = day['horas']
        dia.revisitas = day['revisitas']
        dia.publicaciones = day['publicaciones']
        dia.videos = day['videos']
        dia.fecha = day['fecha']
        daysRegistered.append(dia)
    return daysRegistered

def GuardaDatos(dia):
    daysRegistered.append(dia)
    File.GuardaDatos(daysRegistered)

def EliminaDatos():
    File.EliminaDatos()
    Log.warning(logName="daily-data", message="Todas los datos diarios han sido borrados")

def same_Month():
    'Retorna True si el mes actual es el mismo que tienen los datos en DatosMes.json'
    currentMonth = datetime.strptime(str(datetime.now().month), "%m").strftime("%B").upper()
    #Si el mes actual es igual al que tienen los dias registrados
    return currentMonth == daysRegistered[0].month
