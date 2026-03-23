"""
**Explicación:**  
La solución utiliza un buffer compartido protegido con `Lock` y dos semáforos.  
El semáforo `espacios_libres` impide que el productor agregue tareas cuando el buffer está lleno.  
El semáforo `tareas_disponibles` impide que los consumidores retiren tareas cuando el buffer está vacío.  
Además, se usan valores `None` como señal de finalización para que los consumidores terminen correctamente cuando ya no quedan tareas por procesar.
"""

import threading
import time
import random

class BufferCompartido:
    def __init__(self, capacidad=10):
        self.capacidad = capacidad
        self.buffer = []
        self.mutex = threading.Lock()
        self.espacios_libres = threading.Semaphore(capacidad)
        self.tareas_disponibles = threading.Semaphore(0)

    def agregar(self, tarea):
        self.espacios_libres.acquire()   # espera si el buffer está lleno
        with self.mutex:
            self.buffer.append(tarea)
            print(f"Productor: Tarea {tarea} añadida. Buffer: {self.buffer}")
        self.tareas_disponibles.release()  # avisa que hay una tarea nueva

    def quitar(self, consumidor_id):
        self.tareas_disponibles.acquire()  # espera si el buffer está vacío
        with self.mutex:
            tarea = self.buffer.pop(0)
            print(f"Consumidor-{consumidor_id}: Tomó tarea {tarea}. Buffer: {self.buffer}")
        self.espacios_libres.release()  # libera un espacio en el buffer
        return tarea


def productor(buffer, total_tareas, num_consumidores):
    for i in range(1, total_tareas + 1):
        time.sleep(random.uniform(0.05, 0.15))  # simula producción
        buffer.agregar(i)

    # Señales de fin para cada consumidor
    for _ in range(num_consumidores):
        buffer.agregar(None)


def consumidor(buffer, consumidor_id):
    while True:
        tarea = buffer.quitar(consumidor_id)

        if tarea is None:
            print(f"Consumidor-{consumidor_id}: No hay más tareas. Termina.")
            break

        time.sleep(random.uniform(0.1, 0.3))  # simula procesamiento
        print(f"Consumidor-{consumidor_id}: Procesó tarea {tarea}.")


# Programa principal
buffer = BufferCompartido(capacidad=10)
total_tareas = 20
num_consumidores = 2

hilo_productor = threading.Thread(target=productor, args=(buffer, total_tareas, num_consumidores))
hilos_consumidores = [
    threading.Thread(target=consumidor, args=(buffer, i + 1))
    for i in range(num_consumidores)
]

hilo_productor.start()
for h in hilos_consumidores:
    h.start()

hilo_productor.join()
for h in hilos_consumidores:
    h.join()

print("Todas las tareas fueron procesadas.")