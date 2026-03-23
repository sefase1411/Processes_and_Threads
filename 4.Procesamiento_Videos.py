import threading
import time
import random
from collections import deque


# =========================
# Modelo de trabajo
# =========================
class Trabajo:
    def __init__(self, video_id, cliente, tipo):
        self.video_id = video_id
        self.cliente = cliente
        self.tipo = tipo  # "Premium" o "Gratis"


# =========================
# Strategy: política de prioridad
# =========================
class PoliticaPrioridad:
    def __init__(self, max_premium_seguidos=3):
        self.max_premium_seguidos = max_premium_seguidos
        self.premium_seguidos = 0

    def seleccionar_siguiente(self, cola_premium, cola_gratis):
        # Si ambos tienen trabajos, aplicar prioridad con anti-starvation
        if cola_premium and cola_gratis:
            if self.premium_seguidos >= self.max_premium_seguidos:
                self.premium_seguidos = 0
                return cola_gratis.popleft()
            else:
                self.premium_seguidos += 1
                return cola_premium.popleft()

        # Si solo hay premium
        if cola_premium:
            self.premium_seguidos += 1
            return cola_premium.popleft()

        # Si solo hay gratis
        if cola_gratis:
            self.premium_seguidos = 0
            return cola_gratis.popleft()

        return None


# =========================
# Cola compartida segura
# =========================
class ColaTrabajos:
    def __init__(self, politica):
        self.cola_premium = deque()
        self.cola_gratis = deque()
        self.condition = threading.Condition()
        self.politica = politica
        self.productores_activos = 0

    def registrar_productor(self):
        with self.condition:
            self.productores_activos += 1

    def finalizar_productor(self):
        with self.condition:
            self.productores_activos -= 1
            self.condition.notify_all()

    def agregar_trabajo(self, trabajo):
        with self.condition:
            if trabajo.tipo == "Premium":
                self.cola_premium.append(trabajo)
            else:
                self.cola_gratis.append(trabajo)

            print(f"{trabajo.cliente}: Envió trabajo [{trabajo.video_id}] ({trabajo.tipo})")
            self.condition.notify()

    def obtener_trabajo(self):
        with self.condition:
            while not self.cola_premium and not self.cola_gratis:
                if self.productores_activos == 0:
                    return None
                self.condition.wait()

            return self.politica.seleccionar_siguiente(self.cola_premium, self.cola_gratis)


# =========================
# Clientes
# =========================
class Cliente(threading.Thread):
    def __init__(self, nombre, tipo, cola):
        super().__init__()
        self.nombre = nombre
        self.tipo = tipo
        self.cola = cola

    def run(self):
        self.cola.registrar_productor()

        cantidad_trabajos = random.randint(5, 10)
        for i in range(1, cantidad_trabajos + 1):
            time.sleep(random.uniform(0.1, 0.4))
            trabajo = Trabajo(
                video_id=f"{self.nombre}-VIDEO-{i}",
                cliente=self.nombre,
                tipo=self.tipo
            )
            self.cola.agregar_trabajo(trabajo)

        self.cola.finalizar_productor()


# =========================
# Factory Method
# =========================
class FabricaClientes:
    @staticmethod
    def crear_cliente(nombre, tipo, cola):
        return Cliente(nombre, tipo, cola)


# =========================
# Workers
# =========================
def worker(worker_id, cola):
    while True:
        trabajo = cola.obtener_trabajo()

        if trabajo is None:
            break

        nota = ""
        if trabajo.tipo == "Gratis":
            nota = " (trabajo gratuito procesado sin inanición)"

        print(
            f"Worker-{worker_id}: Procesando trabajo "
            f"[{trabajo.video_id}] de {trabajo.cliente} ({trabajo.tipo}){nota}"
        )

        time.sleep(random.uniform(0.3, 0.8))

    print(f"Worker-{worker_id}: Sin más trabajos. Termina.")


# =========================
# Main
# =========================
def main():
    politica = PoliticaPrioridad(max_premium_seguidos=3)
    cola = ColaTrabajos(politica)

    clientes = []

    # 3 clientes premium
    for i in range(1, 4):
        clientes.append(
            FabricaClientes.crear_cliente(f"Cliente-Premium-{i}", "Premium", cola)
        )

    # 5 clientes gratuitos
    for i in range(1, 6):
        clientes.append(
            FabricaClientes.crear_cliente(f"Cliente-Gratis-{i}", "Gratis", cola)
        )

    workers = []
    for i in range(1, 4):
        t = threading.Thread(target=worker, args=(i, cola))
        workers.append(t)

    # Iniciar workers
    for w in workers:
        w.start()

    # Iniciar clientes
    for c in clientes:
        c.start()

    # Esperar clientes
    for c in clientes:
        c.join()

    # Esperar workers
    for w in workers:
        w.join()

    print("--- Sistema finalizado ---")


if __name__ == "__main__":
    main()