from modules.monticulo import MonticuloMinimos, MonticuloMaximos

class MonticuloMediana:
    def __init__(self):
        # Montículo de máximos para la mitad inferior de los datos 
        self.__mitad_inferior_max = MonticuloMaximos()
        # Montículo de mínimos para la mitad superior de los datos 
        self.__mitad_superior_min = MonticuloMinimos()
        self.__mediana_actual = None

    def __balancear(self):
        """
        Asegura que la diferencia de tamaño entre los dos montículos
        no sea mayor a 1. 
        """
        tam_inf = self.__mitad_inferior_max.tamano()
        tam_sup = self.__mitad_superior_min.tamano()
        
        if abs(tam_inf - tam_sup) > 1:
            if tam_inf > tam_sup:
                # Mover la raíz del max-heap (el más grande de la mitad inf) al min-heap
                valor_a_mover = self.__mitad_inferior_max.eliminar_raiz()
                self.__mitad_superior_min.insertar(valor_a_mover)
            else:
                # Mover la raíz del min-heap (el más pequeño de la mitad sup) al max-heap
                valor_a_mover = self.__mitad_superior_min.eliminar_raiz()
                self.__mitad_inferior_max.insertar(valor_a_mover)
    
    def __actualizar_mediana(self):
        """
        Recalcula la mediana basándose en las raíces de los montículos. 
        """
        tam_inf = self.__mitad_inferior_max.tamano()
        tam_sup = self.__mitad_superior_min.tamano()

        if tam_inf == tam_sup:
            # Si tienen el mismo tamaño, la mediana es el promedio de ambas raíces 
            self.__mediana_actual = (self.__mitad_inferior_max.obtener_raiz() + self.__mitad_superior_min.obtener_raiz()) / 2.0
        elif tam_inf > tam_sup:
            # Si no, es la raíz del montículo más grande 
            self.__mediana_actual = float(self.__mitad_inferior_max.obtener_raiz())
        else:
            # Si no, es la raíz del montículo más grande 
            self.__mediana_actual = float(self.__mitad_superior_min.obtener_raiz())

    def agregar_numero(self, num: int):
        """
        Agrega un nuevo número al cálculo y re-calcula la mediana.
        """
        # Paso 1: Insertar el número
        # Si el max-heap está vacío o el número es menor que su raíz, va a la mitad inferior
        if self.__mitad_inferior_max.esta_vacio() or num < self.__mitad_inferior_max.obtener_raiz():
            self.__mitad_inferior_max.insertar(num)
        else:
            self.__mitad_superior_min.insertar(num)
        
        # Paso 2: Balancear los montículos
        self.__balancear()
        
        # Paso 3: Calcular la nueva mediana
        self.__actualizar_mediana()

    def obtener_mediana(self) -> float:
        """Devuelve la mediana calculada."""
        return self.__mediana_actual