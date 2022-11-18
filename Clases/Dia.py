from datetime import date, datetime
import locale

class Dia:

    __MONTHS = {
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May" : 5,
        "Jun" : 6,
        "Jul" : 7,
        "Aug" : 8,
        "Sep" : 9,
        "Oct" : 10,
        "Nov" : 11,
        "Dec" : 12
    }

    def __init__(self, horas=0 , revisitas=0, publicaciones=0, videos=0):
        self.month = datetime.strptime(str(datetime.now().month), "%m").strftime("%B").upper()
        self.horas = horas
        self.revisitas = revisitas
        self.publicaciones = publicaciones
        self.videos = videos
        self.fecha = self.getFecha()
    
    def getHoras(self):
        return self.horas

    def getRevisitas(self):
        return self.revisitas

    def getPublicaciones(self):
        return self.publicaciones
    
    def getVideos(self):
        return self.videos

    def getFecha(self):
        currentDate = datetime.now().strftime("%d/%b/%Y")
        dateList = currentDate.split('/')
        dateList[1] = str(self.__MONTHS.get(dateList[1]))
        return "/".join(dateList)

    def __str__(self):
        return f"{self.getFecha()}\nHoras: {self.horas}\nPublicaciones: {self.publicaciones}\nRevisitas: {self.revisitas}\nVideos: {self.videos}\n\n"
