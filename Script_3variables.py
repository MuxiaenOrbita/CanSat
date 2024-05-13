from midiutil import MIDIFile
from math import log

def frecuencia_a_nota(frecuencia):
    # Fórmula para convertir frecuencia a nota MIDI
    nota_midi = 12 * (log(frecuencia / 440) / log(2)) + 69
    return int(nota_midi)

def calcular_frecuencia(temperatura, temperatura_min, temperatura_max, frecuencia_min, frecuencia_max):
    # Calcular frecuencia asegurando que esté en el rango especificado
    if temperatura < temperatura_min:
        # Asignar la frecuencia mínima si la temperatura es menor que la mínima conocida
        frecuencia = frecuencia_min
    elif temperatura > temperatura_max:
        # Asignar la frecuencia máxima si la temperatura es mayor que la máxima conocida
        frecuencia = frecuencia_max
    else:
        # Escala lineal entre la temperatura mínima y máxima
        rango_temperatura = temperatura_max - temperatura_min
        rango_frecuencia = frecuencia_max - frecuencia_min
        frecuencia = ((temperatura - temperatura_min) / rango_temperatura) * rango_frecuencia + frecuencia_min

    return frecuencia

def calcular_frecuencia_altitud(altitud, altitud_min, altitud_max, frecuencia_min, frecuencia_max):
    # Calcular frecuencia asegurando que esté en el rango especificado
    if altitud < altitud_min:
        # Asignar la frecuencia mínima si la altitud es menor que la mínima conocida
        frecuencia = frecuencia_min
    elif altitud > altitud_max:
        # Asignar la frecuencia máxima si la altitud es mayor que la máxima conocida
        frecuencia = frecuencia_max
    else:
        # Escala lineal entre la altitud mínima y máxima
        rango_altitud = altitud_max - altitud_min
        rango_frecuencia = frecuencia_max - frecuencia_min
        frecuencia = ((altitud - altitud_min) / rango_altitud) * rango_frecuencia + frecuencia_min

    return frecuencia

def calcular_frecuencia_presion(presion, presion_min, presion_max, frecuencia_min, frecuencia_max):
    # Calcular frecuencia asegurando que esté en el rango especificado
    if presion < presion_min:
        # Asignar la frecuencia mínima si la presión es menor que la mínima conocida
        frecuencia = frecuencia_min
    elif presion > presion_max:
        # Asignar la frecuencia máxima si la presión es mayor que la máxima conocida
        frecuencia = frecuencia_max
    else:
        # Escala lineal entre la presión mínima y máxima
        rango_presion = presion_max - presion_min
        rango_frecuencia = frecuencia_max - frecuencia_min
        frecuencia = ((presion - presion_min) / rango_presion) * rango_frecuencia + frecuencia_min

    return frecuencia

def leer_datos_desde_archivo(nombre_archivo):
    temperaturas = []
    altitudes = []
    presiones = []

    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            valores = linea.strip().split(';')  # Cambiar el separador a punto y coma
            try:
                temperatura = float(valores[1])  # La temperatura está en la segunda columna
                altitud = float(valores[3])  # La altitud está en la cuarta columna
                presion = float(valores[2])  # La presión está en la tercera columna
                temperaturas.append(temperatura)
                altitudes.append(altitud)
                presiones.append(presion)
            except (ValueError, IndexError):
                # Ignorar líneas con valores no válidos o sin suficientes columnas
                pass

    # Calcular temperaturas mínimas y máximas
    temperatura_min = min(temperaturas)
    temperatura_max = max(temperaturas)

    # Calcular altitudes mínimas y máximas
    altitud_min = min(altitudes)
    altitud_max = max(altitudes)

    # Calcular presiones mínimas y máximas
    presion_min = min(presiones)
    presion_max = max(presiones)

    return temperaturas, altitudes, presiones, temperatura_min, temperatura_max, altitud_min, altitud_max, presion_min, presion_max

def generar_archivo_midi(temperaturas, altitudes, presiones, duracion, nombre_archivo_midi="melodia.mid", 
                         frecuencia_min=30, frecuencia_max=7900):
    # Calcular temperaturas mínimas y máximas
    temperatura_min = min(temperaturas)
    temperatura_max = max(temperaturas)

    # Calcular altitudes mínimas y máximas
    altitud_min = min(altitudes)
    altitud_max = max(altitudes)

    # Calcular presiones mínimas y máximas
    presion_min = min(presiones)
    presion_max = max(presiones)

    # Crear archivo MIDI
    mid = MIDIFile(3)  # Crear un archivo MIDI con tres pistas

    # Configurar pistas
    for pista in range(3):
        mid.addTempo(pista, 0, 120)  # Tempo en BPM

    tiempo_inicio = 0
    volumen = 100

    # Pista 0: Temperatura
    canal_temperatura = 0
    for i, temperatura in enumerate(temperaturas):
        frecuencia = calcular_frecuencia(temperatura, temperatura_min, temperatura_max, frecuencia_min, frecuencia_max)
        tiempo_fin = tiempo_inicio + duracion

        # Convertir frecuencia a nota MIDI
        nota_midi = frecuencia_a_nota(frecuencia)

        # Añadir evento de nota a la pista de temperatura
        mid.addNote(
            canal_temperatura,
            0,  # Canal (puede ser cualquier valor ya que estamos usando un sintetizador)
            nota_midi,
            tiempo_inicio,
            tiempo_fin,
            volumen
        )

        tiempo_inicio += duracion

    # Pista 1: Altitud
    canal_altitud = 1
    tiempo_inicio = 0  # Reiniciar tiempo para la segunda pista
    for i, altitud in enumerate(altitudes):
        # Calcular frecuencia de altitud
        frecuencia = calcular_frecuencia_altitud(altitud, altitud_min, altitud_max, frecuencia_min, frecuencia_max)
        tiempo_fin = tiempo_inicio + duracion

        # Convertir frecuencia a nota MIDI
        nota_midi = frecuencia_a_nota(frecuencia)

        # Añadir evento de nota a la pista de altitud
        mid.addNote(
            canal_altitud,
            0,  # Canal (puede ser cualquier valor ya que estamos usando un sintetizador)
            nota_midi,
            tiempo_inicio,
            tiempo_fin,
            volumen
        )

        tiempo_inicio += duracion

    # Pista 2: Presión
    canal_presion = 2
    tiempo_inicio = 0  # Reiniciar tiempo para la tercera pista
    for i, presion in enumerate(presiones):
        # Calcular frecuencia de presión
        frecuencia = calcular_frecuencia_presion(presion, presion_min, presion_max, frecuencia_min, frecuencia_max)
        tiempo_fin = tiempo_inicio + duracion

        # Convertir frecuencia a nota MIDI
        nota_midi = frecuencia_a_nota(frecuencia)

        # Añadir evento de nota a la pista de presión
        mid.addNote(
            canal_presion,
            0,  # Canal (puede ser cualquier valor ya que estamos usando un sintetizador)
            nota_midi,
            tiempo_inicio,
            tiempo_fin,
            volumen
        )

        tiempo_inicio += duracion

    # Escribir el archivo MIDI
    with open(nombre_archivo_midi, "wb") as midi_file:
        mid.writeFile(midi_file)

    # Mostrar temperaturas, altitudes y presiones máximas y mínimas
    print(f"Temperatura mínima: {temperatura_min:.2f} °C")
    print(f"Temperatura máxima: {temperatura_max:.2f} °C")
    print(f"Altitud mínima: {altitud_min:.2f} m")
    print(f"Altitud máxima: {altitud_max:.2f} m")
    print(f"Presión mínima: {presion_min:.2f} hPa")
    print(f"Presión máxima: {presion_max:.2f} hPa")

def generar_archivo_midi_desde_archivo_datos(nombre_archivo_datos, duracion, nombre_archivo_midi="melodia.mid"):
    # Leer datos desde el archivo
    temperaturas, altitudes, presiones, _, _, _, _, _, _ = leer_datos_desde_archivo(nombre_archivo_datos)

    # Generar archivo MIDI
    generar_archivo_midi(temperaturas, altitudes, presiones, duracion, nombre_archivo_midi)

    print(f"Archivo MIDI generado: {nombre_archivo_midi}")

# Nombre del archivo de datos
nombre_archivo_datos = "DATOS1.txt"
duracion = 1  # Duración en segundos para cada nota

# Generar archivo MIDI desde el archivo de datos
generar_archivo_midi_desde_archivo_datos(nombre_archivo_datos, duracion)

