"""
Actividad 5.2
"""
import json
import time
import sys
from collections import defaultdict




def cargar_archivo_json(archivo):
    """
    Definición para cargar el archivo json desde consola
    En la tarea pasada dejaba que el usuario eligiera desde consola,
    Esta ocasión se setean los datos desde consola,
    hay algun tema con eso?
    :param archivo: Path del json
    :return: Json
    """
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No se pudo cargar el archivo {archivo}: {e}")
        return None


def calcular_costo_venta(venta, catalogo_precios):
    """
    Se hace la sumatoria acumulandola por venta
    :param venta:
    :param catalogo_precios:
    :return: el total
    """
    costo_total = 0
    for producto in venta['products']:
        nombre_producto = producto['Product']
        cantidad = producto['Quantity']

        for item in catalogo_precios:
            if item['title'] == nombre_producto:
                costo_total += item['price'] * cantidad
                break
    return costo_total


def main():
    """

    :return: Procesamiento de archivos de entrada
    """
    if len(sys.argv) != 3:
        print("Se debe correr desde consola el programa."
              "Pasando como parametros el archivo .py, PriceCatalogue y "
              "el SalesRecord")
        return

    archivo_catalogo = sys.argv[1]
    archivo_ventas = sys.argv[2]

    catalogo_precios = cargar_archivo_json(archivo_catalogo)
    if catalogo_precios is None:
        return

    ventas = cargar_archivo_json(archivo_ventas)
    if ventas is None:
        return

    inicio_tiempo = time.time()

    ventas_agrupadas = defaultdict(list)
    for venta in ventas:
        ventas_agrupadas[venta['SALE_ID']].append({
            'Product': venta['Product'],
            'Quantity': venta['Quantity']
        })

    total_general = 0
    resultados = []

    for sale_id, productos in ventas_agrupadas.items():
        venta = {'SALE_ID': sale_id, 'products': productos}
        costo_venta = calcular_costo_venta(venta, catalogo_precios)
        total_general += costo_venta
        resultados.append(f"ID de la venta: {sale_id} | Costo total: {costo_venta:.2f} USD")

    tiempo_transcurrido = time.time() - inicio_tiempo

    print("\nResultados de las ventas:")
    for resultado in resultados:
        print(resultado)

    print(f"\nCosto total de todas las ventas: {total_general:.2f} USD")
    print(f"Tiempo de procesamiento: {tiempo_transcurrido:.2f} segundos")

    with open("SalesResults.txt", 'w', encoding='utf-8') as archivo_salida:
        for resultado in resultados:
            archivo_salida.write(resultado + "\n")
        archivo_salida.write(f"\nCosto total de todas las ventas: {total_general:.2f} USD\n")
        archivo_salida.write(f"Tiempo de procesamiento: {tiempo_transcurrido:.2f} segundos\n")

    print("Los resultados se han guardado en el archivo 'SalesResults.txt'")


if __name__ == "__main__":
    main()
