#-----------------------------------------------------------------------
#  AUTOR:  Jose Luis Villarejo (@movilujo)
#  FECHA:  Dic-2016
#  TIPO:   Clase
#  NOMBRE: Brazobot3GL
#  VERSION: 0.1
#
#
#  Clase para describir y controlar  un brazo robótico de
#  3 Grados de Libertad (3GL).
#
#--------------------------------------------------------
# -*- coding: utf-8 -*-

from ArticulacionV2 import Articulacion
from bresenham2D import bresenham2D
import misUtilidades
import math
from time import sleep

class Brazobot3GL():
    nGL = 3

    def __init__(self, sp, alt, conCab='Y', angCab = 90):
        self.__Art = [object,object,object]

        self.__Art[0] = Articulacion(sp, 'a')
        self.__Art[1] = Articulacion(sp, 'b')
        self.__Art[2] = Articulacion(sp, 'c')

        self.Brazo = self.__Art[0]
        self.AnteBrazo = self.__Art[1]
        self.Muneca = self.__Art[2]

        self._X = 100
        self._Y = 100 + alt
        self._H = alt
        self.esCabeceo = conCab
        self.cabeceo = angCab

 ##       self.posXY(self._X, self._Y)

## -----------------------------------
##  Métodos Setter and Getter
## -----------------------------------
    def getnGL(self):
        return self.nGL

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def H(self):
        return self._H

    def setX(self, pX):
        self._X = pX

    def setY(self, pY):
        self._Y = pY

    def setH(self, pH):
        self._H = pH

    @X.setter
    def X(self,valor):
        self.setX(valor)

    @Y.setter
    def Y(self,valor):
        self.setY(valor)

    @H.setter
    def H(self,valor):
        self.setH(valor)

    def __setArticulacion(self, i, v1, v2, v3):
        vAbertura = [misUtilidades.mapServo(v1[0]), misUtilidades.mapServo(v1[1])]
#        self.__Art[i].defArticulacion(v1, v2, v3)
        self.__Art[i].defArticulacion(vAbertura, v2, v3)


    def __setAng(self, i, valor):
        self.__Art[i].ang = valor

# Métodos para definir/describir cada una de las articulaciones
    def setBrazo(self, pAbertura, pLong):
        self.__setArticulacion(0, pAbertura, 'Y', pLong)

    def setAnteBrazo(self, pAbertura, pLong, pCabeceo = 'N'):
        self.__setArticulacion(1, pAbertura, 'Y', pLong)

    def setMuneca(self, pAbertura, pLong, pCabeceo = 'N'):
        self.__setArticulacion(2, pAbertura, 'Y', pLong)

# Método para posicionar el brazo robótico por Cinematica Directa (DK - Direct Kinematic)

    def posDK(self, ang1, ang2, ang3):
        self.__setAng(0, ang1)
        self.__setAng(1, ang2)
        self.__setAng(2, ang3)

# Método para posicionar el brazo robótico por Cinematica Inversa (IK - Inverse Kinematic)

    def posIK(self, vX, vY):
        self.X = vX
        self.Y = vY
        self.getIK()

# Método para posicionar el brazo robótico por Cinematica Inversa & Trayectos

    def posXYTray(self, vX, vY):
        trayecto = bresenham2D(self.X, self.Y, vX, vY)
        print(trayecto.NPixels)  # para depuración
        for i in range(1, trayecto.NPixels):
            print('X: ' + str(self.X) + ' Y: ' + str(self.Y))
            if (trayecto.Decide < 0):
                trayecto.Decide = trayecto.Decide + trayecto.Incrd1
                self.X = self.X + trayecto.IncrXold
                self.Y = self.Y + trayecto.IncrYold
            else:
                trayecto.Decide = trayecto.Decide + trayecto.Incrd2
                self.X = self.X + trayecto.IncrXnew
                self.Y = self.Y + trayecto.IncrYnew
            try:
                self.getIK()
            except:
                pass

#            sleep(0.1)

# Método para el calculo de cinemática inversa

    def getIK(self):

#        print('En getIK')
        Afx = math.cos(math.radians(self.cabeceo)) * self.Muneca.lng
        ladoB = self.X - Afx
        Afy = math.sin(math.radians(self.cabeceo)) * self.Muneca.lng
        ladoA = self.Y - Afy - self.H
        hipo = math.sqrt(math.pow(ladoA,2)+math.pow(ladoB,2))
        Alfa = math.atan2(ladoA, ladoB)
#        print ('Alfa: ' + str(Alfa))
        try:
#            print ('Beta: ' + str((math.pow(self.Brazo.lng,2)-math.pow(self.AnteBrazo.lng,2)+math.pow(hipo,2))/(2*self.Brazo.lng*hipo)))
            Beta = math.acos((math.pow(self.Brazo.lng,2)-math.pow(self.AnteBrazo.lng,2)+math.pow(hipo,2))/(2*self.Brazo.lng*hipo))
#            print ('AlfaBeta: ' + str(math.degrees(Alfa + Beta)))
            if (math.degrees(Alfa + Beta) >= 0):
                angBrazo = math.degrees(Alfa + Beta)
            else:
                angBrazo = 90 + math.degrees(Alfa + Beta)

            if ((misUtilidades.mapServo(angBrazo) >= self.Brazo.minAng()) and (misUtilidades.mapServo(angBrazo) <= self.Brazo.maxAng())):
                self.Brazo.ang = angBrazo
                print ('Grados Brazo: ' + str(self.Brazo.ang))
            else:
                print ('Valores fuera de los limites del Brazo: ' + str(self.X) + ' - ' + str(self.Y))
                print ('Grados Brazo: ' + str(self.Brazo.ang))

            try:
                Gamma = math.acos((math.pow(self.Brazo.lng,2)+math.pow(self.AnteBrazo.lng,2)-math.pow(hipo,2))/(2*self.Brazo.lng*self.AnteBrazo.lng))
#                print ('Gamma: ' + str(Gamma))
#                angAntebrazo = misUtilidades.mapServo(math.degrees(Gamma))
#                print ('Grados AnteBrazo: ' + str(math.degrees(Gamma)))
                angAntebrazo = math.degrees(Gamma)
                if ((misUtilidades.mapServo(angAntebrazo) >= self.AnteBrazo.minAng()) and (misUtilidades.mapServo(angAntebrazo) <= self.AnteBrazo.maxAng())):
                    self.AnteBrazo.ang = angAntebrazo
                    print ('Grados AnteBrazo: ' + str(self.AnteBrazo.ang))
                else:
                    print ('Valores fuera de los limites del AnteBrazo: ' + str(self.X) + ' - ' + str(self.Y))
                    print ('Grados AnteBrazo: ' + str(self.AnteBrazo.ang))

#                angMuneca = misUtilidades.mapServo((270 -(self.Brazo.ang + self.AnteBrazo.ang - self.cabeceo)))
#                angMuneca = (270 -(self.Brazo.ang + self.AnteBrazo.ang - self.cabeceo))
                angMuneca = (270 -(angBrazo + angAntebrazo - self.cabeceo))
#                print('angMuneca: ' + str(angMuneca))
                if ((misUtilidades.mapServo(angMuneca) >= self.Muneca.minAng()) and (misUtilidades.mapServo(angMuneca) <= self.Muneca.maxAng())):
                    self.Muneca.ang = angMuneca
                    print ('Grados Muneca: ' + str(self.Muneca.ang))
                elif (misUtilidades.mapServo(angMuneca) < self.Muneca.minAng()):
                    self.Muneca.ang = self.Muneca.minAng()
                    print ('Grados Muneca: ' + str(self.Muneca.ang))
                else:
                    self.Muneca.ang = self.Muneca.maxAng()
                    print ('Grados Muneca: ' + str(self.Muneca.ang))

            except:
                print ("2.- Triángulo imposible")
                raise
        except:
            print ("1.- Triángulo imposible")
            raise
