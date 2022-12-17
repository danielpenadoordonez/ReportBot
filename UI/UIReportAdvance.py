import time
from Clases.Informe import Informe
from BLL import DiaProcess
from BLL import SendEmail
from BLL import GoalProcess
from BLL import PublisherProcess
from Services.Log import Log
from json.decoder import JSONDecodeError
import smtplib

def load_UIReportAdvance():
    PUBLICADOR = None
    try:
        PUBLICADOR = PublisherProcess.ObtienePublicador()
    except JSONDecodeError as err:
        print("Ocurrio un error, el programa se va cerrar")
        Log.critical(logName="user", message="No se puede cargar la informacion del publicador")
        Log.exception(logName="user", message=err)
        Log.info(logName="bot", message="SESION DE REPORTBOT CERRADA")
        time.sleep(3)
        exit()
    except FileNotFoundError as err:
        print("Ocurrio un error")
        Log.critical(logName="user", message="No se puede cargar la informacion del publicador")
        Log.exception(logName="user", message=err)
        Log.info(logName="bot", message="SESION DE REPORTBOT CERRADA")
        time.sleep(3)
        exit()


    avance = Informe()
    try:
        #Se cargan los dias registrados hasta la fecha con sus respectivos datos
        avance.carga_Dias()
    except JSONDecodeError:
        print("No cuenta con datos registrados para generar un avance")
        time.sleep(3)
    except FileNotFoundError:
        print("No cuenta con datos registrados para generar un avance")
        time.sleep(3)
    else:
        horas = avance.getTotalHoras()
        publicaciones = avance.getTotalPublicaciones()
        revisitas = avance.getTotalRevisitas()
        videos = avance.getTotalVideos()
        diasAvance = avance.getTotalDias()
        

        print("-"*12 + "Creando Avance" + "-"*12)
        time.sleep(2)
        print(avance.construyeAvance())
        dictAvance = {"Horas" : horas, "Publicaciones" : publicaciones, "Revisitas" : revisitas, "Videos" : videos, "Dias" : diasAvance}
        #Se cargan Mis Metas
        misMetas = list()
        try:
            misMetas = GoalProcess.cargar_Mis_Metas()
        except JSONDecodeError:
            pass
        except FileNotFoundError:
            pass
        #Se envia el avance por correo
        try:
            SendEmail.load_Creds()
            SendEmail.envia_Avance(dictAvance, misMetas, PUBLICADOR)
            Log.info(logName="advance-report", message=f"Avance enviado -> Horas: {horas}, Publicaciones: {publicaciones}, Videos: {videos}, Revisitas: {revisitas}, Dias Informados: {diasAvance}")
            print("El Avance ha sido creado y enviado")
        except smtplib.SMTPAuthenticationError:
            print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
            Log.exception(logName="advance-report", message=err)
        except smtplib.SMTPException:
            print("Ocurrio un error al enviar el correo")
            Log.exception(logName="advance-report", message=err)
        except Exception as err:
            print("Ocurrio un error al enviar el correo, revise su conexión a Internet")
            Log.exception(logName="advance-report", message=err)
        time.sleep(5)