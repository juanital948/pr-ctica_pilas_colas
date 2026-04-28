from estructuras import Queue, Stack


class Paciente:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def __str__(self):
        return self.nombre + " (" + self.tipo + ")"


class Area:
    def __init__(self, nombre, capacidad):
        self.nombre: str = nombre
        self.capacidad: int = capacidad
        self.cola = Queue()

    def __str__(self):
        return self.nombre + " -> " + str(self.cola)


class Laboratorio:

    def __init__(self):
        self.pila = Stack()

        self.pila.push(Area("Entrega de resultados", 2))
        self.pila.push(Area("Validación", 1))
        self.pila.push(Area("Análisis", 2))
        self.pila.push(Area("Toma de muestras", 3))

    def agregar_paciente(self, nombre, tipo):
        self.pila.top().cola.enqueue(Paciente(nombre, tipo))

    def ejecutar_turno(self):

        print("\n====== TURNO ======")

        aux = Stack()

        while not self.pila.is_empty():
            aux.push(self.pila.pop())

        buffers = Stack()
        orden_areas = Stack()

        while not aux.is_empty():

            area = aux.pop()
            buffer = Queue()

            print("\nÁrea:", area.nombre)

            for _ in range(area.capacidad):
                if area.cola.is_empty():
                    break

                paciente = area.cola.dequeue()
                print("Atendido:", paciente)
                buffer.enqueue(paciente)

            print("En espera:", area.cola)

            orden_areas.push(area)
            buffers.push(buffer)

        reconstruida = Stack()

        while not orden_areas.is_empty():

            area = orden_areas.pop()
            buffer = buffers.pop()

            if not reconstruida.is_empty():
                siguiente = reconstruida.top()
                while not buffer.is_empty():
                    siguiente.cola.enqueue(buffer.dequeue())

            reconstruida.push(area)

        inv = Stack()
        while not reconstruida.is_empty():
            inv.push(reconstruida.pop())
        while not inv.is_empty():
            self.pila.push(inv.pop())

        print("\n====== FIN TURNO ======")

    def ejecutar_automatico(self):
        turno = 1
        while not self.vacio():
            print("\nTURNO", turno)
            self.ejecutar_turno()
            turno += 1

    def vacio(self):
        aux = Stack()
        vacio = True

        while not self.pila.is_empty():
            area = self.pila.pop()
            if not area.cola.is_empty():
                vacio = False
            aux.push(area)

        while not aux.is_empty():
            self.pila.push(aux.pop())

        return vacio

    def eliminar_area(self, nombre):

        aux = Stack()
        eliminada = None

        while not self.pila.is_empty():
            area = self.pila.pop()

            if area.nombre == nombre:
                eliminada = area
                break
            else:
                aux.push(area)

        if eliminada and not self.pila.is_empty():
            siguiente = self.pila.top()
            while not eliminada.cola.is_empty():
                siguiente.cola.enqueue(eliminada.cola.dequeue())

        while not aux.is_empty():
            self.pila.push(aux.pop())

    def agregar_area(self, nombre, cap):
        self.pila.push(Area(nombre, cap))

    def mostrar(self):
        aux = Stack()

        print("\n--- ESTADO DEL SISTEMA ---")

        while not self.pila.is_empty():
            area = self.pila.pop()
            print(area)
            aux.push(area)

        while not aux.is_empty():
            self.pila.push(aux.pop())


def menu():

    lab = Laboratorio()

    while True:

        print("\n1. Agregar paciente")
        print("2. Ejecutar turno")
        print("3. Ejecutar automático")
        print("4. Eliminar área")
        print("5. Agregar área")
        print("6. Mostrar estado")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            nombre = input("Nombre: ")
            tipo = input("Tipo (adulto/niño): ").lower()

            while tipo not in ["adulto", "niño"]:
                tipo = input("Ingrese adulto o niño: ").lower()

            lab.agregar_paciente(nombre, tipo)

        elif op == "2":
            lab.ejecutar_turno()

        elif op == "3":
            lab.ejecutar_automatico()

        elif op == "4":
            lab.eliminar_area(input("Área: "))

        elif op == "5":
            lab.agregar_area(input("Nombre: "), int(input("Capacidad: ")))

        elif op == "6":
            lab.mostrar()

        elif op == "0":
            break


menu()