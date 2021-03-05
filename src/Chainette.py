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
    Chainette.py rassemble la définition des classes:
        Chainette
            Chainettedict(Chainette)
"""

import sys
import pathlib
import math

import Zbrac as zc
import Zbrent as zb

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Class Chainette
class Chainette:

    """

        Classe Chainette
        ================

        La classe Chainette décrit une fonction chainette
        La fonction chainette ==> a*cosh(x/a)
        On retranche a pour avoir f(0)=0 ==> a*cosh(x/a)-a
        On retranche c le creux pour avoir f(0)=-c ==> a*(cosh(x/a)-1)-c

        :datas:

            self.fA:  float
            self.fC:  float

        :Example:

        >>> c = Chainette(fA=10.,fC=5.)
        >>> print(c)
        Chainette --> A = 10.0, C = 5.0

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fA: float = 1., fC: float = 1.) -> None:

        self.fA = fA
        self.fC = fC

    #-----
    def comp(self, fX: float) -> float:

        """
            retourne le calcul de la chainette à un point donné

            :param: float
            :rtype: float

            :Example:

            >>> a = Chainette(fA=10., fC=1.)
            >>> a.comp(fX=0.)
            -1.0
            >>> a.comp(fX=4.)
            -0.18927628161545051
            >>> a.comp(fX=5.)
            0.276259652063807

        """

        return self.fA*(math.cosh(fX/self.fA)-1.)-self.fC

    #-----
    def compBis(self, fX:float, fD:float) -> float:

        """
            nous avons également besoin de la fonction associée
            y = x * (cosh(d/x) - 1) - c

            :param: float
            :rtype: float

            :Example:

            >>> a = Chainette(fA=10., fC=1.)
            >>> a.compBis(fX=10., fD=0.)
            -1.0
            >>> a.compBis(fX=10., fD=2.)
            -0.7993324438092411
            >>> a.compBis(fX=10., fD=5.)
            0.276259652063807

        """

        self.fA = fX
        return self.comp(fD)

    #-----
    def compCurv(self, fX: float= 0.) -> float:

        """
            retourne le calcul de l'abscisse curviligne (sa longueur)
            de la chainette pour un point donné

            :param: float
            :rtype: float

            :Example:

            >>> a = Chainette(fA=10.)
            >>> a.compCurv(fX=0.)
            0.0
            >>> a.compCurv(fX=4.)
            4.107523258028155
            >>> a.compCurv(fX=5.)
            5.210953054937474

        """

        return self.fA*(math.sinh(fX/self.fA))

    #-----
    def __str__(self) -> None:

        return f'Chainette --> A = {self.fA}, C = {self.fC}'

#----- Class Chainettedict
class Chainettedict(Chainette):

    """

        Classe Chainettedict
        ====================

        La classe Chainettedict représente une chainette construite par dict
        En fait il s'agit, pour un creux donné et un écartement donné,
        de trouver le "a" de la chainette
        l'écartement est l'écartement "total" entre les 2 "zéros"

        :datas:

            self.dictChainette: dict
            self.fDist:         float
            self.fCreux:        float
            self._oK:           boolean
            self.fA:            float

        :Example:

        >>> a = Chainettedict({"creux":1.,"ecartement":8.87136508906719})
        >>> print(a)
        Chainette --> A = 10.00000000474504, C = 1.0
        >>> b = Chainettedict({"creux":0,"ecartement":8.87136508906719})

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictChainette: dict) -> None:

        self.dictChainette = dictChainette

        # ecartement : obligatoire
        if "ecartement" in self.dictChainette:
            self.fDist = self.dictChainette["ecartement"]/2.
        else:
            print(f'< !!!! > Pas de clé "ecartement" dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # creux : obligatoire
        if "creux" in self.dictChainette:
            self.fCreux = self.dictChainette["creux"]
        else:
            print(f'< !!!! > Pas de clé "creux" dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        Chainette.__init__(self, fA=1., fC=self.fCreux)

        self._oK = False

        # on effectue le calcul d'optimisation qu'à la condition que fCreux ne soit pas nul
        # sinon la chainette est dégénérée en droite
        if self.fCreux != 0.:

            self._oK = True
            zBrac = zc.Zbrac(self.compBis, self.fDist)
            if zBrac.solve(self.fDist/2., "D") != 0:

                print(f'Encadrement non trouvé pour la chainette --> voile inconstructible')
                print(f'd = {self.fDist} c = {self.fCreux}')
                sys.exit(ABNORMAL_TERMINATION)

            #print(f'Nombre d\'itérations zchainette = {zBrac.getNiters():d}')
            (fX1, fX2) = zBrac.getFresult()

            fErr = 1.e-8
            zBrent = zb.Zbrent(self.compBis, fErr, self.fDist)
            if zBrent.solve(fX1, fX2) != 0:

                print(f'Pas de solution pour la chainette --> voile inconstructible')
                print(f'x1 = {fX1} x2 = {fX2}')
                print(f'd = {self.fDist} c = {self.fCreux}')
                sys.exit(ABNORMAL_TERMINATION)

            #print(f'Nombre d\'itérations chainette = {zBrent.getNiters():d}')
            self.fA = zBrent.getFresult()

    #-----
    def comp(self, fX: float) -> float:

        """ fonction comp qui traite les 2 cas (chainette ou droite) """

        if self._oK:
            return Chainette.comp(self, fX=fX)
        return 0.

    #-----
    def compCurv(self, fX: float= 0.) -> float:

        """ fonction compCurv qui traite les 2 cas (chainette ou droite) """

        if self._oK:
            return Chainette.compCurv(self, fX=fX)
        return fX

    #-----
    def getDict(self) -> dict:

        """ retourne la description de la chainette """

        return {"a": self.fA, "l": 2.*self.compCurv(self.fDist)}

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
