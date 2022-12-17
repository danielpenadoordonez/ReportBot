import smtplib
import time
import smtplib
import getpass
from Clases.Publicador import Publicador
from BLL import PublisherProcess, SendEmail
from Services.Log import Log
from json.decoder import JSONDecodeError

PUBLICADOR = None
try:
    PUBLICADOR = PublisherProcess.ObtienePublicador()
except JSONDecodeError as err:
    print("Ocurrio un error")
    Log.critical(logName="user", message="No se puede cargar la informacion del publicador")
    Log.exception(logName="user", message=err)
    Log.info(logName="bot", message="SESION DE REPORTBOT CERRADA")
    exit()
except FileNotFoundError as err:
    print("Ocurrio un error")
    Log.critical(logName="user", message="No se puede cargar la informacion del publicador")
    Log.exception(logName="user", message=err)
    Log.info(logName="bot", message="SESION DE REPORTBOT CERRADA")
    exit()

#Se genera el codigo de seguridad
securityCode = PublisherProcess.generateSecurityCode()
Log.info(logName="user", message=f"Nuevo codigo de seguridad generado para cambiar la contraseña -> {securityCode}")
print("\n============= Se le enviará un código de seguridad a su correo =============")
try:
    SendEmail.load_Creds()
    #Se envia el codigo de seguridad por correo
    SendEmail.send_Security_Code(PUBLICADOR, securityCode)
except smtplib.SMTPAuthenticationError as err:
    print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
    Log.exception(logName="user", message=err)
    time.sleep(5)
except smtplib.SMTPException as err:
    print("Ocurrio un error al enviar el correo")
    Log.exception(logName="user", message=err)
    time.sleep(5)
except Exception as err:
    Log.exception(logName="user", message=err)
else:
    codeEntered = input("\nIngrese el código enviado a su correo: ")
    if PublisherProcess.isSecurityCodeCorrect(securityCode, codeEntered):
        #Si el codigo es correcto se le permite modificar la contraseña
        password = getpass.getpass("\n\tSU NUEVA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
        while password.isspace() or password == "":
            print("Por favor digite la contraseña")
            time.sleep(1)
            password = getpass.getpass("\n\tSU NUEVA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
        password = PublisherProcess.getHashPasswdHex(password)

        #Se actualiza el usuario
        PUBLICADOR.passwd = password
        PublisherProcess.EditaPublicador(PUBLICADOR)
        print("\n......Contraseña Guardada......")
        Log.info(logName="user", message=f"Se registro una nueva contraseña para {PUBLICADOR.nombreCompleto}")
        time.sleep(2)
        print("\nVuelva a abrir el programa para usar su nueva contraseña")
        time.sleep(2)
    else:
        #Si el codigo es incorrecto se informa y se cierra el programa
        print("\n¡¡¡¡Código de seguridad incorrecto, el programa se va cerrar!!!!")
        Log.warning(logName="user", message="El codigo de seguridad se ingreso incorrectamente en el programa")
        time.sleep(3)
finally:
    Log.info(logName="bot", message="SESION DE REPORTBOT CERRADA")
    exit()