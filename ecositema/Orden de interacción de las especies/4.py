import random

class Especie:
    def __init__(self, nombre, tipo, capacidad_busqueda, tasa_efectividad=None, velocidad_digestion=None, capacidad_reproduccion=None, cantidad_individuos=1, tasa_mortalidad=0.02):
        self.nombre = nombre
        self.tipo = tipo  # 'herbivoro' o 'carnivoro'
        self.capacidad_busqueda = capacidad_busqueda  # Porcentaje (0-1)
        self.tasa_efectividad = tasa_efectividad if tipo == 'carnivoro' else None  # Porcentaje (0-1)
        self.velocidad_digestion = velocidad_digestion  # Porcentaje (0-1)
        self.capacidad_reproduccion = capacidad_reproduccion  # Porcentaje (0-1)
        self.cantidad_individuos = cantidad_individuos  # Cantidad de individuos
        self.tasa_mortalidad = tasa_mortalidad  # Tasa de mortalidad por vejez/pelea

    def alimentarse(self, alimento_disponible):
        if self.tipo == 'herbivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.velocidad_digestion
            return TAC
        elif self.tipo == 'carnivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.tasa_efectividad * self.velocidad_digestion
            return TAC

    def reproducirse(self):
        if self.capacidad_reproduccion:
            incremento = self.cantidad_individuos * self.capacidad_reproduccion
            self.cantidad_individuos += incremento

    def morir_por_inanicion(self):
        self.cantidad_individuos -= self.cantidad_individuos * 0.1  # Mortalidad por falta de alimento

    def morir_por_vejez(self):
        self.cantidad_individuos -= self.cantidad_individuos * self.tasa_mortalidad  # Mortalidad por vejez/pelea

def simular_dia(especies, alimento_disponible):
    # Las plantas se reproducen primero
    for especie in especies:
        if especie.tipo == 'planta':
            especie.reproducirse()

    # Ordenar herbívoros por capacidad de búsqueda
    herbivoros = [e for e in especies if e.tipo == 'herbivoro']
    herbivoros.sort(key=lambda x: x.capacidad_busqueda, reverse=True)

    # Los herbívoros se alimentan
    for herbivoro in herbivoros:
        alimento_consumido = herbivoro.alimentarse(alimento_disponible)
        if alimento_consumido > 0:
            herbivoro.cantidad_individuos += alimento_consumido  # Aumentar según el alimento consumido
        else:
            herbivoro.morir_por_inanicion()  # Morir por inanición

    # Ordenar carnívoros por capacidad de búsqueda y tasa de efectividad
    carnivoros = [e for e in especies if e.tipo == 'carnivoro']
    carnivoros.sort(key=lambda x: (x.capacidad_busqueda * x.tasa_efectividad), reverse=True)

    # Los carnívoros se alimentan
    for carnivoro in carnivoros:
        alimento_consumido = carnivoro.alimentarse(alimento_disponible)
        if alimento_consumido > 0:
            carnivoro.cantidad_individuos += alimento_consumido  # Aumentar según el alimento consumido
        else:
            carnivoro.morir_por_inanicion()  # Morir por inanición

    # Herbívoros se reproducen
    for herbivoro in herbivoros:
        herbivoro.reproducirse()

    # Carnívoros mueren por inanición y vejez
    for carnivoro in carnivoros:
        carnivoro.morir_por_inanicion()  # Morir por inanición
        carnivoro.morir_por_vejez()  # Morir por vejez

    # Carnívoros se reproducen
    for carnivoro in carnivoros:
        carnivoro.reproducirse()

# Ejemplo de uso
def main():
    # Crear especies de plantas, herbívoros y carnívoros
    plantas = [Especie("Planta A", "planta", capacidad_reproduccion=0.3, cantidad_individuos=50)]
    herbivoros = [Especie("Conejo", "herbivoro", 0.8, velocidad_digestion=0.9, capacidad_reproduccion=0.5, cantidad_individuos=10)]
    carnivoros = [Especie("Lobo", "carnivoro", 0.7, tasa_efectividad=0.6, velocidad_digestion=0.8, capacidad_reproduccion=0.4, cantidad_individuos=5)]

    ecosistema = plantas + herbivoros + carnivoros
    alimento_disponible = 100  # Unidades de alimento disponible

    # Solicitar al usuario la cantidad de días a simular
    dias_a_simular = int(input("Ingrese la cantidad de días a simular: "))

    # Simular los días
    for dia in range(dias_a_simular):
        print(f"Día {dia + 1}:")
        simular_dia(ecosistema, alimento_disponible)
        for especie in ecosistema:
            print(f"{especie.nombre}: {especie.cantidad_individuos:.2f} individuos")
        print("-" * 30)

if __name__ == "__main__":
    main()