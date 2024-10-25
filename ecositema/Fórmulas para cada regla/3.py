import random

class Especie:
    def __init__(self, nombre, tipo, capacidad_busqueda, tasa_efectividad=None, velocidad_digestion=None, capacidad_reproduccion=None, cantidad_individuos=1):
        self.nombre = nombre
        self.tipo = tipo  # 'herbivoro' o 'carnivoro'
        self.capacidad_busqueda = capacidad_busqueda  # Porcentaje (0-1)
        self.tasa_efectividad = tasa_efectividad if tipo == 'carnivoro' else None  # Porcentaje (0-1)
        self.velocidad_digestion = velocidad_digestion  # Porcentaje (0-1)
        self.capacidad_reproduccion = capacidad_reproduccion  # Porcentaje (0-1)
        self.cantidad_individuos = cantidad_individuos  # Cantidad de individuos

    def alimentarse(self, alimento_disponible):
        if self.tipo == 'herbivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.velocidad_digestion
            self.cantidad_individuos += TAC
            return TAC
        elif self.tipo == 'carnivoro':
            TAC = alimento_disponible * self.capacidad_busqueda * self.tasa_efectividad * self.velocidad_digestion
            self.cantidad_individuos += TAC
            return TAC

    def reproducirse(self):
        if self.capacidad_reproduccion:
            incremento = self.cantidad_individuos * self.capacidad_reproduccion
            self.cantidad_individuos += incremento

    def morir(self):
        self.cantidad_individuos -= self.cantidad_individuos * 0.1  # Mortalidad por falta de alimento

def simular_dia(especies, alimento_disponible):
    # Ordenar especies por capacidad de búsqueda y tasa de efectividad
    especies.sort(key=lambda x: (x.capacidad_busqueda * (x.tasa_efectividad if x.tipo == 'carnivoro' else 1)), reverse=True)

    for especie in especies:
        alimento_consumido = especie.alimentarse(alimento_disponible)
        if alimento_consumido == 0:
            especie.morir()
        else:
            especie.reproducirse()

# Ejemplo de uso
herbivoros = [Especie("Conejo", "herbivoro", 0.8, velocidad_digestion=0.9, capacidad_reproduccion=0.5, cantidad_individuos=10)]
carnivoros = [Especie("Lobo", "carnivoro", 0.7, tasa_efectividad=0.6, velocidad_digestion=0.8, capacidad_reproduccion=0.4, cantidad_individuos=5)]

ecosistema = herbivoros + carnivoros
alimento_disponible = 100  # Unidades de alimento disponible

# Simular 10 días
for dia in range(10):
    print(f"Día {dia + 1}:")
    simular_dia(ecosistema, alimento_disponible)
    for especie in ecosistema:
        print(f"{especie.nombre}: {especie.cantidad_individuos:.2f} individuos")