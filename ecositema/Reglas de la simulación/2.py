import json

class Especie:
    def __init__(self, nombre, tipo, capacidad_busqueda, tasa_efectividad=None, velocidad_digestion=None, capacidad_reproduccion=None, cantidad_individuos=1):
        self.nombre = nombre
        self.tipo = tipo  # 'herbivoro', 'carnivoro' o 'planta'
        self.capacidad_busqueda = capacidad_busqueda  # Porcentaje (0-1)
        self.tasa_efectividad = tasa_efectividad if tipo == 'carnivoro' else None  # Porcentaje (0-1)
        self.velocidad_digestion = velocidad_digestion if tipo in ['herbivoro', 'carnivoro'] else None  # Porcentaje (0-1)
        self.capacidad_reproduccion = capacidad_reproduccion  # Porcentaje (0-1)
        self.cantidad_individuos = cantidad_individuos  # Cantidad de individuos

    def alimentar(self, alimento_disponible):
        if self.tipo == 'planta':
            # Las plantas no se alimentan, solo se reproducen
            return 0
        elif self.tipo == 'herbivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.velocidad_digestion
            if TAC > 0:
                self.cantidad_individuos += TAC
                return TAC
            else:
                return 0
        elif self.tipo == 'carnivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.tasa_efectividad * self.velocidad_digestion
            if TAC > 0:
                self.cantidad_individuos += TAC
                return TAC
            else:
                return 0

    def reproducir(self):
        if self.cantidad_individuos > 0:
            incremento = self.cantidad_individuos * self.capacidad_reproduccion
            self.cantidad_individuos += incremento

    def morir(self):
        if self.cantidad_individuos > 0:
            self.cantidad_individuos -= self.cantidad_individuos * 0.1  # Mortalidad por falta de alimento

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "capacidad_busqueda": self.capacidad_busqueda,
            "tasa_efectividad": self.tasa_efectividad,
            "velocidad_digestion": self.velocidad_digestion,
            "capacidad_reproduccion": self.capacidad_reproduccion,
            "cantidad_individuos": self.cantidad_individuos
        }

def simular_dia(especies):
    # Las plantas se reproducen
    for especie in especies:
        if especie.tipo == 'planta':
            especie.reproducir()

    # Alimentar herbívoros
    for especie in especies:
        if especie.tipo == 'herbivoro':
            alimento_consumido = especie.alimentar(100)  # Suponiendo 100 unidades de alimento disponible
            if alimento_consumido == 0:
                especie.morir()  # Si no se alimenta, muere

    # Alimentar carnívoros
    for especie in especies:
        if especie.tipo == 'carnivoro':
            alimento_consumido = especie.alimentar(100)  # Suponiendo 100 unidades de alimento disponible
            if alimento_consumido == 0:
                especie.morir()  # Si no se alimenta, muere

    # Reproducción de herbívoros y carnívoros
    for especie in especies:
        if especie.tipo in ['herbivoro', 'carnivoro']:
            if especie.cantidad_individuos > 0:  # Solo puede reproducirse si ha comido
                especie.reproducir()

def guardar_ecosistema(especies, filename):
    with open(filename, 'w') as file:
        json.dump([especie.to_dict() for especie in especies], file, indent=4)

def cargar_ecosistema(filename):
    with open(filename, 'r') as file:
        especies_data = json.load(file)
        return [Especie(**data) for data in especies_data]

def mostrar_estadisticas(especies):
    stats = {especie.nombre: {
        "tipo": especie.tipo,
        "cantidad_individuos": especie.cantidad_individuos,
        "capacidad_reproduccion": especie.capacidad_reproduccion
    } for especie in especies}
    return stats

def main():
    ecosistema = []
    while True:
        print("\nMenú:")
        print("1. Agregar Especie")
        print("2. Simular Día")
        print("3. Mostrar Estadísticas")
        print("4. Guardar Ecosistema")
        print("5. Cargar Ecosistema")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre de la especie: ")
            tipo = input("Tipo (herbivoro, carnivoro, planta): ")
            capacidad_busqueda = float(input("Capacidad de búsqueda (0-1): "))
            tasa_efectividad = float(input("Tasa de efectividad (0-1, solo para carnívoros): ")) if tipo == 'carnivoro' else None
            velocidad_digestion = float(input("Velocidad de digestión (0-1): ")) if tipo in ['herbivoro', 'carnivoro'] else None
            capacidad_reproduccion = float(input("Capacidad de reproducción (0-1): "))
            cantidad_individuos = int(input("Cantidad de individuos: "))
            nueva_especie = Especie(nombre, tipo, capacidad_busqueda, tasa_efectividad, velocidad_digestion, capacidad_reproduccion, cantidad_individuos)
            ecosistema.append(nueva_especie)
            print(f"Especie {nombre} agregada.")

        elif opcion == '2':
            dias = int(input("¿Cuántos días desea simular? "))
            for dia in range(dias):
                simular_dia(ecosistema)
                print(f"Día {dia + 1} simulado.")
            guardar_ecosistema(ecosistema, 'datos.txt')
            print("Datos del ecosistema guardados.")

        elif opcion == '3':
            stats = mostrar_estadisticas(ecosistema)
            print(json.dumps(stats, indent=4))

        elif opcion == '4':
            filename = input("Nombre del archivo para guardar el ecosistema: ")
            guardar_ecosistema(ecosistema, filename)
            print(f"Ecosistema guardado en {filename}.")

        elif opcion == '5':
            filename = input("Nombre del archivo para cargar el ecosistema: ")
            ecosistema = cargar_ecosistema(filename)
            print(f"Ecosistema cargado desde {filename}.")

        elif opcion == '6':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()