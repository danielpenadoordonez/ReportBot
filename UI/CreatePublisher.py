import time
import smtplib
from BLL import PublisherProcess
from BLL import SendEmail
from Clases.Publicador import Publicador
import getpass

print("""
 ______    ______    _______    _______    _______    _________          ______     ______   __________ 
|      |  |         |       |   |      |   |      |       |             |      |   |      |      |   
|      |  |         |       |   |      |   |      |       |             |      |   |      |      |
|______|  |______   |_______|   |      |   |______|       |             |______|   |      |      |
|\\        |         |           |      |   |\\             |             |      |   |      |      |
| \\       |         |           |      |   | \\            |             |      |   |      |      |
|  \\      |______   |           |______|   |  \\           |             |______|   |______|      | 
                                      
DESCRIPCION: 
ReportBot es un programa para facilitar el proceso de gestion y envio de 
informes a fin de mes, lo unico que tiene que hacer es asegurarse de ingresar
los datos que hizo cada dia que participe en alguna faceta del ministerio.
Si participa varias veces en un mismo dia se recomienda que ingrese todos los
datos juntos al fin del dia.

Tambien incluye la opcion de agregar metas que quiera alcanzar en el mes o cada mes
y una opcion para ver avances y registrar como va en el mes hasta la fecha en que 
solicite el avance

IMPORTANTE: 
Para usar ReportBot debe aceptar ingresar todos los siguientes datos de lo contrario
no podra usar el programa
Datos a Ingresar: - Su Nombre Completo
                  - Su Correo Personal (Se recomienda el que use mas frecuentemente)
                  - El Correo del que recoje su informe
                  - El grupo de predicacion al que usted pertenece
                  - Su Genero (Para indicar en el informe si es publicador o publicadora)
""")

opciones = ["Si", "No"]

opcion = input("Acepta las condiciones, Digite Si o No: ").capitalize()
#Validar que se haya ingresado la opcion correcta
while opcion not in opciones:
    print("Opcion Invalida")
    time.sleep(1)
    opcion = input("Acepta las condiciones, Digite Si o No: ").capitalize()

if opcion == "Si":
    #Se solicita el ingreso de los datos y se valida que se ingresen correctamente
    print("\nIngrese los siguienes datos:")
    time.sleep(1)
    fullName = input("\n\tSU NOMBRE COMPLETO: ")
    while fullName.isspace() or len(fullName.split()) < 3:
        print("Por favor ingrese su nombre completo con sus 2 apellidos")
        time.sleep(1)
        fullName = input("\n\tSU NOMBRE COMPLETO: ")

    personalEmail = input("\n\tSU CORREO PERSONAL: ")
    while not PublisherProcess.is_Email_Valid(personalEmail):
        print("Direccion de correo invalida")
        time.sleep(1)
        personalEmail = input("\n\tSU CORREO PERSONAL: ")

    reportRecieverEmail = input("\n\tCORREO DEL ENCARGADO DE RECOJER SU INFORME: ")
    while not PublisherProcess.is_Email_Valid(reportRecieverEmail):
        print("Direccion de correo invalida")
        time.sleep(1)
        reportRecieverEmail = input("\n\tCORREO DEL ENCARGADO DE RECOJER SU INFORME: ")
        
    group = input("\n\tSU GRUPO DE PREDICACION: ")
    while group.isspace() or group == "":
        print("Por favor ingrese el grupo al que pertenece")
        time.sleep(1)
        group = input("\n\tSU GRUPO DE PREDICACION: ")

    gender = input("\n\tDigite su genero (H si es Hombre, M si es Mujer): ").upper()
    options = ["H", "M"]
    if gender not in options:
        print("Opcion Invalida, digite H o M: ")
        time.sleep(1)
        gender = input("\n\tDigite su genero (H si es Hombre, M si es Mujer): ").upper()

    password = getpass.getpass("\n\tDIGITE UNA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
    while password.isspace() or password == "":
        print("Por favor digite una contraseña")
        time.sleep(1)
        password = getpass.getpass("\n\tDIGITE UNA CONTRASEÑA (No se va a ver cuando la escriba): ", stream=None)
    password = PublisherProcess.getHashPasswdHex(password)

    #Se crea el nuevo publicador y se guardan sus datos
    newPublisher = Publicador(fullName, personalEmail, reportRecieverEmail, group, gender, password)
    PublisherProcess.GuardaPublicador(newPublisher)
    print("---------------Procesando y registrando datos---------------")
    time.sleep(4)
    #Enviar aviso de que hay un nuevo publicador registrado
    try:
        SendEmail.load_Creds()
        SendEmail.send_New_User_Alert(newPublisher)
    except smtplib.SMTPAuthenticationError:
        pass
    except smtplib.SMTPException:
        pass
    print("\nLos datos han sido registrados correctamente")
    time.sleep(1)
    print("\nPara empezar a usar las funciones disponibles, vuelva a abrir el programa")
    time.sleep(4)

else:
    exit()


