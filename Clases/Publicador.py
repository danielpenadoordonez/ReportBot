class Publicador():

    def __init__(self, nombreCompleto="", correoPersonal="", correoEncargado="", grupo="", genero="", password=None):
        self.nombreCompleto = nombreCompleto
        self.correoPersonal = correoPersonal
        self.correoEncargadoInfs = correoEncargado
        self.grupo = grupo
        self.genero = genero
        self.passwd = password

    #Metodos Get y Set
    def setNombreCompleto(self, nombreCompleto):
        self.nombreCompleto = nombreCompleto

    def setCorreoPersonal(self, correoPersonal):
        self.correoPersonal = correoPersonal

    def setCorreoEncargadoInfs(self, correoEncargado):
        self.correoEncargadoInfs = correoEncargado

    def setGrupo(self, grupo):
        self.grupo = grupo

    def setGenero(self, genero):
        self.genero = genero

    def getNombreCompleto(self):
        return self.nombreCompleto

    def getCorreoPersonal(self):
        return self.correoPersonal

    def getCorreoEncargadoInfs(self):
        return self.correoEncargadoInfs

    def getGrupo(self):
        return self.grupo

    def getGenero(self):
        return self.genero

    