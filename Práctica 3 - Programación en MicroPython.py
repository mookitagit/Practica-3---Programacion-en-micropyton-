# TEAM markoboquiñechainajesu

# ESTE CÓDIGO EMPLEA MICROPYTHON PARA REALIZAR UNA LECTURA DE SENSORES EN RASPBAERRY PI PICO Y LOS GUARDA EN UN ARCHIVO CSV.

# 30 / 04 / 2025 - V. 2. 0. 0 - INTEGRACIÓN DE SENSORES Y PROCESAMIENTO DE DATOS CON MICROPYTHON.

import machine # Librería para controlar hardware como pines
import time # Librería para trabajar con tiempo y fechas
import dht # Librería para interactuar con el sensor DHT11

# Inicialización de pines
sensor_dht = dht.DHT11(machine.Pin(4))       # GP4
pot = machine.ADC(26)                        # GP26 / ADC0
sensor_sonido = machine.ADC(27)              # GP27 / ADC1

# Archivo CSV
archivo = "datos.csv" # Nombre del archivo donde se guardará

# Sobrescribir archivo al iniciar (limpiar datos anteriores y escribir encabezado)
with open(archivo, "w") as f:  # Abre el archivo en modo escritura para limpiarlo y crear encabezados
    f.write("Fecha y Hora,Voltaje(V),Temperatura(C),Humedad(%), Sonido\n") # Encabezados de columnas


while True:
    # Leer ADC (potenciómetro)
    pot_valor = pot.read_u16()               # Valor de 0 a 65535
    voltaje = (pot_valor / 65535.0) * 3.3 # Conversión del valor leído a voltaje real en el rango de 0 a 3.3V

    # Leer DHT11
    sensor_dht.measure() # Solicita al sensor DHT11 que realice una medición de temperatura y humedad
    temperatura = sensor_dht.temperature() # Obtiene la temperatura medida por el DHT11 y la guarda en la variable 'temperatura'
    humedad = sensor_dht.humidity() # Obtiene la humedad relativa medida por el DHT11 y la guarda en la variable 'humedad'
    
    #Leer RQ-S001
    sonido_valor = sensor_sonido.read_u16()  # Lee el valor del sensor de sonido
    
    #Guarda la fecha y hora (Timestamp)
    timestamp = time.localtime() # Estás obteniendo la fecha y hora local actual
    año, mes, dia, hora, minuto, segundo, *_ = timestamp #descompone los primeros seis elementos del objeto 
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(año, mes, dia, hora, minuto, segundo) #convierte los valores numéricos de fecha y hora en una cadena con formato legible
    
    # Mostrar en terminal
    print(f"Fecha y hora: {timestamp_str}| Voltaje: {voltaje:.2f} V | Temperatura: {temperatura} °C | Humedad: {humedad}% | Sonido: {sonido_valor}") #imprime un mensaje formateado y legible con información de fecha, hora y diversas mediciones

    # Guardar en CSV solo si hay lectura válida
    with open(archivo, "a") as f: #bre un archivo en modo "append" (adición) para escribir datos sin borrar lo anterior
        f.write(f"{timestamp_str}, {voltaje:.2f},{temperatura},{humedad}, {sonido_valor}\n") #escribe una línea de datos en formato CSV, con valores separados por comas
 
    time.sleep(0.5)  # Leer cada medio segundo
