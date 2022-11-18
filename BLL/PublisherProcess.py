from random import randrange
from DAL import File
from Clases.Publicador import Publicador
import hashlib

def ObtienePublicador():
    publisherDict = File.ObtienePublicador()["Publicador"]
    publicadorRegistrado = Publicador()
    publicadorRegistrado.nombreCompleto = publisherDict['nombreCompleto']
    publicadorRegistrado.correoPersonal = publisherDict['correoPersonal']
    publicadorRegistrado.correoEncargadoInfs = publisherDict['correoEncargadoInfs']
    publicadorRegistrado.grupo = publisherDict['grupo']
    publicadorRegistrado.genero = publisherDict['genero']
    try:
        publicadorRegistrado.passwd = publisherDict['passwd']
    except KeyError:
        publicadorRegistrado.passwd = None
    return publicadorRegistrado

def GuardaPublicador(publicador):
    File.GuardaPublicador(publicador)

def EditaPublicador(publicador):
    #Para editar un publicador se debe borrar todo primero
    File.BorraPublicador()
    File.GuardaPublicador(publicador)

def is_Email_Valid(email):
    'Returns True if the email is valid'
    return email.find('@') != -1 and email.find('.') != -1

def EliminaPublicador():
    'Elimina todos los datos de los 3 archivos JSON'
    File.BorraPublicador()
    File.BorraJSONMetas()
    File.EliminaDatos()

def getHashPasswdHex(passwd) -> str:
    'Retorna el hash en hexadecimal'
    hash = hashlib.sha256()
    hash.update(bytearray(passwd, "UTF-8"))
    return hash.hexdigest()

def getHashPasswdBytes(passwd) -> bytes:
    'Retorna el hash en bytes'
    hash = hashlib.sha256()
    hash.update(bytearray(passwd, "UTF-8"))
    return hash.digest()

def isPasswdCorrect(savedPassword, loginPassword):
    'Retorna True si la contraseña es correcta'
    #Se obtiene el hash en hexadecimal de la contraseña digitada
    loginPassword = getHashPasswdHex(loginPassword)
    return loginPassword == savedPassword

def generateSecurityCode():
    'Genera el codigo de 6 dígitos para recuperar la contraseña'
    securityCode:str = ""
    for i in range(6):
        #Se genera un numero aleatorio
        randNum = randrange(1,10)
        securityCode += str(randNum)
    return securityCode

def isSecurityCodeCorrect(securityCode, codeEntered):
    """Verifica que el codigo de seguridad ingresado por el usuario es el correcto"""
    return securityCode == codeEntered