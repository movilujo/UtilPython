# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
#  AUTOR:  Jose Luis Villarejo (@movilujo)
#  FECHA:  Dic-2016
#  TIPO:   Clase
#  NOMBRE: bresenham2D
#  VERSION: 0.1
#
#
#  Clase para describir y calcular trayectorias en 2D
#
#--------------------------------------------------------

class bresenham2D():

    def __init__(self, Xold, Yold, Xnew, Ynew):
        DistX = abs(Xnew - Xold)
        DistY = abs(Ynew - Yold)

        if (DistX >= DistY):
            self.NPixels = DistX + 1
            self.Decide = (2 * DistY) - DistX
            self.Incrd1 = DistY * 2
            self.Incrd2 = (DistY - DistX) * 2
            self.IncrXold = 1
            self.IncrXnew = 1
            self.IncrYold = 0
            self.IncrYnew = 1
        else:
            self.NPixels = DistY + 1
            self.Decide = (2 * DistX) - DistY
            self.Incrd1 = DistX * 2
            self.Incrd2 = (DistX - DistY) * 2
            self.IncrXold = 0
            self.IncrXnew = 1
            self.IncrYold = 1
            self.IncrYnew = 1

        if (Xold > Xnew):
            self.IncrXold = -self.IncrXold
            self.IncrXnew = -self.IncrXnew


        if (Yold > Ynew):
            self.IncrYold = -self.IncrYold
            self.IncrYnew = -self.IncrYnew
