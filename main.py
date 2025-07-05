import csv
from collections import defaultdict

def cargar_datos_csv(ruta_csv):
    datos = []
    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            dia = int(fila['Día'])  
            atributos = tuple(fila[col] for col in lector.fieldnames if col != 'Día')
            datos.append((dia, atributos))
    return sorted(datos, key=lambda x: x[0])  

def construir_modelo_markov(datos):
    transiciones = defaultdict(int)
    total_transiciones = defaultdict(int)

    for i in range(len(datos) - 1):
        dia_actual, estado_actual = datos[i]
        dia_siguiente, estado_siguiente = datos[i + 1]

        if dia_siguiente == dia_actual + 1:  # Caso de si son dias exclusivos
            transiciones[(estado_actual, estado_siguiente)] += 1
            total_transiciones[estado_actual] += 1

    # Construye matriz de transicion
    modelo = defaultdict(dict)
    for (estado_origen, estado_destino), conteo in transiciones.items():
        modelo[estado_origen][estado_destino] = conteo / total_transiciones[estado_origen]

    return modelo

def imprimir_modelo(modelo):
    print("Modelo de Markov: Matriz de Transición\n")
    for origen, destinos in sorted(modelo.items()):
        origen_str = " - ".join(origen)
        print(f"Estado actual: {origen_str}")
        print("  Transiciones posibles:")
        for destino, prob in sorted(destinos.items(), key=lambda x: -x[1]):
            destino_str = " - ".join(destino)
            print(f"    → {destino_str.ljust(25)} Probabilidad: {prob:.4f}")
        print("-" * 50)


if __name__ == "__main__":
    ruta_csv = "datos.csv"  
    datos = cargar_datos_csv(ruta_csv)
    modelo = construir_modelo_markov(datos)
    imprimir_modelo(modelo)
