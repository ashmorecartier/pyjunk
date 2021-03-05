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
    Direction.py rassemble la définition des classes:
        Direction2D
        Direction3D
        Endroit2D
        Endroit3D
            Extremite3D(Endroit3D)
"""

from __future__ import annotations

import sys
import pathlib
import math

import Geom as ge

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Classe représentant une direction 2 dimensions
class Direction2D:

    """

        Classe Direction2D
        ==================

        La classe Direction2D contient les données d'un vecteur2D construit par un dictionnaire

        :datas:

            self.dictDirection2D: dict
            self.v2ddict:         Vect2Ddict

        :Example:

        >>> a = Direction2D({"vect2D": {"x": 10., "y": 10.}})
        >>> print(a)
        Vect2D  --> (X,Y) = (   10.000,   10.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictDirection2D: dict) -> None:

        self.dictDirection2D = dictDirection2D

        if "vect2D" in self.dictDirection2D and isinstance(self.dictDirection2D["vect2D"], dict):
            self.v2ddict = ge.Vect2Ddict(dictVect2D=self.dictDirection2D["vect2D"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDirection2D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def norm2d(self) -> float:

        """
            retourne la norme du vecteur Direction2D

            :param:
            :rtype: float

            :Example:

            >>> a = Direction2D({"vect2D": {"x": 10., "y": 10.}})
            >>> print(a.norm2d(), math.sqrt(10**2+10**2))
            14.142135623730951 14.142135623730951

        """

        return self.v2ddict.norm2d()

    #-----
    def angle2D(self) -> float:

        """
            retourne l'angle en radians d'une direction

            :param:
            :rtype: float

            :Example:

            >>> a = Direction2D({"vect2D": {"x": 10., "y": 10.}})
            >>> print(a.angle2D(), math.atan(10./10.))
            0.7853981633974483 0.7853981633974483

        """

        return self.v2ddict.angle2d()

    #-----
    def rot2d(self, fAth: float) -> dict:

        """
            tourne le Dicrection2D de fAth (radians)

            :param: Direction2D
            :rtype: dict

            :Example:

            >>> a = Direction2D({"vect2D": {"x": 10., "y": 10.}})
            >>> print(a.rot2d(fAth=math.radians(90.)))
            {'vect2D': {'x': -10.0, 'y': 10.0}}
            >>> print(a.rot2d(fAth=math.radians(-90.)))
            {'vect2D': {'x': 10.0, 'y': -10.0}}

        """

        return {'vect2D': self.v2ddict.rot2d(ath=fAth).getDict()}

    #-----
    def __str__(self) -> None:

        return f'{self.v2ddict}'

#----- Classe représentant une direction 3 dimensions
class Direction3D:

    """

        Classe Direction3D
        ================

        La classe Direction3D contient les données d'un vecteur3D construit par un dictionnaire

        :datas:

            self.dictDirection3D: dict
            self.v3ddict:         Vect3Ddict

        :Example:

        >>> a = Direction3D({"vect3D": {"x": 10., "y": 10., "z": 10.}})
        >>> print(a)
        Vect3D  --> (X,Y,Z) = (   10.000,   10.000,   10.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictDirection3D: dict) -> None:

        self.dictDirection3D = dictDirection3D

        if "vect3D" in self.dictDirection3D and isinstance(self.dictDirection3D["vect3D"], dict):
            self.v3ddict = ge.Vect3Ddict(dictVect3D=self.dictDirection3D["vect3D"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDirection3D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def norm3d(self) -> float:

        """
            retourne la norme du vecteur Direction3D

            :param:
            :rtype: float

            :Example:

            >>> a = Direction3D({"vect3D": {"x": 10., "y": 10., "z": 10.}})
            >>> print(a.norm3d(), math.sqrt(10**2+10**2+10**2))
            17.320508075688775 17.320508075688775

        """

        return self.v3ddict.norm3d()

    #-----
    def scaldiv3d(self, k: float=1.) -> dict:

        """
            applique un facteur par division au vecteur Direction3D

            :param: float
            :rtype: dict

            :Example:

            >>> a = Direction3D({"vect3D": {"x": 10., "y": 10., "z": 10.}})
            >>> print(a.scaldiv3d(k=2.))
            {'vect3D': {'x': 5.0, 'y': 5.0, 'z': 5.0}}

        """

        return {"vect3D": self.v3ddict.scaldiv3d(k=k).getDict()}

    #-----
    def prodvect3d(self, direction: Direction3D) -> dict:

        """
            effectue le produit vectoriel avec une autre Direction3D

            :param: Direction3D
            :rtype: dict

            :Example:

            >>> a = Direction3D({"vect3D": {"x": 1., "y": 0., "z": 0.}})
            >>> b = Direction3D({"vect3D": {"x": 0., "y": 1., "z": 0.}})
            >>> print(a.prodvect3d(b))
            {'vect3D': {'x': 0.0, 'y': 0.0, 'z': 1.0}}

        """

        return {"vect3D": self.v3ddict.prodvect3d(direction.v3ddict).getDict()}

    #-----
    def __str__(self) -> None:

        return f'{self.v3ddict}'

#----- Classe représentant un lieu 2 dimensions
class Endroit2D:

    """

        Classe Endroit2D
        ================

        La classe Endroit2D contient les données d'un point2D construit par un dictionnaire

        :datas:

            self.dictEndroit2D: dict
            self.p2ddict:       Point2Ddict

        :Example:

        >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
        >>> print(a)
        Point2D --> (X,Y) = (   10.000,   10.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictEndroit2D: dict) -> None:

        self.dictEndroit2D = dictEndroit2D

        if "point2D" in self.dictEndroit2D and isinstance(self.dictEndroit2D["point2D"], dict):
            self.p2ddict = ge.Point2Ddict(dictPoint2D=self.dictEndroit2D["point2D"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictEndroit2D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def dist2d(self, endroit2D: Endroit2D) -> float:

        """
            retourne la distance entre 2 endroits

            :param: endroit2D
            :rtype: float

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> b = Endroit2D({"point2D": {"x": 20., "y": 20.}})
            >>> print(a.dist2d(b), math.sqrt(10**2+10**2))
            14.142135623730951 14.142135623730951

        """

        return self.p2ddict.dist2d(endroit2D.p2ddict)

    #-----
    def mid2d(self, endroit2D: Endroit2D) -> dict:

        """
            retourne le millieu entre 2 endroits sous forme de dict

            :param: Endroit2D
            :rtype: dict

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> b = Endroit2D({"point2D": {"x": 20., "y": 30.}})
            >>> print(a.mid2d(b))
            {'point2D': {'x': 15.0, 'y': 20.0}}

        """

        return {"point2D": self.p2ddict.mid2d(endroit2D.p2ddict).getDict()}

    #-----
    def lin2d(self, k: float, endroit2D: Endroit2D) -> dict:

        """
            retourne la combinaison linéaire entre 2 endroits sous forme de dict

            :param: float, Endroit2D
            :rtype: dict

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> b = Endroit2D({"point2D": {"x": 20., "y": 30.}})
            >>> print(a.lin2d(k=0.5, endroit2D=b))
            {'point2D': {'x': 15.0, 'y': 20.0}}

        """

        return {'point2D': self.p2ddict.lin2d(k, endroit2D.p2ddict).getDict()}

    #-----
    def rot2d(self, fAth: float) -> dict:

        """
            tourne l'Endroit2D de fAth (radians) autour de l'origine

            :param: Endroit2D
            :rtype: dict

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> print(a.rot2d(fAth=math.radians(90.)))
            {'point2D': {'x': -10.0, 'y': 10.0}}
            >>> print(a.rot2d(fAth=math.radians(-90.)))
            {'point2D': {'x': 10.0, 'y': -10.0}}

        """

        return {'point2D': (self.p2ddict - ge.Point2D(fX=0., fY=0.)).rot2d(ath=fAth).getDict()}

    #-----
    def __add__(self, direction2D: Direction2D) -> ge.Point2Ddict:

        """
            retourne le point2D translaté du vecteur2D sous forme de dict

            :param: Direction2D
            :rtype: dict

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> b = Direction2D({"vect2D": {"x": 20., "y": 20.}})
            >>> print(a + b)
            {'point2D': {'x': 30.0, 'y': 30.0}}

        """

        return {'point2D': self.p2ddict.trans2d(direction2D.v2ddict).getDict()}

    #-----
    def __sub__(self, endroit2D: Endroit2D) -> ge.Vect2Ddict:

        """
            retourne le vecteur entre 2 endroits sous forme de dict

            :param: endroit2D
            :rtype: dict

            :Example:

            >>> a = Endroit2D({"point2D": {"x": 10., "y": 10.}})
            >>> b = Endroit2D({"point2D": {"x": 20., "y": 20.}})
            >>> print(a - b)
            {'vect2D': {'x': -10.0, 'y': -10.0}}
            >>> print(b - a)
            {'vect2D': {'x': 10.0, 'y': 10.0}}

        """

        return {'vect2D': (self.p2ddict - endroit2D.p2ddict).getDict()}

    #-----
    def __str__(self) -> None:

        return f'{self.p2ddict}'

#----- Classe représentant un lieu 3 dimensions
class Endroit3D:

    """

        Classe Endroit3D
        ==============

        La classe Endroit3D contient les données d'un point3D construit par un dictionnaire

        :datas:

            self.dictEndroit3D: dict
            self.p3ddict:       Point3Ddict

        :Example:

        >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
        >>> print(a)
        Point3D --> (X,Y,Z) = (   10.000,   10.000,   10.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictEndroit3D: dict) -> None:

        self.dictEndroit3D = dictEndroit3D

        if "point3D" in self.dictEndroit3D and isinstance(self.dictEndroit3D["point3D"], dict):
            self.p3ddict = ge.Point3Ddict(dictPoint3D=self.dictEndroit3D["point3D"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictEndroit3D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def getHt(self) -> float:

        """
            retourne la hauteur de l'Endroit3D cad z

            :param:
            :rtype: float

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 0., "y": 0., "z": 10.}})
            >>> print(a.getHt())
            10.0

        """

        return self.p3ddict.p3dz()

    #-----
    def dist3d(self, endroit3D: Endroit3D) -> float:

        """
            retourne la distance entre 2 endroits

            :param: endroit3D
            :rtype: float

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Endroit3D({"point3D": {"x": 20., "y": 20., "z": 20.}})
            >>> print(a.dist3d(b), math.sqrt(10**2+10**2+10**2))
            17.320508075688775 17.320508075688775

        """

        return self.p3ddict.dist3d(endroit3D.p3ddict)

    #-----
    def mid3d(self, endroit3D: Endroit3D) -> dict:

        """
            retourne le millieu entre 2 endroits sous forme de dict

            :param: Endroit3D
            :rtype: dict

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Endroit3D({"point3D": {"x": 20., "y": 30., "z": 40.}})
            >>> print(a.mid3d(b))
            {'point3D': {'x': 15.0, 'y': 20.0, 'z': 25.0}}

        """

        return {"point3D": self.p3ddict.mid3d(endroit3D.p3ddict).getDict()}

    #-----
    def lin3d(self, k: float, endroit3D: Endroit3D) -> dict:

        """
            retourne la combinaison linéaire entre 2 endroits sous forme de dict

            :param: float, Endroit3D
            :rtype: dict

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Endroit3D({"point3D": {"x": 20., "y": 30., "z": 40.}})
            >>> print(a.lin3d(k=0.5, endroit3D=b))
            {'point3D': {'x': 15.0, 'y': 20.0, 'z': 25.0}}

        """

        return {'point3D': self.p3ddict.lin3d(k, endroit3D.p3ddict).getDict()}

    #-----
    def __sub__(self, endroit3D: Endroit3D) -> ge.Vect3Ddict:

        """
            retourne le vecteur entre 2 endroits sous forme de dict

            :param: endroit3D
            :rtype: dict

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Endroit3D({"point3D": {"x": 20., "y": 20., "z": 20.}})
            >>> print(a - b)
            {'vect3D': {'x': -10.0, 'y': -10.0, 'z': -10.0}}
            >>> print(b - a)
            {'vect3D': {'x': 10.0, 'y': 10.0, 'z': 10.0}}

        """

        return {'vect3D': (self.p3ddict - endroit3D.p3ddict).getDict()}

    #-----
    def applyTwists(self, fAtwistr: float) -> dict:

        """
            tourne l'Endroit3D autour de l'axe z de fAtwistr (radians)

            :param: Endroit3D
            :rtype: dict

            :Example:

            >>> a = Endroit3D({"point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> print(a.applyTwists(fAtwistr=math.radians(90.)))
            {'point3D': {'x': -10.0, 'y': 10.0, 'z': 10.0}}
            >>> print(a.applyTwists(fAtwistr=math.radians(-90.)))
            {'point3D': {'x': 10.0, 'y': -10.0, 'z': 10.0}}

        """

        return {'point3D': (self.p3ddict - ge.Point3D(fX=0., fY=0., fZ=0.)).rot3dz(ath=fAtwistr).getDict()}

    #-----
    def __str__(self) -> None:

        return f'{self.p3ddict}'

#----- Classe représentant une extrémité de baton
class Extremite3D(Endroit3D):

    """

        Classe Extremite3D
        ==================

        La classe Extremite3D contient les données d'une extrémité d'un baton

        :datas:

            self.dictExtremite3D: dict
            self.type:            str

        :Example:

        >>> a = Extremite3D({"type": "Guindant", "point3D": {"x": 10., "y": 10., "z": 10.}})
        >>> print(a)
        Guindant   : Point3D --> (X,Y,Z) = (   10.000,   10.000,   10.000) mm
        >>> b = Extremite3D({"type": "Chute   ", "point3D": {"x": 20., "y": 20., "z": 20.}})
        >>> print(b)
        Chute      : Point3D --> (X,Y,Z) = (   20.000,   20.000,   20.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictExtremite3D: dict) -> None:

        self.dictExtremite3D = dictExtremite3D

        if "type" in self.dictExtremite3D and isinstance(self.dictExtremite3D["type"], str):
            self.type = dictExtremite3D["type"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictExtremite3D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "point3D" in self.dictExtremite3D:
            Endroit3D.__init__(self, {"point3D": self.dictExtremite3D["point3D"]})
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictExtremite3D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def mid3d(self, extremite3D: Extremite3D) -> dict:

        """
            retourne le dictionnaire milieu de 2 extremites

            :param: Extremite3D
            :rtype: dict

            :Example:

            >>> a = Extremite3D({"type": "Guindant", "point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Extremite3D({"type": "Guindant", "point3D": {"x": 20., "y": 20., "z": 20.}})
            >>> print(a.mid3d(b))
            {'type': 'Guindant', 'point3D': {'x': 15.0, 'y': 15.0, 'z': 15.0}}

        """

        assert self.type == extremite3D.type
        return {"type": self.type, **Endroit3D.mid3d(self, extremite3D)}

    #-----
    def lin3d(self, k: float, extremite3D: Extremite3D) -> dict:

        """
            retourne le dictionnaire interpolation lineaire de facteur k entre 2 extremites

            :param: float, Extremite3D
            :rtype: dict

            :Example:

            >>> a = Extremite3D({"type": "Guindant", "point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> b = Extremite3D({"type": "Chute", "point3D": {"x": 20., "y": 20., "z": 20.}})
            >>> print(a.lin3d(0.5, b))
            {'type': 'Intermediaire', 'point3D': {'x': 15.0, 'y': 15.0, 'z': 15.0}}

        """

        assert self.type != extremite3D.type
        return {'type': 'Intermediaire', **Endroit3D.lin3d(self, k, extremite3D)}

    #-----
    def getType(self):

        """ retourne le type """

        return self.type

    #-----
    def applyTwists(self, fAtwistr: float) -> dict:

        """
            tourne l'Extrémité autour de l'axe z de fAtwistr (radians)

            :param: Extrémité
            :rtype: dict

            :Example:

            >>> a = Extremite3D({"type": "Guindant", "point3D": {"x": 10., "y": 10., "z": 10.}})
            >>> print(a.applyTwists(fAtwistr=math.radians(90.)))
            {'type': 'Guindant', 'point3D': {'x': -10.0, 'y': 10.0, 'z': 10.0}}
            >>> print(a.applyTwists(fAtwistr=math.radians(-90.)))
            {'type': 'Guindant', 'point3D': {'x': 10.0, 'y': -10.0, 'z': 10.0}}

        """

        return {"type": self.type, **Endroit3D.applyTwists(self, fAtwistr=fAtwistr)}

    #-----
    def __str__(self) -> str:

        return f'{self.type:<10} : {Endroit3D.__str__(self)}'

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
