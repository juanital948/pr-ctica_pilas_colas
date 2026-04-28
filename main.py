from estructuras import Queue, Stack


class Paciente:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def __str__(self):
        return self.nombre + " (" + self.tipo + ")"


class Area:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.cola_pacientes = Queue()

    def __str__(self):
        return self.nombre + " -> " + str(self.cola_pacientes)


class Laboratorio:

    def __init__(self):
        self.pila_areas = Stack()
        self.pila_areas.push(Area("Entrega de resultados", 2))
        self.pila_areas.push(Area("Validación", 1))
        self.pila_areas.push(Area("Análisis", 2))
        self.pila_areas.push(Area("Toma de muestras", 3))

    def agregar_paciente(self, nombre, tipo):
        paciente = Paciente(nombre, tipo)
        self.pila_areas.top().cola_pacientes.enqueue(paciente)

    def ejecutar_turno(self):

        print("\n===== INICIO TURNO =====")

        pila_invertida = Stack()
        pila_recorrido = Stack()
        pila_pacientes_atendidos = Stack()

        while not self.pila_areas.is_empty():
            pila_invertida.push(self.pila_areas.pop())

        while not pila_invertida.is_empty():
            self.pila_areas.push(pila_invertida.pop())

        while not self.pila_areas.is_empty():

            area_actual = self.pila_areas.pop()
            pacientes_atendidos = Queue()

            print("\nÁrea:", area_actual.nombre)

            for _ in range(area_actual.capacidad):
                if area_actual.cola_pacientes.is_empty():
                    break

                paciente = area_actual.cola_pacientes.dequeue()
                print("Atendido:", paciente)
                pacientes_atendidos.enqueue(paciente)

            print("En espera:", area_actual.cola_pacientes)

            pila_recorrido.push(area_actual)
            pila_pacientes_atendidos.push(pacientes_atendidos)

        while not pila_recorrido.is_empty():

            area_actual = pila_recorrido.pop()
            pacientes_atendidos = pila_pacientes_atendidos.pop()

            if not self.pila_areas.is_empty():
                area_siguiente = self.pila_areas.top()

                while not pacientes_atendidos.is_empty():
                    area_siguiente.cola_pacientes.enqueue(
                        pacientes_atendidos.dequeue()
                    )

            self.pila_areas.push(area_actual)

        print("\n===== FIN TURNO =====")

    def ejecutar_automatico(self):
        numero_turno = 1

        while not self.esta_vacio():
            print("\nTURNO", numero_turno)
            self.ejecutar_turno()
            numero_turno += 1

    def esta_vacio(self):
        pila_auxiliar = Stack()
        vacio = True

        while not self.pila_areas.is_empty():
            area = self.pila_areas.pop()

            if not area.cola_pacientes.is_empty():
                vacio = False

            pila_auxiliar.push(area)

        while not pila_auxiliar.is_empty():
            self.pila_areas.push(pila_auxiliar.pop())

        return vacio

    def eliminar_area(self, nombre_area):

        pila_auxiliar = Stack()
        area_eliminada = None

        while not self.pila_areas.is_empty():
            area = self.pila_areas.pop()

            if area.nombre == nombre_area:
                area_eliminada = area
                break
            else:
                pila_auxiliar.push(area)

        if area_eliminada and not self.pila_areas.is_empty():
            area_siguiente = self.pila_areas.top()

            while not area_eliminada.cola_pacientes.is_empty():
                area_siguiente.cola_pacientes.enqueue(
                    area_eliminada.cola_pacientes.dequeue()
                )

        while not pila_auxiliar.is_empty():
            self.pila_areas.push(pila_auxiliar.pop())

    def agregar_area(self, nombre, capacidad):
        self.pila_areas.push(Area(nombre, capacidad))

    def mostrar_estado(self):

        pila_auxiliar = Stack()

        print("\n--- ESTADO DEL SISTEMA ---")

        while not self.pila_areas.is_empty():
            area = self.pila_areas.pop()
            print(area)
            pila_auxiliar.push(area)

        while not pila_auxiliar.is_empty():
            self.pila_areas.push(pila_auxiliar.pop())


def menu():

    laboratorio = Laboratorio()

    while True:

        print("\n1. Agregar paciente")
        print("2. Ejecutar turno")
        print("3. Ejecutar automático")
        print("4. Eliminar área")
        print("5. Agregar área")
        print("6. Mostrar estado")
        print("0. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            tipo = input("Tipo (adulto/niño): ").lower()

            while tipo not in ["adulto", "niño"]:
                tipo = input("Ingrese adulto o niño: ").lower()

            laboratorio.agregar_paciente(nombre, tipo)

        elif opcion == "2":
            laboratorio.ejecutar_turno()

        elif opcion == "3":
            laboratorio.ejecutar_automatico()

        elif opcion == "4":
            laboratorio.eliminar_area(input("Área: "))

        elif opcion == "5":
            laboratorio.agregar_area(
                input("Nombre: "),
                int(input("Capacidad: "))
            )

        elif opcion == "6":
            laboratorio.mostrar_estado()

        elif opcion == "0":
            break


menu()