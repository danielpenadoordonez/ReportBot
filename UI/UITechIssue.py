from Services.Log import Log
from BLL import SendEmail
import smtplib
import time

def load_UITechIssue(publicador):
    #Se pide una descripcion del issue
    print("="*50)
    issue_Description = input("DESCRIBA EL PROBLEMA TÉCNICO QUE ESTÁ TENIENDO: ")
    Log.warning(logName="bot", message=f"PROBLEMA TÉCNICO: {issue_Description}")
    log_Files = list()
    try:
        Log.info(logName="bot", message="Cargando logs para enviarlos al desarrollador")
        print("\nCargando logs para enviarlos al desarrollador.........................................")
        log_Files = Log.get_Log_Files()
        Log.info(logName="bot", message="Logs cargados correctamente")
        time.sleep(2)
    except Exception as err:
        print("Ocurrió un error al cargar los logs!!")
        Log.error(logName="bot", message="Ocurrió un error al cargar los logs")
        Log.exception(logName="bot", message=err)

    try:
        SendEmail.load_Creds()
        SendEmail.send_TechIssue_Email(publicador, issue_Description, log_Files)
        print("\n\t¡Se ha enviado la informacion al desarrollador para que revise el problema!")
        time.sleep(2)
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
        Log.exception(logName="bot", message=err)
    except smtplib.SMTPException:
        print("Ocurrio un error al enviar el correo")
        Log.exception(logName="bot", message=err)
    except Exception as err:
        print("Ocurrio un error al enviar el correo, revise su conexión a Internet")
        Log.exception(logName="bot", message=err)