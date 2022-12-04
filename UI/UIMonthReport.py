import time
from Clases.Informe import Informe
from BLL import DiaProcess
from BLL import SendEmail
from BLL import GoalProcess
from BLL import PublisherProcess
from json.decoder import JSONDecodeError
import smtplib

def load_UIMonthReport():
    PUBLICADOR = None
    try:
        PUBLICADOR = PublisherProcess.ObtienePublicador()
    except JSONDecodeError:
        print("Ocurrio un error")
        exit()
    except FileNotFoundError:
        print("Ocurrio un erro")
        exit()

    #Primero se tiene que verificar que el mes haya terminado para generar el informe
    try:
        DiaProcess.carga_Dias_Registrados()
        if DiaProcess.same_Month():
            print("Este mes no ha terminado, debe esperar a que concluya para enviar el informe")
            time.sleep(5)
    except JSONDecodeError:
        print("No cuenta con datos registrados para crear y enviar el informe")
        time.sleep(3)
    except FileNotFoundError:
        print("No cuenta con datos registrados para crear y enviar el informe")
        time.sleep(3)
    else:
        #Se tiene que solicitar la cantidad de estudios que dirigio en el mes
        estudios = 0
        invalidData = True
        while invalidData:
            try:
                estudios = int(input("\tESTUDIOS: "))
                invalidData = False
            except ValueError:
                print("Todos los datos se debe ingresar con numeros")
        informe = Informe(estudios)
        #Se cargan los dias registrados con sus respectivos datos
        Informe.carga_Dias()

            #Se traen los totales para mandarlos a la tabla HTML para el correo
        horasInf = informe.getTotalHoras()
        publicacionesInf = informe.getTotalPublicaciones()
        videosInf = informe.getTotalVideos()
        revisitasInf = informe.getTotalRevisitas()
        diasInf = informe.getTotalDias()
            
        informe = informe.construyeInforme()
        print("-"*12 + "Creando Informe" + "-"*12)
        time.sleep(3)
        #Se muestra el informe en consola 
        print(informe)
            
        #Se envia por correo a mi mismo y al que recoge los informes
        dictInforme = {"Horas": horasInf, "Publicaciones": publicacionesInf, "Videos" : videosInf, "Revisitas" : revisitasInf, "Estudios" : estudios, "Dias" : diasInf}
        try:
            SendEmail.load_Creds()
            SendEmail.envia_Informe_Por_Correo(dictInforme, PUBLICADOR)
            try:
                goalList = GoalProcess.cargar_Mis_Metas()
                time.sleep(1)
                SendEmail.envia_Reporte_Metas(goalList, dictInforme, PUBLICADOR)
            except JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
            #Se elimina el contenido del archivo con los datos para que se pueda volver a usar
            DiaProcess.EliminaDatos()
            #Se confirma que el proceso se hizo de manera exitosa
            print("El Informe ha sido creado y enviado")
        except smtplib.SMTPAuthenticationError:
            print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
        except smtplib.SMTPException:
            print("Ocurrio un error al enviar el correo")
        time.sleep(5)