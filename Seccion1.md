# Taller de Concurrencia y Cliente-Servidor

## Objetivo General

Evaluar la capacidad del estudiante para analizar, diseñar e implementar soluciones concurrentes utilizando primitivas de sincronización dentro de escenarios de arquitectura cliente-servidor.

## Competencias a Desarrollar

- Diferenciar procesos vs. hilos en sistemas concurrentes.
- Analizar problemas de concurrencia y paralelismo.
- Identificar condiciones de carrera, *deadlocks* y *starvation*.
- Implementar sincronización usando:
  - Locks
  - RLocks
  - Semáforos
  - Variables condicionales
  - Eventos
  - Barreras
  - Temporizadores
- Diseñar soluciones concurrentes para sistemas cliente-servidor.

---

## SECCIÓN 1: Conceptual

Responda a las siguientes preguntas de manera clara, concisa y técnicamente precisa.

### 1. Diferencia entre concurrencia y paralelismo

**Pregunta:**  
Explique la diferencia fundamental entre concurrencia y paralelismo. Proporcione un ejemplo de la vida cotidiana (no informático) para cada concepto que ilustre claramente esta diferencia.

**Respuesta:**  
La diferencia fundamental entre concurrencia y paralelismo está en que, en la concurrencia, varias actividades se van atendiendo dentro del mismo intervalo de tiempo, pero no necesariamente se realizan al mismo tiempo exacto; en cambio, en el paralelismo sí se ejecutan de manera simultánea.

Por ejemplo, un caso de concurrencia en la vida cotidiana es cuando un mesero atiende varias mesas durante su turno. Primero toma el pedido de una, luego lleva la cuenta a otra y después responde una pregunta en otra mesa. No hace todo al mismo tiempo, pero sí va alternando entre varias tareas para que todas avancen.

Un ejemplo de paralelismo sería una mudanza en la que varias personas trabajan al mismo tiempo: una empaca cajas, otra baja los muebles y otra los acomoda en el camión. En este caso, las actividades sí ocurren simultáneamente.

En resumen, la concurrencia consiste en organizar varias tareas que progresan por turnos, mientras que el paralelismo implica ejecutar varias tareas al mismo tiempo.

---

### 2. Condición de carrera (*race condition*)

**Pregunta:**  
Defina qué es una condición de carrera (*race condition*). En el siguiente fragmento de código en Python, identifique la condición de carrera y explique por qué ocurre.

**Respuesta:**  
Una **condición de carrera** ocurre cuando dos o más hilos o procesos acceden al mismo tiempo a un dato compartido y lo modifican sin sincronización, de modo que el resultado final depende del orden en que se ejecuten esas operaciones.

En el siguiente código:

```python
import threading

contador_compartido = 0
NUM_INC = 1000000

def incrementar():
    global contador_compartido
    for _ in range(NUM_INC):
        contador_compartido += 1

hilo1 = threading.Thread(target=incrementar)
hilo2 = threading.Thread(target=incrementar)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print(f"Valor esperado: {2*NUM_INC}, Valor obtenido: {contador_compartido}")

Correccion:

import threading

contador_compartido = 0
NUM_INC = 1000000
lock = threading.Lock()   // definicion de lock 

def incrementar():
    global contador_compartido
    for _ in range(NUM_INC):
        with lock:       //Aplicacion
            contador_compartido += 1

hilo1 = threading.Thread(target=incrementar)
hilo2 = threading.Thread(target=incrementar)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print(f"Valor esperado: {2*NUM_INC}, Valor obtenido: {contador_compartido}")


### 3. Diferencia entre *deadlock* e inanición (*starvation*)

**Pregunta:**  
Un *deadlock* (bloqueo mutuo) y la inanición (*starvation*) son dos problemas graves en sistemas concurrentes. Compare y contraste estos dos conceptos. ¿Cuál de los dos considera más fácil de prevenir en el diseño de un sistema y por qué?

**Respuesta:**  
Un *deadlock* o bloqueo mutuo ocurre cuando dos o más procesos o hilos quedan esperando indefinidamente recursos que están retenidos entre sí, de modo que ninguno puede continuar. En cambio, la inanición o *starvation* sucede cuando un proceso sí podría ejecutarse, pero en la práctica nunca recibe el recurso o el turno porque otros procesos siempre son atendidos antes.

La diferencia principal es que, en el *deadlock*, todos los involucrados quedan completamente detenidos, mientras que en la inanición el sistema sigue funcionando, pero uno o varios procesos pueden quedarse esperando por mucho tiempo o incluso de forma indefinida.

Por ejemplo, en un *deadlock*, el proceso A tiene el recurso 1 y espera el recurso 2, mientras que el proceso B tiene el recurso 2 y espera el recurso 1. Ninguno avanza. En la inanición, en cambio, un proceso de baja prioridad puede quedar siempre aplazado porque continuamente llegan procesos de mayor prioridad.

Considero que el *deadlock* es más fácil de prevenir en el diseño de un sistema, porque existen reglas más claras para evitarlo, como imponer un orden fijo para tomar recursos, evitar la espera circular o liberar recursos antes de pedir otros nuevos. La inanición suele ser más difícil de controlar, porque depende mucho de cómo se reparten prioridades y del planificador del sistema.

---

### 4. Uso de múltiples procesos vs. múltiples hilos en un servidor

**Pregunta:**  
En el contexto de un servidor que atiende a múltiples clientes, describa una situación donde el uso de múltiples procesos (vía `multiprocessing`) sería más ventajoso que el uso de múltiples hilos (vía `threading`). Mencione al menos dos ventajas y una desventaja de usar procesos en este escenario.

**Respuesta:**  
Una situación donde usar múltiples procesos sería más ventajoso que usar múltiples hilos es en un servidor que atiende muchos clientes y donde cada solicitud realiza cálculos pesados, por ejemplo: procesamiento de imágenes, cifrado, análisis de datos o inteligencia artificial.

En ese caso, `multiprocessing` puede ser mejor porque cada proceso trabaja de forma independiente y aprovecha mejor varios núcleos del procesador. Con `threading`, en Python, los hilos pueden verse limitados en tareas de mucho cálculo.

**Ventajas de usar procesos:**

1. **Mejor rendimiento en tareas intensivas de CPU.**  
   Los procesos pueden ejecutarse realmente en paralelo en distintos núcleos, lo que mejora el tiempo de respuesta del servidor.

2. **Mayor aislamiento y seguridad.**  
   Si un proceso que atiende a un cliente falla, no afecta tan fácilmente a los demás, porque cada proceso tiene su propia memoria.

**Desventaja de usar procesos:**

- **Consumen más recursos.**  
  Crear y mantener procesos gasta más memoria y más tiempo que usar hilos, por lo que el servidor puede volverse más pesado.