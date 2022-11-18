import smtplib
import time
import smtplib
import getpass
from Clases.Publicador import Publicador
from BLL import PublisherProcess, SendEmail
from json.decoder import JSONDecodeError

PUBLICADOR = None
try:
    PUBLICADOR = PublisherProcess.ObtienePublicador()
except JSONDecodeError:
    print("Ocurrio un error")
    exit()
except FileNotFoundError:
    print("Ocurrio un error")
    exit()

#Se genera el codigo de seguridad
securityCode = PublisherProcess.generateSecurityCode()
print("\n============= Se le enviará un código de seguridad a su correo =============")
try:
    SendEmail.load_Creds()
    #Se envia el codigo de seguridad por correo
    SendEmail.send_Security_Code(PUBLICADOR, securityCode)
except smtplib.SMTPAuthenticationError:
    print("Error de autenticacion en el correo, contacte al desarrollador e informele de este error")
    time.sleep(5)
except smtplib.SMTPException:
    print("Ocurrio un error al enviar el correo")
    time.sleep(5)
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
        time.sleep(2)
        print("\nVuelva a abrir el programa para usar su nueva contraseña")
        time.sleep(2)
    else:
        #Si el codigo es incorrecto se informa y se cierra el programa
        print("\n¡¡¡¡Código de seguridad incorrecto, el programa se va cerrar!!!!")
        time.sleep(3)
finally:
    exit()