"""
**Explicación:**  
Cada hilo representa un auto. Primero, cada auto tarda un tiempo aleatorio en llegar a la salida. 
Cuando llega, imprime un mensaje y espera en la barrera con `barrera.wait()`. 
La barrera bloquea a cada auto hasta que los 5 hayan llegado. 
En el momento en que todos alcanzan la barrera, esta se libera y todos los autos continúan al mismo tiempo, 
iniciando la carrera de forma simultánea.
"""

import threading
import time
import random

def auto(auto_id, barrera):
    time.sleep(random.uniform(0.5, 2))  # tiempo aleatorio para llegar
    print(f"Auto {auto_id} llegó a la salida y está esperando.")

    posicion = barrera.wait()  # espera a que lleguen los 5 autos

    if posicion == 0:
        print("--- ¡CARRERA! ---")

    print(f"Auto {auto_id} inició la carrera.")


# Barrera para 5 autos
barrera_salida = threading.Barrier(5)

# Crear e iniciar 5 hilos
hilos = []
for i in range(1, 6):
    h = threading.Thread(target=auto, args=(i, barrera_salida))
    hilos.append(h)
    h.start()

# Esperar a que todos terminen
for h in hilos:
    h.join()
