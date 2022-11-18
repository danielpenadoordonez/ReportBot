import time
import getpass
from BLL import PublisherProcess
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


optionsToEdit = ['1', '2', '3', '4', '5', '6']
if PUBLICADOR.genero == 'H':
    print(f"""
    ===================================================
    |     PUBLICADOR: {PUBLICADOR.nombreCompleto}    
    ===================================================
    |""")
else:
    print(f"""
    ===================================================
    |     PUBLICADORA: {PUBLICADOR.nombreCompleto}    
    ===================================================
    |""")
print(f"""    |
    |
    | 1. Correo Personal ->  {PUBLICADOR.correoPersonal}
    |
    | 2. Correo del Recolector de Informe ->   {PUBLICADOR.correoEncargadoInfs}
    |
    | 3. Su Grupo de Predicacion   ->     {PUBLICADOR.grupo}
    |
    | 4. Cambiar su Contraseña
    |
    | 5. Eliminar Publicador del Programa (Elimina todos los Datos del Publicador, Datos del Mes, y Metas)
    |
    | 6. Regresar
    ===================================================
    """)
selectedOption = input("\tOpcion a Editar> ")
while selectedOption not in optionsToEdit:
    print("Opcion Invalida\n")
    time.sleep(1)
    selectedOption = input("\tOpcion a Editar> ")
    
#Funcion que va a modificar datos
def modify_Based_On_Option():
    'Realiza el proceso de editar acorde a la opcion seleccionada'
    if selectedOption == '1':
        newPersonalEmail = input("\tIngrese su nuevo correo personal: ")
        while not PublisherProcess.is_Email_Valid(newPersonalEmail):
            print("Direccion de correo invalida")
            time.sleep(1)
            newPersonalEmail = input("\tIngrese su nuevo correo personal: ")
        PUBLICADOR.correoPersonal = newPersonalEmail

    elif selectedOption == '2':
        newEncEmail = input("\tIngrese el nuevo correo del encargado del informe: ")
        while not PublisherProcess.is_Email_Valid(newEncEmail):
            print("Direccion de correo invalida")
            time.sleep(1)
            newEncEmail = input("\tIngrese el nuevo correo del encargado del informe: ")
        PUBLICADOR.correoEncargadoInfs = newEncEmail

    elif selectedOption == '3':
        newGroup = input("\tIngrese su nuevo grupo de predicacion: ")
        while newGroup.isspace() or newGroup == "":
            print("Por favor ingrese su nuevo grupo")
            time.sleep(1)
            newGroup = input("\tIngrese su nuevo grupo de predicacion: ")
        PUBLICADOR.grupo = newGroup

    elif selectedOption == '4':
        #Se tiene que pedir la contraseña
        loginpassword = getpass.getpass("\nContraseña: ", stream=None)
        fails = 0
        while not PublisherProcess.isPasswdCorrect(PUBLICADOR.passwd, loginpassword):
            print("\tContraseña Incorrecta")
            fails += 1
            time.sleep(1)
            #Al tercer fallo
            if fails == 3:
                print("\n¡¡¡Se le acabaron los intentos, ReportBot se va cerrar!!!")
                time.sleep(2)
                exit()
            loginpassword = getpass.getpass("\nContraseña: ", stream=None)
        import UI.ChangePass

    elif selectedOption == '5':
        respuesta = input("\tDesea eliminar toda la informacion del Publicador (Si/No)> ").capitalize()
        if respuesta == "Si":
            #Se le tiene que pedir al usuario que ingrese su contraseña y solo se le dan 2 oportunidades para ingresarla
            loginpassword = getpass.getpass("\nContraseña: ", stream=None)
            fails = 0
            #Mientras la contraseña no sea valida
            while not PublisherProcess.isPasswdCorrect(PUBLICADOR.passwd, loginpassword):
                print("\tContraseña Incorrecta")
                fails += 1
                time.sleep(1)
                #Al segundo fallo
                if fails == 2:
                    print("\n¡¡¡Se le acabaron los intentos, ReportBot se va cerrar!!!")
                    time.sleep(2)
                    exit()
                loginpassword = getpass.getpass("\nContraseña: ", stream=None)
                
            PublisherProcess.EliminaPublicador()
            print("------------------ELIMINANDO TODOS LOS DATOS------------------")
            time.sleep(2)
            print("\nToda su informacion, metas y registros del mes ha sido eliminada")
            time.sleep(4)
            exit()

    elif selectedOption == '6':
        pass

#Se llama a al funcion
modify_Based_On_Option()
optList = ["Si", "No"]
if selectedOption == '6':
    confirmation = "No"
else:
    confirmation = input("\n\tDesea editar otro dato (Si/No)> ").capitalize()

while confirmation not in optList:
    print("Respuesta Invalida")
    time.sleep(1)
    confirmation = input("\n\tDesea editar otro dato (Si/No)> ").capitalize()
while confirmation == "Si":
    selectedOption = input("\tOpcion a Editar> ")
    while selectedOption not in optionsToEdit:
        print("Opcion Invalida\n")
        time.sleep(1)
        selectedOption = input("\tOpcion a Editar> ")
    #Se vuelve a llamar a la funcion de editar 
    modify_Based_On_Option()
    confirmation = input("\n\tDesea editar otro dato (Si/No)> ").capitalize()
    while confirmation not in optList:
        print("Respuesta Invalida")
        time.sleep(1)
        confirmation = input("\n\tDesea editar otro dato (Si/No)> ").capitalize()


if selectedOption != '5' and selectedOption != '6':
    #Se guardan los datos modificados
    PublisherProcess.EditaPublicador(PUBLICADOR)
    time.sleep(1)
    print("\nLos nuevos datos se han actualizado")
time.sleep(2)