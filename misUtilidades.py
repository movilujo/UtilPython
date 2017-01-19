import serial
import serial.tools.list_ports

# La función mapeo() simula la función map() de Arduino
def mapeo(val, minIn, maxIn, minOut, maxOut):
    return (val - minIn) * (maxOut - minOut) / (maxIn - minIn) + minOut

# La función mapServo() convierte un valor entre 0 y 180 de entrada y lo devuelve en formato -90 y 90
def mapServo(val):
    return val - 90

# Devuelve el nombre del puerto Serie en el que se encuentra conectado la placa arduino
def getSPArduino():
    Puertos = list(serial.tools.list_ports.comports())

    bEncontrado = False
    for i in Puertos:
        if ('USB' in i[1]) or ('Arduino' in i[1]):
            try:
                PUERTO = i[0]
                VELOCIDAD = '9600' #''
                sp = serial.Serial(PUERTO, VELOCIDAD)
                print('Encontrado!!!')
                sp.close()
                bEncontrado = True
                Arduino = i[0]
            except:
                pass

    if bEncontrado:
        return Arduino
    else:
        return 'xxx'