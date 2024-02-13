import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# escuchar nuestro microfono y devolver audio como texto
def transformar_audio_en_texto():
    # almacenar recognizar en variable
    r = sr.Recognizer()

    # configurar microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar!")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-ar")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el error
        except sr.UnknownValueError:
            # prueba de que no comprendio audio
            print("Ups, no entendi")

            # devolver error
            return "Sigo esperando..."

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio audio
            print("Ups, no hay servicio")

            # devolver error
            return "Sigo esperando..."
        # error inesperado
        except:
            # prueba de que no comprendio audio
            print("Ups, algo ha salido mal")

            # devolver error
            return "Sigo esperando..."


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender motor de pyttsx3
    engine = pyttsx3.init()

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


#engine = pyttsx3.init()
#for voz in engine.getProperty('voices'):
#    print(voz)


# informar el dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con dias
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # decir dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar la hora
def pedir_hora():

    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas Noches!'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día!'
    else:
        momento = 'Buenas Tardes!'

    # decir el saludo
    hablar(f'{momento}, Soy Zira, tu asistente personal, Por favor, dime en qué te puedo ayudar?')


# funcion central del asistente
def pedir_cosas():

    # activar el saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso!')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue

            except:
                hablar("Perdón, no lo he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()
