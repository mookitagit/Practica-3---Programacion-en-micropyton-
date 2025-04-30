# TEAM markoboquiñechainajesu

# ESTE CÓDIGO EMPLEA MICROPYTHON PARA REALIZAR UNA LECTURA DE SENSORES EN RASPBAERRY PI PICO Y LOS GUARDA EN UN ARCHIVO CSV.

# 29 / 04 / 2025 - V. 1. 0. 0 - INTEGRACIÓN DE SENSORES Y PROCESAMIENTO DE DATOS CON MICROPYTHON.

import machine
import time
import dht

# Inicialización de pines
sensor_dht = dht.DHT11(machine.Pin(4))       # GP4
pot = machine.ADC(26)                        # GP26 / ADC0

# Archivo CSV
archivo = "datos.csv"

# Sobrescribir archivo al iniciar (limpiar datos anteriores y escribir encabezado)
with open(archivo, "w") as f:
    f.write("Fecha y Hora,Voltaje(V),Temperatura(C),Humedad(%)\n")

while True:
    # Leer ADC (potenciómetro)
    pot_valor = pot.read_u16()               # Valor de 0 a 65535
    voltaje = (pot_valor / 65535.0) * 3.3

    # Leer DHT11
    sensor_dht.measure()
    temperatura = sensor_dht.temperature()
    humedad = sensor_dht.humidity()
    
    #Guarda la fecha y hora (Timestamp)
    timestamp = time.localtime()
    año, mes, dia, hora, minuto, segundo, *_ = timestamp
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(año, mes, dia, hora, minuto, segundo)
    
    # Mostrar en terminal
    print(f"Fecha y hora: {timestamp_str}| Voltaje: {voltaje:.2f} V | Temperatura: {temperatura} °C | Humedad: {humedad} %")

    # Guardar en CSV solo si hay lectura válida
    with open(archivo, "a") as f:
        f.write(f"{timestamp_str}, {voltaje:.2f},{temperatura},{humedad}\n")

    time.sleep(0.5)  # Leer cada medio segundo
