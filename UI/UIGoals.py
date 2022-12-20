import time
from Clases.Meta import Meta
from BLL import GoalProcess
from Services.Log import Log
from json.decoder import JSONDecodeError

def load_UIGoals():
    choiceOptions = ['A', 'B', 'C', 'D']
    invalidChoice = True
    goalChoice = None

    Meta.load_Goals()

    while invalidChoice:
        goalChoice = input("""
        A. Ver mis Metas
        B. Agregar Meta
        C. Eliminar Meta
        D. Salir
        \n\t>""")
        if goalChoice in choiceOptions:
            invalidChoice = False
        else:
            print("\t\nOpcion Invalida")
            time.sleep(1)

        
    #Opcion A = Ver mis Metas
    if goalChoice == 'A':
        try:
            #Se traen todas las metas registradas en el JSON y se muestra la info de cada una 
            for goal in GoalProcess.cargar_Mis_Metas():
                print(goal)
                time.sleep(1)
            Log.info(logName="goals", message="Metas cargadas y mostradas correctamente")
        except JSONDecodeError:
            #Esta excepcion se da si el archivo JSON esta vacio lo que significa
            #que no hay metas guardadas
            print("\nNo tiene metas registradas")
            Log.warning(logName="goals", message="No se encontraron metas en Metas.json: El archivo esta vacío, no existe o tiene algún error de sintaxis")
            time.sleep(1)
        except FileNotFoundError:
            print("\nNo tiene metas registradas")
            Log.warning(logName="goals", message="No se encontraron metas en Metas.json: El archivo esta vacío, no existe o tiene algún error de sintaxis")
            time.sleep(1)

    #Opcion B = Agregar Meta
    elif goalChoice == 'B':

        def nueva_Meta():
            #Desplegar las opciones de metas
            print(Meta.display_Types())
            try:
                #En el fondo se cargan las metas que ya estan registradas
                GoalProcess.cargar_Mis_Metas()
            except JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
            #Hay que validar que el tipo de meta este disponible y 
            #que la cantidad sea numerica
            tipoDeMeta = None
            metaNoDisponible = True
            while metaNoDisponible:
                tipoDeMeta = input("\n\tTIPO DE META: ")
                if tipoDeMeta in Meta.get_Tipos_Metas():
                    metaNoDisponible = False
                else:
                    print('La meta ingresada no esta disponible')
                    time.sleep(1)
            nombre = input("\n\tNOMBRE PERSONALIZADO: ")
            while nombre.isspace() or nombre == "":
                print("Por favor elija un nombre para su nueva meta")
                time.sleep(1)
                nombre = input("\n\tNOMBRE PERSONALIZADO: ")
            descripcion = input("\n\tDESCRIPCION: ")
            cantidad = 0
            invalidData = True
            while invalidData:
                try:
                    cantidad = int(input("\n\tCANTIDAD META: "))
                    invalidData = False
                except ValueError:
                    print("La cantidad meta se debe indicar con un numero")

            #Se construye el objeto Meta y se debe agregar su contenido al JSON
            meta = Meta(nombre, cantidad, descripcion, tipoDeMeta)
            #Se debe verificar que no sea de un tipo ya registrado
            if GoalProcess.meta_Existe(meta):
                print("\nYa tiene una meta de", meta.tipo, f": si desea una nueva meta de {meta.tipo} debe eliminar la que ya tiene registrada")
                time.sleep(8)
                return
            GoalProcess.GuardaMetaJSON(meta)
            Log.info(logName="goals", message=f"NUEVA META GUARDADA -> Nombre: {meta.nombre}, Cantidad: {meta.cantidad}, Tipo de Meta: {meta.tipo}, Descripcion: {meta.descripcion}")
            time.sleep(1)
            print('\n\n' + ' '*20 + "¡Meta Guardada!")
            time.sleep(2)

        #Se llama a la funcion
        nueva_Meta()
        #Se pregunta al usuario si desea agregar otra meta
        ops = ["Si", "No"]
        answer = input("\nDesea agregar otra meta (Si/No)> ").capitalize()
        #Se valida que sea una respuesa correcta
        while answer not in ops:
            print("Respuesta Invalida, debe digitar Si o No")
            time.sleep(1)
            answer = input("\nDesea agregar otra meta (Si/No)> ").capitalize()
        while answer == "Si":
            #Se vuelve a llamar la funcion que agrega metas
            nueva_Meta()
            answer = input("\nDesea agregar otra meta (Si/No)> ").capitalize()
            while answer not in ops:
                print("Respuesta Invalida, debe digitar Si o No")
                time.sleep(1)
                answer = input("\nDesea agregar otra meta (Si/No)> ").capitalize()

    #Opcion C = Eliminar Meta
    elif goalChoice == 'C':
        #Primeramente se deben cargar las metas ya registradas en una lista
        misMetas = list()
        idsDisponibles = list()
        try:
            misMetas = GoalProcess.cargar_Mis_Metas()
        except JSONDecodeError:
            #Se muestra el siguiente mensaje si no hay metas guardadas
            print("\nNo tiene metas registradas")
            Log.warning(logName="goals", message="No se encontraron metas en Metas.json: El archivo esta vacío, no existe o tiene algún error de sintaxis")
            time.sleep(3)
        except FileNotFoundError:
            print("\nNo tiene metas registradas")
            Log.warning(logName="goals", message="No se encontraron metas en Metas.json: El archivo esta vacío, no existe o tiene algún error de sintaxis")
            time.sleep(3)
        else:
            #Por cada meta, muestra el ID, el tipo de meta, y la cantidad en una tabla
            tablaMetas = f"""
        
                                    MIS METAS

            ============================================================
                            |                     
                META        |     NOMBRE (OBJETIVO)        
                            |                     
            ============================================================
            """
            for meta in misMetas:
                tablaMetas += f"""
                            |                     
                     {meta.id}      |       {meta.nombre} ({meta.cantidad})          
                            |                     
            ------------------------------------------------------------
                """
                time.sleep(0.5)
                idsDisponibles.append(meta.id)

            print(tablaMetas)
            idSeleccionado = 0
            idInvalido = True
            while idInvalido:
                try:
                    idSeleccionado = input("\n\tMETA a Eliminar o digite Todo si desea eliminarlas todas> ")
                    if idSeleccionado == "Todo" or idSeleccionado == "todo" or idSeleccionado == "TODO":
                        #Se debe confirmar
                        confirmacion = input("\nEsta seguro que desea eliminar todas sus metas (Si/No)> ")
                        if confirmacion == "Si" or confirmacion == "si":
                            GoalProcess.BorraJSONMetas()
                            Log.warning(logName="goals", message="Todas las metas han sido borradas de Metas.json")
                            time.sleep(1)
                            print("\nTodas sus metas han sido eliminadas")
                            time.sleep(2)
                            exit()
                        
                    idSeleccionado = int(idSeleccionado)
                    if idSeleccionado in idsDisponibles:
                        idInvalido = False
                    else:
                        print("La Meta ingresada no existe")
                        time.sleep(1)
                except ValueError:
                    print("La META se debe indicar por su número")
                    time.sleep(1)
                except KeyboardInterrupt:
                    time.sleep(2)
                    break
                
            try:
                if idSeleccionado != 0:
                    GoalProcess.EliminaMeta(idSeleccionado)
                    Log.info(logName="goals", message=f"La Meta con id {idSeleccionado} ha sido eliminada de la lista en Metas.json")
                    time.sleep(1)
                    print(f"La meta {idSeleccionado} ha sido eliminada")
                    time.sleep(2)
                else:
                    Log.warning(logName="goals", message="La META es 0 por lo tanto no se borró ninguna meta de Metas.json")
            except IndexError:
                pass
            #Si no quedan mas metas se tienen que quitar los corchetes en el archivo Metas.json
            try:
                if len(GoalProcess.cargar_Mis_Metas()) == 0:
                    GoalProcess.BorraJSONMetas()
                    Log.warning(logName="goals", message="Todas las metas han sido borradas de Metas.json")
            except JSONDecodeError:
                pass
            except FileNotFoundError:
                pass

    #Opcion D = Salir
    elif goalChoice == 'D':
        print("Hasta la proxima !!")
        time.sleep(2)