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
    Zbrac.py rassemble la définition des classes:
        Zbrac
"""

import sys
import pathlib

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Classe permettant de calculer un encadrement de la solution à partir d'un point
class Zbrac:

    """

        Classe Zbrac
        ============

        La classe Zbrac permet d'obtenir un encadrement de la solution
        d'une fonction à partir d'un seul point fX.
        il est souhaitable que la fonction soit gentiment monotone
        on applique la technique suivante :
        dans un diagramme x-fx selon C ou D
           |
        */ | /*
        -------
        /* | */
           |

        :Example:

        >>> def f(x): return (2.*x-1.)*(2.*x+1.)
        >>> Zc = Zbrac(f)
        >>> Zc.solve(5., 'C')
        0
        >>> Zc.getFresult()
        (0.625, 0.3125)
        >>> Zc.getNiters()
        5

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    __iter = 20
    __factor = 2.
    __sens1 = {'C':1./__factor, 'D':__factor}
    __sens2 = {'C':__factor, 'D':1./__factor}

    #-----
    def __init__(self, func, *param) -> None:

        self.func = func
        self.param = param

        self.nError = 0
        self.nIter = 0

        self.fX0 = 0.
        self.fX1 = 0.

        self.fY0 = 0.
        self.fY1 = 0.

    #-----
    def solve(self, fX: float, sSens: str) -> int:

        """
            lance le solveur avec un paramètre

            :param fX: borne
            :type fX: float
            :param sSens: sens 'C' croissant 'D' décroissant
            :type sSens: string
            :return: 0 ok 1 pas ok
            :rtype: int

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zc = Zbrac(f)
            >>> Zc.solve(5., 'E')
            Mauvaise indication du sens
            1
            >>> Zc.solve(5., 'C')
            0
            >>> Zc.solve(-5., 'D')
            0

        """

        if sSens not in ('C', 'D'):

            print(f'Mauvaise indication du sens')
            self.nError = 1
            return self.nError

        self.nIter = 1
        self.fX0 = fX
        self.fY0 = self.func(self.fX0, *self.param)
        while self.nIter < Zbrac.__iter:

            if self.fX0*self.fY0 > 0.:

                self.fX1 = self.fX0*Zbrac.__sens1[sSens]

            else:

                self.fX1 = self.fX0*Zbrac.__sens2[sSens]

            self.fY1 = self.func(self.fX1, *self.param)
            self.nIter += 1

            if self.fY0*self.fY1 > 0.:

                self.fX0 = self.fX1
                self.fY0 = self.fY1

            else:

                self.nError = 0
                return self.nError

        print(f'Maximum number of iterations exceeded in zbrac')
        self.nError = 1
        return self.nError

    #-----
    def getFresult(self) -> (float, float):

        """
            retourne le résultat
            nécessite d'avoir lancer le solve et d'avoir tester le code erreur

            :param: aucun
            :return: le résultat
            :rtype: liste de 2 float

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zc = Zbrac(f)
            >>> Zc.solve(5., 'C')
            0
            >>> Zc.getFresult()
            (0.625, 0.3125)
            >>> Zc.solve(-5., 'D')
            0
            >>> Zc.getFresult()
            (-0.625, -0.3125)

        """

        return (self.fX0, self.fX1)

    #-----
    def getNiters(self) -> int:

        """
            retourne le nombre d'itérations effectuées
            nécessite d'avoir lancer le solve et d'avoir tester le code erreur

            :param: aucun
            :return: le nombre d'itérations
            :rtype: int

            >>> def f(x): return (2.*x-1.)*(2.*x+1.)
            >>> Zc = Zbrac(f)
            >>> Zc.solve(5., 'C')
            0
            >>> Zc.getNiters()
            5
            >>> Zc.solve(-5., 'D')
            0
            >>> Zc.getNiters()
            5

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
