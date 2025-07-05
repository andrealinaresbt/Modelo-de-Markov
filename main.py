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

def predecir_estado_siguiente(modelo):
    print("\nConsulta interactiva")
    print("Ingresa una combinación de atributos (por ejemplo: soleado frío)")
    print("Escribe 'salir' para terminar.\n")

    while True:
        entrada = input("Estado actual (clima temperatura): ").strip()
        if entrada.lower() == 'salir':
            print("Saliendo del modo interactivo.")
            break

        partes = entrada.split()
        if len(partes) != 2:
            print("Por favor, ingresa exactamente dos valores separados por espacio (ej: soleado frío)")
            continue

        estado_actual = tuple(partes)
        if estado_actual not in modelo:
            print(f"No hay datos suficientes para predecir desde el estado: {estado_actual}")
            continue

        print(f"\nDesde el estado {estado_actual[0]} - {estado_actual[1]}, las posibles transiciones son:")
        for destino, prob in sorted(modelo[estado_actual].items(), key=lambda x: -x[1]):
            print(f"  → {destino[0]} - {destino[1]} con probabilidad {prob:.4f}")
        print()


if __name__ == "__main__":
    ruta_csv = "datos.csv"  
    datos = cargar_datos_csv(ruta_csv)
    modelo = construir_modelo_markov(datos)
    imprimir_modelo(modelo)
    predecir_estado_siguiente(modelo)
