from BLL import DiaProcess

class Informe:

    days = list()
    
    def __init__(self, estudios=0):
        self.estudios = estudios

    @classmethod
    def carga_Dias(cls):
        'Carga todos los dias registrados en DatosMes.json'
        cls.days = DiaProcess.carga_Dias_Registrados()

    def getTotalHoras(self):
        'Retorna el total de Horas registradas'
        horas = 0
        if len(self.days) > 0:
            for day in self.days:
                horas += day.horas
            return horas
        else:
            return 0

    def getTotalPublicaciones(self):
        'Retorna el total de Publicaciones registradas'
        publicaciones = 0
        if len(self.days) > 0:
            for day in self.days:
                publicaciones += day.publicaciones
            return publicaciones
        else:
            return 0

    def getTotalRevisitas(self):
        'Retorna el total de Revisitas registradas'
        revisitas = 0
        if len(self.days) > 0:
            for day in self.days:
                revisitas += day.revisitas
            return revisitas
        else:
            return 0

    def getTotalVideos(self):
        'Retorna el total de Videos registrados'
        videos = 0
        if len(self.days) > 0:
            for day in self.days:
                videos += day.videos
            return videos
        else:
            return 0

    def getTotalDias(self):
        'Retorna la cantidad de dias que se predico en el mes'
        fechasRegistradas = list()
        if len(self.days) > 0:
            for day in self.days:
                if day.fecha not in fechasRegistradas:
                    fechasRegistradas.append(day.fecha)
            return len(fechasRegistradas)
        else:
            return 0

    #Metodo que construye el informe y lo devuelve
    def construyeInforme(self):
        horas = self.getTotalHoras()
        publicaciones = self.getTotalPublicaciones()
        revisitas = self.getTotalRevisitas()
        videos = self.getTotalVideos()
        
        reporte = f""" 
                         ----------------------------------
                         |                 |                
                         |  Horas          |      {horas}         
                         |                 |              
                         |  Publicaciones  |      {publicaciones}       
                         |                 |              
                         |  Videos         |      {videos}       
                         |                 |              
                         |  Revisitas      |      {revisitas}       
                         |                 |              
                         |  Estudios       |      {self.estudios}       
                         |                 |              
                         ----------------------------------"""
                    
        return reporte
