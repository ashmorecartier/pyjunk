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
    Models.py rassemble la définition des classes:
        Model
            ModelFlat(Model)
            ModelParabolique(Model)
            ModelTube(Model)
        ModelSwitch
"""

from __future__ import annotations

import sys
import pathlib

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Classe représentant un modèle de creux
class Model:

    """

        Classe Model
        ============

        La classe Model représente un modèle de creux générique

        :datas:

            self.name: str

        :Example:

        >>> a = Model(name="foo")
        >>> print(a)
        --> Model                  :                       foo
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, name: str) -> None:

        self.name = name

    #-----
    def getCreux(self, fraction: float = 0.) -> float:

        """ générique """

    #-----
    def __str__(self) -> str:

        strMsg = f'--> Model                  : {self.name:>25s}\n'
        return strMsg

#----- Classe représentant un modèle de creux "parabolique" dans le sens de la longueur
class ModelFlat(Model):

    """

        Classe ModelFlat
        ================

        La classe ModelFlat représente un creux nul quelque soit la position
            on retourne donc 0.

        :datas:

        :Example:

        >>> a = ModelFlat()
        >>> print(a)
        --> Model                  :                 ModelFlat
                        Paramètres :
                                    (aucun)
        <BLANKLINE>
        >>> a.getCreux(fraction=0.)
        0.0
        >>> a.getCreux(fraction=0.5)
        0.0
        >>> a.getCreux(fraction=1.)
        0.0

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self) -> None:

        super().__init__('ModelFlat')

    #-----
    def getCreux(self, fraction: float = 0.) -> float:

        assert(fraction >= 0. and fraction <= 1.)
        return 0.

    #-----
    def __str__(self) -> str:

        strMsg = super().__str__()
        strMsg += f'                Paramètres :\n'
        strMsg += f'                            (aucun)\n'
        return strMsg

#----- Classe représentant un modèle de creux "parabolique" dans le sens de la longueur
class ModelParabolique(Model):

    """

        Classe ModelParabolique
        =======================

        La classe ModelParabolique représente le creux "parabolique" dans le sens de la longueur
            cad que pour une section donnée (nombre variant de 0. (guindant) à 1. (chute) et
            une position de creux max donnée en pourcent 0.% (guindant) 100.% (chute),
            la valeur du creux est calculée par la formule :
                si on est avant le creux max :
                    k = 1 - ((x - rpdepthp)/rpdepthp)**2
                si on est après le creux max :
                    k = 1 - ((x - rpdepthp)/(1 - rpdepthp))**2
            On a donc à faire avec 2 paraboles :
                pour x = 0, k = 0
                pour x = rpdepth, k = 1
                pour x = 1, k = 0
            Ensuite on retourne k * creuxmax

        :datas:

            self.dictParams: dict
            self.rpdepth:    float
            self.rpdepthp:   float
            self.creuxmax:   float

        :Example:

        >>> a = ModelParabolique({"rpdepth": 40., "creuxmax": 50.})
        >>> print(a)
        --> Model                  :          ModelParabolique
                        Paramètres :
                                     rpdepth =    40.000% <=>     0.400
                                     creux   =    50.000
        <BLANKLINE>
        >>> a.getCreux(fraction=0.)
        0.0
        >>> a.getCreux(fraction=0.2)
        37.5
        >>> a.getCreux(fraction=0.4)
        50.0
        >>> a.getCreux(fraction=0.6)
        44.44444444444445
        >>> a.getCreux(fraction=1.)
        0.0
        >>> b = ModelParabolique({"creuxmax": 50.})
        < !!!! > Pas de clé "rpdepth" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(b)
        --> Model                  :          ModelParabolique
                        Paramètres :
                                     rpdepth =    40.000% <=>     0.400
                                     creux   =    50.000
        <BLANKLINE>
        >>> c = ModelParabolique({"rpdepth": 40.})
        < !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(c)
        --> Model                  :          ModelParabolique
                        Paramètres :
                                     rpdepth =    40.000% <=>     0.400
                                     creux   =     0.000
        <BLANKLINE>
        >>> d = ModelParabolique({})
        < !!!! > Pas de clé "rpdepth" ou clé incorrecte dans le Json valeur par défaut affectée
        < !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(d)
        --> Model                  :          ModelParabolique
                        Paramètres :
                                     rpdepth =    40.000% <=>     0.400
                                     creux   =     0.000
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictParams: dict) -> None:

        super().__init__('ModelParabolique')

        self.dictParams = dictParams
        # rpdepth : Float,  compris entre >= 10. et <= 90., par défaut 40.
        self.rpdepth = 40.
        if "rpdepth" in self.dictParams and \
           isinstance(self.dictParams["rpdepth"], float) and \
           self.dictParams["rpdepth"] >= 10. and \
           self.dictParams["rpdepth"] <= 90.:
            self.rpdepth = self.dictParams["rpdepth"]
        else:
            print(f'< !!!! > Pas de clé "rpdepth" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.rpdepthp = self.rpdepth/100.

        # creuxmax : Float, compris entre >= 1. et <= 500., par défaut 0.
        self.creuxmax = 0.
        if "creuxmax" in self.dictParams and \
           isinstance(self.dictParams["creuxmax"], float) and \
           self.dictParams["creuxmax"] >= 1. and \
           self.dictParams["creuxmax"] <= 500.:
            self.creuxmax = self.dictParams["creuxmax"]
        else:
            print(f'< !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée')

    #-----
    def getCreux(self, fraction: float = 0.) -> float:

        assert(fraction >= 0. and fraction <= 1.)
        if fraction <= self.rpdepthp:
            return self.creuxmax * (1. - ((fraction - self.rpdepthp)/self.rpdepthp)**2)
        else:
            return self.creuxmax * (1. - ((fraction - self.rpdepthp)/(1. - self.rpdepthp))**2)

    #-----
    def __str__(self) -> str:

        strMsg = super().__str__()
        strMsg += f'                Paramètres :\n'
        strMsg += f'                             rpdepth = {self.rpdepth:>9.3f}% <=> {self.rpdepthp:>9.3f}\n'
        strMsg += f'                             creux   = {self.creuxmax:>9.3f}\n'
        return strMsg

#----- Classe représentant un modèle de creux "tubulaire" dans le sens de la longueur
class ModelTube(Model):

    """

        Classe ModelTube
        ================

        La classe ModelTube représente le creux "tubulaire" dans le sens de la longueur
            cad que pour une section donnée (nombre variant de 0. (guindant) à 1. (chute),
            il y a 2 bornes (min et max). Avant le min on a une parabole, après le max on a une parabole,
            entre les 2, le creux est constant.
            la valeur du creux est calculée par la formule :
                si on est avant le creux min :
                    k = 1 - ((x - rpdepthminp)/rpdepthminp)**2
                si on est entre le creux min et le creux max :
                    k = 1
                si on est après le creux max :
                    k = 1 - ((x - rpdepthmaxp)/(1 - rpdepthmaxp))**2
            Ensuite on retourne k * creuxmax

        :datas:

            self.dictParams:  dict
            self.rpdepthmin:  float
            self.rpdepthminp: float
            self.rpdepthmax:  float
            self.rpdepthmaxp: float
            self.creuxmax:    float

        :Example:

        >>> a = ModelTube({"rpdepthmin": 15., "rpdepthmax": 85., "creuxmax": 50.})
        >>> print(a)
        --> Model                  :                 ModelTube
                        Paramètres :
                                     rpdepthmin =    15.000% <=>     0.150
                                     rpdepthmax =    85.000% <=>     0.850
                                     creux      =    50.000
        <BLANKLINE>
        >>> a.getCreux(fraction=0.)
        0.0
        >>> a.getCreux(fraction=0.1)
        44.44444444444445
        >>> a.getCreux(fraction=0.4)
        50.0
        >>> a.getCreux(fraction=0.6)
        50.0
        >>> a.getCreux(fraction=1.)
        0.0
        >>> b = ModelTube({"creuxmax": 40.})
        < !!!! > Pas de clé "rpdepthmin" ou clé incorrecte dans le Json valeur par défaut affectée
        < !!!! > Pas de clé "rpdepthmax" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(b)
        --> Model                  :                 ModelTube
                        Paramètres :
                                     rpdepthmin =    15.000% <=>     0.150
                                     rpdepthmax =    85.000% <=>     0.850
                                     creux      =    40.000
        <BLANKLINE>
        >>> c = ModelTube({"rpdepthmin": 40.})
        < !!!! > Pas de clé "rpdepthmax" ou clé incorrecte dans le Json valeur par défaut affectée
        < !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(c)
        --> Model                  :                 ModelTube
                        Paramètres :
                                     rpdepthmin =    40.000% <=>     0.400
                                     rpdepthmax =    85.000% <=>     0.850
                                     creux      =     0.000
        <BLANKLINE>
        >>> d = ModelTube({})
        < !!!! > Pas de clé "rpdepthmin" ou clé incorrecte dans le Json valeur par défaut affectée
        < !!!! > Pas de clé "rpdepthmax" ou clé incorrecte dans le Json valeur par défaut affectée
        < !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée
        >>> print(d)
        --> Model                  :                 ModelTube
                        Paramètres :
                                     rpdepthmin =    15.000% <=>     0.150
                                     rpdepthmax =    85.000% <=>     0.850
                                     creux      =     0.000
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictParams: dict) -> None:

        super().__init__('ModelTube')

        self.dictParams = dictParams
        # rpdepthmin : Float,  compris entre >= 5. et <= 45., par défaut 15.
        self.rpdepthmin = 15.
        if "rpdepthmin" in self.dictParams and \
           isinstance(self.dictParams["rpdepthmin"], float) and \
           self.dictParams["rpdepthmin"] >= 5. and \
           self.dictParams["rpdepthmin"] <= 45.:
            self.rpdepthmin = self.dictParams["rpdepthmin"]
        else:
            print(f'< !!!! > Pas de clé "rpdepthmin" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.rpdepthminp = self.rpdepthmin/100.

        # rpdepthmax : Float,  compris entre >= 55. et <= 95., par défaut 85.
        self.rpdepthmax = 85.
        if "rpdepthmax" in self.dictParams and \
           isinstance(self.dictParams["rpdepthmax"], float) and \
           self.dictParams["rpdepthmax"] >= 55. and \
           self.dictParams["rpdepthmax"] <= 95.:
            self.rpdepthmax = self.dictParams["rpdepthmax"]
        else:
            print(f'< !!!! > Pas de clé "rpdepthmax" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.rpdepthmaxp = self.rpdepthmax/100.

        # creuxmax : Float, compris entre >= 1. et <= 500., par défaut 0.
        self.creuxmax = 0.
        if "creuxmax" in self.dictParams and \
           isinstance(self.dictParams["creuxmax"], float) and \
           self.dictParams["creuxmax"] >= 1. and \
           self.dictParams["creuxmax"] <= 500.:
            self.creuxmax = self.dictParams["creuxmax"]
        else:
            print(f'< !!!! > Pas de clé "creuxmax" ou clé incorrecte dans le Json valeur par défaut affectée')

    #-----
    def getCreux(self, fraction: float = 0.) -> float:

        assert(fraction >= 0. and fraction <= 1.)
        if fraction <= self.rpdepthminp:

            return self.creuxmax * (1. - ((fraction - self.rpdepthminp)/self.rpdepthminp)**2)

        elif fraction <= self.rpdepthmaxp:

            return self.creuxmax

        else:

            return self.creuxmax * (1. - ((fraction - self.rpdepthmaxp)/(1. - self.rpdepthmaxp))**2)

    #-----
    def __str__(self) -> str:

        strMsg = super().__str__()
        strMsg += f'                Paramètres :\n'
        strMsg += f'                             rpdepthmin = {self.rpdepthmin:>9.3f}% <=> {self.rpdepthminp:>9.3f}\n'
        strMsg += f'                             rpdepthmax = {self.rpdepthmax:>9.3f}% <=> {self.rpdepthmaxp:>9.3f}\n'
        strMsg += f'                             creux      = {self.creuxmax:>9.3f}\n'
        return strMsg


#----- Classe permettant de créer un modèle
class ModelSwitch:

    """

        Classe ModelSwitch
        ==================

        La classe ModelSwitch permet de créer le bon modèle

        :datas:

            self.dictModel: dict
            self.nameModel: str
            self.Model:     Model

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictModel: dict) -> None:

        self.dictModel = dictModel
        if not "nameModel" in dictModel:
            print(f'Pas de clé "nameModel" dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)
        self.nameModel = dictModel["nameModel"]

        if self.nameModel == "ModelFlat":
            self.model = ModelFlat()
        elif self.nameModel == "ModelParabolique":
            self.model = ModelParabolique(dictModel["paramModel"])
        elif self.nameModel == "ModelTube":
            self.model = ModelTube(dictModel["paramModel"])
        else:
            print(f'Pas de modèle correspondant')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def getModel(self) -> Model:

        """ retourne la classe correcte """
        return self.model

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
