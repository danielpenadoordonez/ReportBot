import time
from Clases.Dia import Dia
from BLL import DiaProcess
from UI.UIMonthReport import load_UIMonthReport
from Services.Log import Log
from json.decoder import JSONDecodeError

def load_UIDatosDia():
    try:
        #Se cargan los dias registrados
        DiaProcess.carga_Dias_Registrados()
    except JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    else:
        #Si empezó un nuevo mes y el usuario no ha enviado el informe del mes anterior 
        #entonces no puede ingresar datos del nuevo mes
        if not DiaProcess.same_Month():
            print("No ha generado el informe del mes anterior, para ingresar nuevos datos debe primero enviar el informe anterior")
            time.sleep(3)
            #Se le pregunta la usuario si desea enviar el informe
            answerOptions = ['Si', 'No']
            answer = input("\nDesea enviar el informe ya (Si/No)> ").capitalize()
            while answer not in answerOptions:
                print("\tRespuesta Invalida")
                time.sleep(1)
                answer = input("\nDesea enviar el informe ya (Si/No)> ").capitalize()
            #Si el usuario decidio enviar el informe se envia y luego se le permite ingresar los datos nuevos
            if answer == 'Si':
                load_UIMonthReport()
                DiaProcess.EliminaDatos()

                #Comprobar que los datos del mes anterior no estén en el archivo
                try:
                    #Se cargan los dias registrados
                    DiaProcess.carga_Dias_Registrados()
                except JSONDecodeError:
                    pass
                except FileNotFoundError:
                    pass
                else:
                    print("¡No se pudieron eliminar los datos del mes anterior!")
                    Log.error(logName="daily-data", message="No se pudieron borrar los datos del archivo DatosMes.json")
                    time.sleep(1)
                    print("\nContacte al desarrollador para que le ayude y pueda registrar los datos del nuevo mes")
                    time.sleep(4)
                    exit()

                print("""
                ---------------------------------------------------
                Ya puede ingresar los datos del nuevo mes
                ---------------------------------------------------
                """)
                time.sleep(1)
            else:
                exit()

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
    Log.info(logName="daily-data", message=f"Registro de datos -> Horas: {dia.horas}, Revisitas: {dia.revisitas}, Publicaciones: {dia.publicaciones}, Videos: {dia.videos}")
    print("Datos Guardados")
    time.sleep(2)