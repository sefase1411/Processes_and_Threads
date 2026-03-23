"""
**Explicación:**  
En esta solución se utiliza un `Event` para representar la cancelación de la operación y un `Timer` de 2 segundos para 
controlar el tiempo máximo de espera. El temporizador se inicia antes de ejecutar la conexión al servicio.

Si la conexión tarda más de 2 segundos, el `Timer` ejecuta la función `timeout_expirado()`, la cual imprime un mensaje 
de error y activa el evento de cancelación con `evento_cancelacion.set()`. Esto indica que la operación excedió el 
tiempo permitido.

Si la conexión termina antes del límite, el programa verifica que el evento no haya sido activado, cancela el temporizador 
con `timer.cancel()` y muestra el mensaje de conexión exitosa.

Esta versión es mejor porque diferencia correctamente entre una conexión exitosa y una conexión que tardó demasiado. 
Aunque `time.sleep()` no puede interrumpirse directamente, el uso del evento permite marcar la operación como cancelada 
y evitar que el sistema la considere válida después del timeout.
"""
import threading
import time
import random

def conectar_a_servicio():
    tiempo = random.randint(1, 5)
    time.sleep(tiempo)
    return "Conectado"

def timeout_expirado(evento_cancelacion):
    print("Timeout: La conexión tardó demasiado. Operación cancelada.")
    evento_cancelacion.set()

def main():
    evento_cancelacion = threading.Event()

    timer = threading.Timer(3, timeout_expirado, args=(evento_cancelacion,))
    timer.start()

    resultado = conectar_a_servicio()

    if not evento_cancelacion.is_set():
        timer.cancel()
        print(f"Conexión exitosa: {resultado}.")
    # si el evento está activado, ya se imprimió el mensaje de timeout

main()