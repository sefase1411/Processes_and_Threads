### 1. El Cajero Automático
"""
**Problemas identificados:**

- **Condición de carrera sobre `saldo_cuenta`.**  
  Varios hilos acceden y modifican la misma variable compartida al mismo tiempo sin sincronización.

- **Uso incorrecto del acceso al saldo.**  
  La validación `if saldo_cuenta >= monto` y la operación `saldo_cuenta -= monto` no están protegidas como una sola sección crítica.

- **Lock declarado pero no utilizado.**  
  Aunque se crea `lock_cuenta = threading.Lock()`, nunca se usa para controlar el acceso concurrente.

**Riesgos:**

- **Retiros simultáneos incorrectos.**  
  Varios clientes pueden leer el mismo saldo antes de que otro hilo lo actualice.

- **Saldo inconsistente o negativo.**  
  El programa puede permitir más retiros de los que realmente soporta la cuenta.

- **Resultados no deterministas.**  
  El saldo final puede cambiar entre ejecuciones, aunque el código sea el mismo.

**Propuesta de corrección:**

Se debe usar el `Lock` para proteger toda la operación de retiro, es decir, tanto la validación del saldo como el descuento. De esta manera, solo un hilo a la vez podrá revisar y modificar `saldo_cuenta`.

**Código corregido:**
"""
import threading
import time

saldo_cuenta = 1000
lock_cuenta = threading.Lock()

def retirar_dinero(cliente_id, monto):
    global saldo_cuenta
    print(f"Cliente {cliente_id} intenta retirar ${monto}...")

    with lock_cuenta:
        if saldo_cuenta >= monto:
            time.sleep(0.1)
            saldo_cuenta -= monto
            print(f"Cliente {cliente_id} retiró ${monto}. Nuevo saldo: ${saldo_cuenta}")
        else:
            print(f"Cliente {cliente_id}: Fondos insuficientes. Saldo actual: ${saldo_cuenta}")

clientes = []
for i in range(5):
    t = threading.Thread(target=retirar_dinero, args=(i, 600))
    clientes.append(t)
    t.start()

for t in clientes:
    t.join()

print(f"Saldo final: ${saldo_cuenta}")