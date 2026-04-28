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
        return self.nombre + " [" + str(self.cola_pacientes) + "]"


class Laboratorio:
    def __init__(self):
        self.areas = Stack()
        self.areas.push(Area("Entrega de resultados", 2))
        self.areas.push(Area("Validación de resultados", 1))
        self.areas.push(Area("Análisis", 2))
        self.areas.push(Area("Toma de muestras", 3))

    def agregar_paciente(self, nombre, tipo):
        paciente = Paciente(nombre, tipo)
        self.areas.top().cola_pacientes.enqueue(paciente)
        print("Paciente agregado correctamente.")

    def ejecutar_turno(self):
        print("\n===== TURNO =====")

        pila_recorrido = Stack()
        pila_atendidos = Stack()

        while not self.areas.is_empty():
            area_actual = self.areas.pop()
            atendidos_area = Queue()

            print("\nÁrea:", area_actual.nombre)

            contador = 0

            while contador < area_actual.capacidad and not area_actual.cola_pacientes.is_empty():
                paciente = area_actual.cola_pacientes.dequeue()
                print("Atendido:", paciente)
                atendidos_area.enqueue(paciente)
                contador += 1

            if contador == 0:
                print("No se atendieron pacientes.")

            print("En espera:", area_actual.cola_pacientes)

            pila_recorrido.push(area_actual)
            pila_atendidos.push(atendidos_area)

        while not pila_recorrido.is_empty():
            area_actual = pila_recorrido.pop()
            atendidos_area = pila_atendidos.pop()

            if not self.areas.is_empty():
                area_siguiente = self.areas.top()

                while not atendidos_area.is_empty():
                    area_siguiente.cola_pacientes.enqueue(atendidos_area.dequeue())
            else:
                while not atendidos_area.is_empty():
                    paciente_sale = atendidos_area.dequeue()
                    print("Sale del laboratorio:", paciente_sale)

            self.areas.push(area_actual)

        print("\n===== FIN DEL TURNO =====")

    def ejecutar_automatico(self):
        turno = 1

        while not self.esta_vacio():
            print("\nTURNO", turno)
            self.ejecutar_turno()
            turno += 1

        print("\nNo quedan pacientes en el laboratorio.")

    def esta_vacio(self):
        auxiliar = Stack()
        vacio = True

        while not self.areas.is_empty():
            area = self.areas.pop()

            if not area.cola_pacientes.is_empty():
                vacio = False

            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.areas.push(auxiliar.pop())

        return vacio

    def mostrar_estado(self):
        auxiliar = Stack()

        print("\n===== ESTADO DEL SISTEMA =====")

        while not self.areas.is_empty():
            area = self.areas.pop()
            print(area.nombre)
            print("Pacientes:", area.cola_pacientes)
            print("Cantidad:", area.cola_pacientes.len())
            auxiliar.push(area)

        while not auxiliar.is_empty():
            self.areas.push(auxiliar.pop())

    def agregar_area(self, nombre, capacidad):
        if capacidad <= 0:
            print("La capacidad debe ser mayor que cero.")
            return

        self.areas.push(Area(nombre, capacidad))
        print("Área agregada correctamente.")

    def eliminar_area(self, nombre):
        auxiliar = Stack()
        area_eliminada = None

        while not self.areas.is_empty():
            area = self.areas.pop()

            if area.nombre == nombre:
                area_eliminada = area
                break
            else:
                auxiliar.push(area)

        if area_eliminada is None:
            while not auxiliar.is_empty():
                self.areas.push(auxiliar.pop())

            print("No se encontró el área.")
            return

        if not self.areas.is_empty():
            area_siguiente = self.areas.top()

            while not area_eliminada.cola_pacientes.is_empty():
                area_siguiente.cola_pacientes.enqueue(area_eliminada.cola_pacientes.dequeue())
        else:
            while not area_eliminada.cola_pacientes.is_empty():
                paciente_sale = area_eliminada.cola_pacientes.dequeue()
                print("Paciente retirado del sistema:", paciente_sale)

        while not auxiliar.is_empty():
            self.areas.push(auxiliar.pop())

        print("Área eliminada correctamente.")


def menu():
    laboratorio = Laboratorio()

    while True:
        print("\n===== MENÚ LABORATORIO =====")
        print("1. Agregar paciente")
        print("2. Ejecutar turno")
        print("3. Ejecutar automático")
        print("4. Eliminar área")
        print("5. Agregar nueva área")
        print("6. Consultar estado")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            tipo = input("Tipo de paciente adulto/niño: ").lower()

            while tipo != "adulto" and tipo != "niño":
                tipo = input("Ingrese adulto o niño: ").lower()

            laboratorio.agregar_paciente(nombre, tipo)

        elif opcion == "2":
            laboratorio.ejecutar_turno()

        elif opcion == "3":
            laboratorio.ejecutar_automatico()

        elif opcion == "4":
            nombre = input("Nombre del área a eliminar: ")
            laboratorio.eliminar_area(nombre)

        elif opcion == "5":
            nombre = input("Nombre de la nueva área: ")
            capacidad = int(input("Capacidad por turno: "))
            laboratorio.agregar_area(nombre, capacidad)

        elif opcion == "6":
            laboratorio.mostrar_estado()

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


menu()