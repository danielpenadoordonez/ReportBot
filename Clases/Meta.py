from datetime import datetime
from DAL.DT import GoalData
from json import JSONDecodeError

class Meta:
    'Clase para crear nuevos objetos meta que se guardan en el archivo Goals.json'
    __TIPOS_DE_METAS = dict()

    def __init__(self, nombre='', cantidad=0, descripcion='', tipo=''):
        self.nombre = nombre
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.tipo = tipo
        self.fechaRegistro = datetime.now().strftime("%d/%b/%Y")
        #Llamado a funcion que asigna el ID del tipo de meta seleccionado
        #al atributo self.id
        self.set_Id(self.tipo)

    #METODOS SET Y GET
    def get_Nombre(self):
        return self.nombre

    def get_Cantidad(self):
        return self.cantidad

    def get_Descripcion(self):
        return self.descripcion

    def get_Tipo(self):
        return self.tipo

    def get_Id(self):
        return self.id

    def set_Nombre(self, nombre):
        self.nombre = nombre

    def set_Cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_Descripcion(self, descripcion):
        self.descripcion = descripcion

    def set_Tipo(self, tipo):
        self.tipo = tipo

    def set_Id(self, tipo):
        #Funcion anidada que retorna True si la llave de diccionario pasado como argumento
        #contiene el valor del tipo de meta seleccionado
        def is_Type(keyId):
            return self.__TIPOS_DE_METAS[keyId] == tipo
            
        #Se usa la funcion filter() para iterar sobre las llaves de __TIPOS_DE_METAS
        #y se filtra la respuesta usando la funcion anidada anterior
        lst = (list(filter(is_Type, self.__TIPOS_DE_METAS.keys())))
        self.id = lst[0] if len(lst) == 1 else None
    
    @classmethod
    def load_Goals(cls):
        try:
            goals_Json = GoalData.loadGoals()
            #Convertir cada id de string a int
            goal_Keys_Num = list(map(lambda key : int(key), goals_Json.keys()))
            for key in goal_Keys_Num:
                cls.__TIPOS_DE_METAS[key] = goals_Json.get(str(key))
            
        except JSONDecodeError:
            cls.__TIPOS_DE_METAS = {
                                    1: "Horas",
                                    2: "Revisitas",
                                    3: "Publicaciones",
                                    4: "Estudios",
                                    5: "Videos",
                                    6: "Dias"
                                }
        except FileNotFoundError:
            cls.__TIPOS_DE_METAS = {
                                    1: "Horas",
                                    2: "Revisitas",
                                    3: "Publicaciones",
                                    4: "Estudios",
                                    5: "Videos",
                                    6: "Dias"
                                }

    @classmethod
    def get_Tipos_Metas(cls):
        return list(map(lambda value : value, cls.__TIPOS_DE_METAS.values()))
    #FIN DE SET Y GET

    @classmethod
    def display_Types(cls):
        'Muestra los tipos de metas que hay disponibles'
        displayString = "\t\nTIPOS DE METAS" + '.'*45 + "\n"
        for value in cls.__TIPOS_DE_METAS.values():
            displayString += '\t-- ' + value + "\n"
        return displayString
    
    def __str__(self) -> str:
        return f"""
        NOMBRE: {self.nombre}
        OBJETIVO: {self.cantidad}
        DESCRIPCION: {self.descripcion}
        TIPO: {self.tipo}
        """