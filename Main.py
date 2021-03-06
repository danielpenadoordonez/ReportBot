import smtplib
import time
from BLL import PublisherProcess
from json.decoder import JSONDecodeError
import getpass


#Se tiene que traer el publicador usuario, si no existe se tiene que registrar
#Para hacer el registro se llama a CreatePublisher
PUBLICADOR = None
try:
    PUBLICADOR = PublisherProcess.ObtienePublicador()
except JSONDecodeError:
    import UI.CreatePublisher
    exit()
except FileNotFoundError:
    import UI.CreatePublisher
    exit()

#Se tiene que pedir la clave para ingresar y si no tiene clave tiene que ingresar una
savedPassword = PUBLICADOR.passwd
try:
    #Se verifica si el usuario tiene clave y que el hash este correcto
    assert savedPassword != None and len(savedPassword) == 64
    loginpassword = getpass.getpass("\nContraseña: ", stream=None)
    fails = 0
    #Mientras la contraseña no sea valida
    while not PublisherProcess.isPasswdCorrect(savedPassword, loginpassword):
        print("\tContraseña Incorrecta")
        fails += 1
        time.sleep(1)
        #Al tercer fallo
        if fails == 3:
            #Se le pregunta al usuario si desea recuperar su contraseña
            userAnswer = input("\nDesea recuperar su contraseña (Si/No)> ").capitalize()
            answerOptions = ["Si", "No"]
            while userAnswer not in answerOptions:
                print("\tOpcion Invalida")
                time.sleep(1)
                userAnswer = input("\nDesea recuperar su contraseña (Si/No)> ").capitalize()

            #Si el usuario solicita el cambio de contraseña se tiene que llamar el modulo que lo hace
            if userAnswer == "Si":
                import UI.ChangePass
            else:    
                exit()
        loginpassword = getpass.getpass("\nContraseña: ", stream=None)

except AssertionError:
    print("\nUsted no tiene contraseña")
    time.sleep(1)
    #Se le tiene que pedir al usuario que registre una contraseña
    password = getpass.getpass("\n\tDIGITE UNA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
    while password.isspace() or password == "":
        print("Por favor digite una contraseña")
        time.sleep(1)
        password = getpass.getpass("\n\tDIGITE UNA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
    password = PublisherProcess.getHashPasswdHex(password)
    
    #Se actualiza el usuario
    PUBLICADOR.passwd = password
    PublisherProcess.EditaPublicador(PUBLICADOR)
    print("......Contraseña Guardada......")
    time.sleep(2)
    print("\nVuelva a abrir el programa para usar su nueva contraseña")
    time.sleep(2)
    exit()

opcion = input(f"""
 ______    ______    _______    _______    _______    _________          ______     ______   __________ 
|      |  |         |       |   |      |   |      |       |             |      |   |      |      |   
|      |  |         |       |   |      |   |      |       |             |      |   |      |      |
|______|  |______   |_______|   |      |   |______|       |             |______|   |      |      |
|\\        |         |           |      |   |\\             |             |      |   |      |      |
| \\       |         |           |      |   | \\            |             |      |   |      |      |
|  \\      |______   |           |______|   |  \\           |             |______|   |______|      | 
                                      
Hola {PUBLICADOR.nombreCompleto}

==========================================
|  QUE DESEA HACER                       |
|----------------------------------------| 
|   1. INGRESAR DATOS DEL DIA            |
|   2. GENERAR Y ENVIAR INFORME DEL MES  |
|   3. VER AVANCE ACTUAL                 |
|   4. METAS MENSUALES                   |
|   5. EDITAR DATOS DE PUBLICADOR        |
|   6. SALIR                             |
==========================================\n>""")
opcionesDisponibles = ['1', '2', '3', '4', '5', '6']
#Se valida que se ingrese una opcion valida
while opcion not in opcionesDisponibles:
    print("Opcion Invalida")
    opcion = input("\n>")

if opcion == '1':
    import UI.UIDatosDia

elif opcion == '2':
    import UI.UIMonthReport
    
elif opcion == '3':
    import UI.UIReportAdvance


elif opcion == '4':
    import UI.UIGoals

elif opcion == '5':
    import UI.UIUpdatePublisher

elif opcion == '6':
    print("Hasta la proxima !!")
    time.sleep(2)
    
