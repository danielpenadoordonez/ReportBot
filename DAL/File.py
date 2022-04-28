from fileinput import close
import os
import json
from stat import S_IREAD, S_IWRITE

#Registra los datos por dia para el informe
def GuardaDatos(dias):
    file = os.path.join("DAL", "DatosMes.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    with open(file, "w") as monthFile:
        json.dump(dias, monthFile, indent=4, default=lambda dia : dia.__dict__)
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)

def ObtieneDiasRegistrados():
    file = os.path.join("DAL", "DatosMes.json")
    with open(file, "r") as monthFile:
        return json.load(monthFile)

def EliminaDatos():
    file = os.path.join("DAL", "DatosMes.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    open(file, "w").close()
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)

#Registra los datos para las metas
def GuardaMetaJSON(metas):
    file = os.path.join("DAL", "Metas.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    with open(file, "w") as goalFile:
        json.dump(metas, goalFile, indent=4, default=lambda goal: goal.__dict__)
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)

def ObtieneMetasJSON():
    file = os.path.join("DAL", "Metas.json")
    with open(file, "r") as goalFile:
        return json.load(goalFile)  

def BorraJSONMetas():
    file = os.path.join("DAL", "Metas.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    open(file, "w").close()
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)

#Registra los datos del publicador
def GuardaPublicador(publicador):
    file = os.path.join("DAL", "Publicador.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    with open(file, "w") as publisherFile:
        json.dump({"Publicador" : publicador.__dict__}, publisherFile, indent=4)
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)

def ObtienePublicador():
    file = os.path.join("DAL", "Publicador.json")
    with open(file, "r") as publisherFile:
        return json.load(publisherFile)

def BorraPublicador():
    file = os.path.join("DAL", "Publicador.json")
    if os.path.exists(file):
        #Se debe habilitar la escritura
        os.chmod(file, S_IWRITE)
    open(file, "w").close()
    #Se debe volver a poner como de solo lectura
    os.chmod(file, S_IREAD)