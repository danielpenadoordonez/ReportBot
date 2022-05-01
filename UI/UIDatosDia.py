import time
from Clases.Dia import Dia
from BLL import DiaProcess
from json.decoder import JSONDecodeError

try:
    #Se cargan los dias registrados
    DiaProcess.carga_Dias_Registrados()
    #Si empezo un nuevo mes y el usuario no ha enviado el informe del mes anterior 
    #entonces no puede ingresar datos del nuevo mes
    if not DiaProcess.same_Month():
        print("No ha generado el informe del mes anterior, para ingresar nuevos datos debe primero enviar el informe anterior")
        time.sleep(5)
        #Se le pregunta la usuario si desea enviar el informe
        answerOptions = ['Si', 'No']
        answer = input("\nDesea enviar el informe ya (Si/No)> ").capitalize()
        while answer not in answerOptions:
            print("\tRespuesta Invalida")
            time.sleep(1)
            answer = input("\nDesea enviar el informe ya (Si/No)> ").capitalize()
        #Si el usuario decidio enviar el informe se envia y luego se le permite ingresar los datos nuevos
        if answer == 'Si':
            import UI.UIMonthReport
            print("""
            ---------------------------------------------------
               Ya puede ingresar los datos del nuevo mes
            ---------------------------------------------------
            """)
            time.sleep(1)
        else:
            exit()
except JSONDecodeError:
    pass
except FileNotFoundError:
    pass

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
print("Datos Guardados")
time.sleep(2)