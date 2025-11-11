import pickle

class ClasificadorReclamo:
    def __init__(self):
        self.__clf = None 
        with open('./data/claims_clf.pkl', 'rb') as archivo:
                self.__clf = pickle.load(archivo)
        

    def clasificar(self, p_reclamo: str) -> str:
        if self.__clf is None:
            print("Error: El clasificador no está cargado.")
            return "indefinido" # El clasificador no se pudo cargar
        
        try:

            respuesta_lista = self.__clf.classify([p_reclamo])
            return respuesta_lista[0]
        
        except Exception as e:
            print(f"Error al clasificar el reclamo: {e}")
            return "indefinido"
        
    
    