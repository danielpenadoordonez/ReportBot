import time
from Clases.Informe import Informe
from BLL import DiaProcess
from BLL import SendEmail
from BLL import GoalProcess
from BLL import PublisherProcess
from json.decoder import JSONDecodeError
import smtplib

PUBLICADOR = None
try:
    PUBLICADOR = PublisherProcess.ObtienePublicador()
except JSONDecodeError:
    print("Ocurrio un error, el programa se va cerrar")
    time.sleep(3)
    exit()
except FileNotFoundError:
    print("Ocurrio un error")
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
        print("El Avance ha sido creado y enviado")
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
    except smtplib.SMTPException:
        print("Ocurrio un error al enviar el correo")
    time.sleep(5)