#! /bin/env python3
# -*- coding: utf-8 -*-

################################################################################
#
#   This file is part of PYJUNK.
#
#   Copyright © 2021 Marc JOURDAIN
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the “Software”),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
#   You should have received a copy of the MIT License
#   along with PYJUNK.  If not, see <https://mit-license.org/>.
#
################################################################################

"""
    Zbrent.py rassemble la définition des classes:
        Zbrent
"""

import sys
import pathlib

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Classe pour rechercher le zéro d'une fonction entre 2 bornes
class Zbrent:

    """

        Classe Zbrent
        =============

        La classe Zbrent permet de trouver le zéro d'une fonction.
        Cet algorithme est inspiré des Numerical Recipes
        chapitre 9.3 Van Wijngaarden-Dekker-Brent Method
        page 359-362 dans Numerical Recipes in C

        :Example:

        >>> def f(x): return (2.*x-1.)*(2.*x+1.)
        >>> Zb = Zbrent(f, 1.e-8)
        >>> Zb.solve(0.3, 1.3)
        0
        >>> Zb.getFresult()
        0.4999999993823022
        >>> Zb.getNiters()
        6
        >>> Zb.solve(2.,3.)
        a =  2.0 fa =  15.0
        b =  3.0 fb =  35.0
        error in zbrent
        1

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    __itmax = 100
    __eps = 3.e-12

    #-----
    def __init__(self, func, fErr:float, *param) -> None:

        self.func = func
        self.fErr = fErr
        self.param = param

        self.nError = 0
        self.fResult = 0.
        self.nIter = 0

        self.fA = 0.
        self.fB = 0.
        self.fC = 0.
        self.fD = 0.
        self.fE = 0.
        self.fS = 0.
        self.fP = 0.
        self.fQ = 0.
        self.fR = 0.

        self.fXm = 0.

        self.fFa = 0.
        self.fFb = 0.
        self.fFc = 0.

        self.tol1 = 0.

    #-----
    def solve(self, fX1:float, fX2:float) -> int:

        """
            lance le solveur entre deux bornes

            :param fX1: borne 1
            :param fX2: borne 2
            :type fX1: float
            :type fX2: float
            :return: 0 ok 1 pas ok
            :rtype: int

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zb = Zbrent(f, 1.e-8)
            >>> Zb.solve(0.3, 1.3)
            0
            >>> Zb.solve(2.,3.)
            a =  2.0 fa =  15.0
            b =  3.0 fb =  35.0
            error in zbrent
            1

        """

        self.fA = fX1
        self.fB = fX2
        self.fC = fX2

        self.fFa = self.func(self.fA, *self.param)
        self.fFb = self.func(self.fB, *self.param)

        if (self.fFa > 0. and self.fFb > 0.) or (self.fFa < 0. and self.fFb < 0.):

            print('a = ', self.fA, 'fa = ', self.fFa)
            print('b = ', self.fB, 'fb = ', self.fFb)
            print('error in zbrent')
            self.nError = 1
            return self.nError

        self.fFc = self.fFb

        while self.nIter < Zbrent.__itmax:

            if (self.fFb > 0. and self.fFc > 0.) or (self.fFb < 0. and self.fFc < 0.):

                self.fC = self.fA
                self.fFc = self.fFa
                self.fD = self.fB - self.fA
                self.fE = self.fD

            if abs(self.fFc) < abs(self.fFb):

                self.fA = self.fB
                self.fB = self.fC
                self.fC = self.fA
                self.fFa = self.fFb
                self.fFb = self.fFc
                self.fFc = self.fFa

            self.tol1 = 2.*Zbrent.__eps*abs(self.fB) + .5*self.fErr
            self.fXm = .5*(self.fC - self.fB)

            if (abs(self.fXm) <= self.tol1) or (self.fFb == 0.):

                self.nError = 0
                self.fResult = self.fB
                return self.nError

            if (abs(self.fE) >= self.tol1) and (abs(self.fFa) > abs(self.fFb)):

                self.fS = self.fFb/self.fFa

                if self.fA == self.fC:

                    self.fP = 2.*self.fXm*self.fS
                    self.fQ = 1. - self.fS

                else:

                    self.fQ = self.fFa/self.fFc
                    self.fR = self.fFb/self.fFc
                    self.fP = self.fS*(2.*self.fXm*self.fQ*(self.fQ - self.fR) - \
                                        (self.fB - self.fA)*(self.fR - 1.))
                    self.fQ = (self.fQ - 1.)*(self.fR - 1.)*(self.fS - 1.)

                if self.fP > 0.:

                    self.fQ = -self.fQ

                self.fP = abs(self.fP)

                if 2.*self.fP < min(3.*self.fXm*self.fQ - abs(self.tol1*self.fQ),
                                     abs(self.fE*self.fQ)):

                    self.fE = self.fD
                    self.fD = self.fP/self.fQ

                else:

                    self.fD = self.fXm
                    self.fE = self.fD

            else:

                self.fD = self.fXm
                self.fE = self.fD

            self.fA = self.fB
            self.fFa = self.fFb

            if abs(self.fD) > self.tol1:

                self.fB += self.fD

            else:

                if self.fXm >= 0.:

                    self.fB += abs(self.tol1)

                else:

                    self.fB += -abs(self.tol1)

            self.fFb = self.func(self.fB, *self.param)
            self.nIter += 1

        print(f'Maximum number of iterations exceeded in zbrent')
        self.nError = 1
        return self.nError

    #-----
    def getFresult(self) -> float:

        """
            retourne le résultat
            nécessite d'avoir lancer le solve et d'avoir tester le code erreur

            :param: aucun
            :return: le résultat
            :rtype: float

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zb = Zbrent(f, 1.e-8)
            >>> Zb.solve(0.3, 1.3)
            0
            >>> Zb.getFresult()
            0.4999999993823022

        """

        return self.fResult

    #-----
    def getNiters(self) -> int:

        """
            retourne le nombre d'itérations effectuées
            nécessite d'avoir lancer le solve et d'avoir tester le code erreur

            :param: aucun
            :return: le nombre d'itérations
            :rtype: int

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zb = Zbrent(f, 1.e-8)
            >>> Zb.solve(0.3, 1.3)
            0
            >>> Zb.getNiters()
            6

        """

        return self.nIter

#----- start here
if __name__ == '__main__':

    import doctest

    (failureCount, testCount) = doctest.testmod(verbose=False)

    print(f'nombre de tests : {testCount:>3d}, nombre d\'erreurs : {failureCount:>3d}', end='')

    if failureCount != 0:
        print(f' --> Arrêt du programme {pathlib.Path(__file__)}')
        sys.exit(ABNORMAL_TERMINATION)
    else:
        print(f' --> All Ok {pathlib.Path(__file__)}')
        sys.exit(NORMAL_TERMINATION)
