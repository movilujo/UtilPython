# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
#  AUTOR:  Jose Luis Villarejo (@movilujo)
#  FECHA:  Dic-2016
#  TIPO:   Clase
#  NOMBRE: Articulacion
#  VERSION: 0.2
#
#
#  Clase para describir y controlar las articulaciones de
#  un brazo robótico. Debe cargarse el firmware apropiado
#  en la placa arduino o similar que controla los servos
#
#  Inspiraciones y reconocimientos
#  --------------------------------
#
#    Oscillator.py -- Juan Gonzalez-Gomez (obijuan)
#     https://github.com/Obijuan/ArduSnake/blob/master/python/Oscillator.py
#--------------------------------------------------------
import misUtilidades

#--Command definitions
CMD_END = '\r'

class IncorrectAngle():
  pass

class Articulacion(object):
    def __init__(self, sp,  pDir):
        self.sp = sp
        self.dir = pDir
        self._abertura = [0,0]
        self._eje = ''
        self._ang = 0
        self._lng = 0

    def __str__(self):
        str1 = "Articulación: {}\n".format(self._dir)
        str2 = "Serial port: {}".format(self.sp.name)
        return str1 + str2

    def setAng(self, pAng):
        #print 'Angulo entrada: ' + str(pAng)
        pAng = misUtilidades.mapeo(pAng, 0, 180, -90, 90)

        #print 'Angulo mapeado: ' + str(pAng)
    #-- Check that the pos in the range [-90,90]
        if not (-90 <= pAng <= 90):
          raise IncorrectAngle()
          return

        #-- Convert the pos to an integer value
        pAng = int(round(pAng))

        cmd = self.dir + str(pAng) + CMD_END

        #Debug
        print(cmd)

        self.sp.write(cmd)

        self._ang = pAng


#    @property
    def dir(self):
        return self._dir

    @property
    def abertura(self):
        return self._abertura

    @property
    def eje(self):
        return self._eje

    @property
    def ang(self):
        return self._ang

    @property
    def lng(self):
        return self._lng

    def setDir(self, pDir):
        self._dir = pDir

    def setAbertura(self, valor):
        self._abertura = valor

    def setEje(self, pEje):
        self._eje = pEje

    def setLng(self, pLong):
        self._lng = pLong

    def setCabeceo(self, esCab):
        self._cabeceo = esCab

    def minAng(self):
        return self._abertura[0]

    def maxAng(self):
        return self._abertura[1]

    def defArticulacion(self, vAbertura, vEje, vLong):
        self.abertura = vAbertura
        self.eje = vEje
        self.lng = vLong

    @abertura.setter
    def abertura(self, valor):
        self.setAbertura(valor)

    @eje.setter
    def eje(self, pEje):
        self.setEje(pEje)

    @ang.setter
    def ang(self, pAng):
        self.setAng(pAng)

    @lng.setter
    def lng(self, pLong):
        self.setLng(pLong)


