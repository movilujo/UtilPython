import serial
import serial.tools.list_ports

def mapeo(val, minIn, maxIn, minOut, maxOut):
    return (val - minIn) * (maxOut - minOut) / (maxIn - minIn) + minOut

def mapServo(val):
    return val - 90

def getSPArduino():
    Puertos = list(serial.tools.list_ports.comports())

    bEncontrado = False
    for i in Puertos:
        if ('USB' in i[1]) or ('Arduino' in i[1]):
            try:
                PUERTO = i[0]
                VELOCIDAD = '9600' \
                            ''
                sp = serial.Serial(PUERTO, VELOCIDAD)
                print('Conectado!!!')
                sp.close()
                bEncontrado = True
                Arduino = i[0]
            except:
                pass

    if bEncontrado:
        return Arduino
    else:
        return 'xxx'