import time
from Clases.Dia import Dia
from BLL import DiaProcess
from Services.Log import Log
from json.decoder import JSONDecodeError

def load_UIDatosDia():
    sent_Previous_Month_Report = True
    try:
        #Se cargan los dias registrados
        DiaProcess.carga_Dias_Registrados()
    except JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    else:
        #Si empezó un nuevo mes y el usuario no ha enviado el informe del mes anterior 
        #entonces no puede ingresar datos del nuevo mes
        if not DiaProcess.same_Month():
            print("No ha enviado el informe del mes anterior, para ingresar nuevos datos debe primero enviar el informe anterior")
            Log.error(logName="daily-data", message="No se pueden registrar datos en DatosMes.json, Causa -> No se ha enviado el informe")
            sent_Previous_Month_Report = False
            time.sleep(2)
    finally:
        if sent_Previous_Month_Report: #Si ya se envio el informe del mes anterior
            #Se solicitan los datos para registrarlos en el archivo
            horas = revisitas = publicaciones = videos = 0
            invalidData = True
            while invalidData:
                try:
                    horas = int(input("\tHORAS: "))
                    publicaciones = int(input("\tPUBLICACIONES: "))
                    revisitas = int(input("\tREVISITAS: "))
                    videos = int(input("\tVIDEOS: "))
                    invalidData = False
                except ValueError:
                    print("Todos los datos se deben ingresar con numeros")
            #Se construye el dia con su informacion para guardarlo en el archivo
            dia  = Dia(horas, revisitas, publicaciones, videos)
            DiaProcess.GuardaDatos(dia)
            Log.info(logName="daily-data", message=f"Registro de datos -> Horas: {dia.horas}, Revisitas: {dia.revisitas}, Publicaciones: {dia.publicaciones}, Videos: {dia.videos}")
            print("\n\t¡Datos Guardados!")
            time.sleep(2)    