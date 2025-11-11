from modules.reclamo import Reclamo
from collections import Counter #modulo para evitar usar diccionarios
from modules.calculadora_mediana import MonticuloMediana 

# Lista simple de "stopwords" en español 
STOPWORDS = [
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "con", "por", "un",
    "para", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o",
    "este", "ha", "me", "si", "sin", "sobre", "este", "es", "porque", "cuando",
    "muy", "ante", "bajo", "cabe", "contra", "desde", "durante", "entre", "hacia",
    "hasta", "mediante", "para", "por", "segun", "sin", "so", "sobre", "tras", "via"
]

class GeneradorEstadisticas:
    def __init__(self, reclamos: list[Reclamo]):
        self.__reclamos = reclamos

    def calcular_porcentajes_estado(self) -> dict[str, float]:
        """
        Calcula el número total de reclamos y los porcentajes por estado.
        """
        total_reclamos = len(self.__reclamos)
        if total_reclamos == 0:
            return {"total": 0, "pendientes": 0, "en_proceso": 0, "resueltos": 0}

        conteo_estados = Counter(r.estado for r in self.__reclamos) #cuenta cuántas veces aparece cada elemento único.

        #Porque es una estructura auto-descriptiva.
        #Cada valor que devuelve va acompañado de una "etiqueta" (la clave) que explica qué es.
        reporte = {
            "total": total_reclamos,
            "pendientes": (conteo_estados.get("pendiente", 0) / total_reclamos) * 100,
            "en_proceso": (conteo_estados.get("en proceso", 0) / total_reclamos) * 100,
            "resueltos": (conteo_estados.get("resuelto", 0) / total_reclamos) * 100,
        }
        return reporte

    def calcular_palabras_frecuentes(self, cantidad: int = 15) -> list[tuple[str, int]]:
        #Unimos el contenido de todos los reclamos en un solo texto.
        texto_completo = " ".join(r.contenido for r in self.__reclamos).lower()

        # Definimos los caracteres que SÍ queremos conservar.
        caracteres_permitidos = "abcdefghijklmnopqrstuvwxyzáéíóúñ "
        
        # Usamos una lista para construir el nuevo string limpio eficientemente.
        lista_caracteres_limpios = []
        for caracter in texto_completo:
            if caracter in caracteres_permitidos:
                lista_caracteres_limpios.append(caracter)
            else:
                # Si el caracter no es una letra (ej. un punto, coma, número),
                # lo reemplazamos por un espacio para separar palabras.
                lista_caracteres_limpios.append(' ')
        
        # Unimos la lista de caracteres para formar nuestro texto limpio.
        texto_limpio = "".join(lista_caracteres_limpios)

        #Separamos en palabras y filtramos las stopwords y palabras cortas.
        palabras = [
            palabra for palabra in texto_limpio.split()
            if palabra not in STOPWORDS and len(palabra) > 2
        ]

        #Contamos las frecuencias y devolvemos las 'cantidad' más comunes.
        return Counter(palabras).most_common(cantidad) #a partir del diccionario de Counter, se ordenan las palabras y se determina la mas y menos comun
    
    def calcular_mediana_tiempos_resolucion(self) -> float:
        calculadora = MonticuloMediana()
        reclamos_validos_contados = 0
        
        for reclamo in self.__reclamos:
            # Filtramos solo los estados que pide la consigna 
            if reclamo.estado in ["en proceso", "resuelto"]:
                tiempo_asignado = reclamo.tiempo_resolucion_asignado
                
                # Nos aseguramos que el reclamo tenga un tiempo asignado
                if tiempo_asignado is not None:
                    calculadora.agregar_numero(tiempo_asignado)
                    reclamos_validos_contados += 1
        
        if reclamos_validos_contados == 0:
            return 0.0 # Evitamos errores si no hay reclamos con tiempo
        
        return calculadora.obtener_mediana()