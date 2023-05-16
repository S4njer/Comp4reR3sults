## Python 3.11

import csv
from datetime import datetime, timedelta
import ast
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def obtener_resultados(archivo):
    resultados = []
    with open(archivo, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dominio = row[0]
            fecha_str = row[1]
            try:
                fechas = ast.literal_eval(row[2])
            except (ValueError, SyntaxError):
                fechas = []
            ip = row[3]
            expiracion = row[4] if len(row) >= 5 else ''  # Leer la fecha de expiración si existe, de lo contrario asignar una cadena vacía
            resultados.append((dominio, fecha_str, fechas, ip, expiracion))
    return resultados


def obtener_nombre_archivo_fecha(fecha):
    fecha_str = fecha.strftime("%y%m%d")
    return f"{fecha_str}.domain_results.csv"

def comparar_resultados_hoy_ayer():
    fecha_hoy = datetime.now().date()
    fecha_ayer = fecha_hoy - timedelta(days=1)
    archivo_hoy = obtener_nombre_archivo_fecha(fecha_hoy)
    archivo_ayer = obtener_nombre_archivo_fecha(fecha_ayer)

    resultados_hoy = obtener_resultados(archivo_hoy)
    resultados_ayer = obtener_resultados(archivo_ayer)

    cambios_encontrados = False

    # Comparar los resultados de hoy con los de ayer
    for resultado_hoy in resultados_hoy:
        encontrado = False
        for resultado_ayer in resultados_ayer:
            if resultado_hoy[0] == resultado_ayer[0]:
                if resultado_hoy[1] != resultado_ayer[1] or resultado_hoy[2] != resultado_ayer[2] or resultado_hoy[3] != resultado_ayer[3] or resultado_hoy[4] != resultado_ayer[4]:
                    print(f"{Fore.RED}Dominio: {resultado_hoy[0]} ha cambiado el resultado.")
                    print(f"{Style.BRIGHT}Datos de hoy: {resultado_hoy[1]} | {resultado_hoy[3]} | {resultado_hoy[4]}")
                    print(f"{Style.BRIGHT}Datos de ayer: {resultado_ayer[1]} | {resultado_ayer[3]} | {resultado_ayer[4]}")
                    print(f"{Fore.GREEN}----------------------------------------------")
                    cambios_encontrados = True
                encontrado = True
        break
        if not encontrado:
            print(f"{Fore.GREEN}Dominio: {resultado_hoy[0]} es un resultado nuevo.")
            print(f"{Style.BRIGHT}Datos de hoy: {resultado_hoy[1]} | {resultado_hoy[2]} | {resultado_hoy[3]} | {resultado_hoy[4]}")
            print(f"{Fore.GREEN}----------------------------------------------")
            cambios_encontrados = True

    # Mostrar resultados de ayer que no están presentes hoy
    for resultado_ayer in resultados_ayer:
        encontrado = False
        for resultado_hoy in resultados_hoy:
            if resultado_ayer[0] == resultado_hoy[0]:
                encontrado = True
                break
        if not encontrado:
            print(f"{Fore.RED}Dominio: {resultado_ayer[0]} ya no está presente hoy.")
            print(f"{Style.BRIGHT}Datos de ayer: {resultado_ayer[1]} | {resultado_ayer[2]} | {resultado_ayer[3]}")
            print(f"{Fore.GREEN}----------------------------------------------")
            cambios_encontrados = True

    if not cambios_encontrados:
        print(f"{Fore.RED}[{Fore.YELLOW}+{Fore.RED}]{Fore.WHITE} {Fore.GREEN}No se encontraron cambios entre los resultados de hoy y los de ayer.")

# Ejemplo de uso
comparar_resultados_hoy_ayer()
