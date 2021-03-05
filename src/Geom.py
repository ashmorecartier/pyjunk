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
    Geom.py rassemble la définition des classes:
        Vect1D
            Vect1Ddict(Vect1D)
            Vect2D(Vect1D)
                Vect2Ddict(Vect2D)
                Vect3D(Vect2D)
                    Vect3Ddict(Vect3D)
        Point1D
            Point1Ddict(Point1D)
            Point2D(Point1D)
                Point2Ddict(Point2D)
                Point3D(Point2D)
                    Point3Ddict(Point3D)
"""

from __future__ import annotations

import sys
import pathlib
import math

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- Classe représentant un vecteur 1 dimension
class Vect1D:

    """

        Classe Vect1D
        =============

        La classe Vect1D représente un vecteur 1 dimension

        :datas:

            self.fX: float

        :Example:

        >>> a = Vect1D(fX=3.)
        >>> print(a)
        Vect1D  --> (X) = (    3.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fX: float=0.) -> None:

        self.fX = fX

    #-----
    def v1dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect1D(fX=3.)
            >>> a.v1dx()
            3.0

        """

        return self.fX

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Vect1D(fX=3.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0}

        """

        return {"x": self.fX}

    #-----
    def __eq__(self, v1d: Vect1D) -> bool:

        return self.v1dx() == v1d.v1dx()

    #-----
    def __str__(self) -> str:

        return f'Vect1D  --> (X) = ({self.fX:9.3f}) mm'

#----- Classe représentant un vecteur 1 dimension constructeur par dict
class Vect1Ddict(Vect1D):

    """

        Classe Vect1Ddict
        =================

        La classe Vect1Ddict représente un vecteur 1 dimension construit par dict

        :datas:

            self.dictVect1D: dict

        :Example:

        >>> a = Vect1Ddict({"x":3.})
        >>> print(a)
        Vect1D  --> (X) = (    3.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictVect1D: dict) -> None:

        self.dictVect1D = dictVect1D
        if "x" in self.dictVect1D and isinstance(self.dictVect1D["x"], float):
            Vect1D.__init__(self, fX=self.dictVect1D["x"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Vect1Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un vecteur 2 dimensions
class Vect2D(Vect1D):

    """

        Classe Vect2D
        =============

        La classe Vect2D représente un vecteur 2 dimensions
        hérite de Vect1D

        :datas:

            self.fY: float

        :Example:

        >>> a = Vect2D(fX=3., fY=4.)
        >>> print(a)
        Vect2D  --> (X,Y) = (    3.000,    4.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fX: float=0., fY: float=0.) -> None:

        Vect1D.__init__(self, fX)
        self.fY = fY

    #-----
    def v2dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect2D(fX=3., fY=4.)
            >>> a.v2dx()
            3.0

        """

        return Vect1D.v1dx(self)

    #-----
    def v2dy(self) -> float:

        """
            retourne le contenu de fY

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect2D(fX=3., fY=4.)
            >>> a.v2dy()
            4.0

        """

        return self.fY

    #-----
    def rot2d(self, ath: float=0.) -> Vect2D:

        """
            effectue une rotation d'un angle ath en radian

            :param: ath (angle en radian)
            :rtype: Vect2D

            :Example:

            >>> a = Vect2D(fX=1., fY=1.)
            >>> print(a.rot2d(ath=math.radians(+45.)))
            Vect2D  --> (X,Y) = (    0.000,    1.414) mm

        """

        return Vect2D(fX=math.cos(ath)*self.v2dx() - math.sin(ath)*self.v2dy(),
                      fY=math.sin(ath)*self.v2dx() + math.cos(ath)*self.v2dy())

    #-----
    def angle2d(self) -> float:

        """
            calcule l'angle 2D du Vect2D

            :param: aucun
            :rtype: float (radian)

            :Example:

            >>> a = Vect2D(fX=1., fY=1.)
            >>> print(math.degrees(a.angle2d()))
            45.0

            .. warning:: nécessite évidemment que fX != 0.

        """

        return math.atan2(self.v2dy(), self.v2dx())

    #-----
    def norm2d(self) -> float:

        """
            calcule la norme du Vect2D

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect2D(fX=1., fY=1.)
            >>> print(a.norm2d())
            1.4142135623730951

        """

        return math.sqrt(self.v2dx()*self.v2dx() + self.v2dy()*self.v2dy())

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX,fY sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Vect2D(fX=3., fY=4.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0, 'y': 4.0}

        """

        return {**Vect1D.getDict(self), **{"y": self.fY}}

    #-----
    def __eq__(self, v2d: Vect2D) -> bool:

        return (self.v2dx() == v2d.v2dx()) and (self.v2dy() == v2d.v2dy())

    #-----
    def __str__(self) -> str:

        return f'Vect2D  --> (X,Y) = ({self.v2dx():9.3f},{self.v2dy():9.3f}) mm'

#----- Classe représentant un vecteur 2 dimension constructeur par dict
class Vect2Ddict(Vect2D):

    """

        Classe Vect2Ddict
        =================

        La classe Vect2Ddict représente un vecteur 2 dimensions construit par dict

        :datas:

            self.dictVect2D: dict

        :Example:

        >>> a = Vect2Ddict({"x":3., "y":4.})
        >>> print(a)
        Vect2D  --> (X,Y) = (    3.000,    4.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictVect2D: dict) -> None:

        self.dictVect2D = dictVect2D
        if "x" in self.dictVect2D and isinstance(self.dictVect2D["x"], float) and\
           "y" in self.dictVect2D and isinstance(self.dictVect2D["y"], float):
            Vect2D.__init__(self, fX=self.dictVect2D["x"], fY=self.dictVect2D["y"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Vect2Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un vecteur 3 dimensions
class Vect3D(Vect2D):

    """

        Classe Vect3D
        =============

        La classe Vect3D représente un vecteur 3 dimensions
        hérite de Vect2D

        :datas:

            self.fZ: float

        :Example:

        >>> a = Vect3D(fX=3., fY=4., fZ=6.)
        >>> print(a)
        Vect3D  --> (X,Y,Z) = (    3.000,    4.000,    6.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fX: float=0., fY: float=0., fZ: float=0.) -> None:

        Vect2D.__init__(self, fX, fY)
        self.fZ = fZ

    #-----
    def v3dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=3., fY=4., fZ=6.)
            >>> a.v3dx()
            3.0

        """

        return Vect2D.v2dx(self)

    #-----
    def v3dy(self) -> float:

        """
            retourne le contenu de fY

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=3., fY=4., fZ=6.)
            >>> a.v3dy()
            4.0

        """

        return Vect2D.v2dy(self)

    #-----
    def v3dz(self) -> float:

        """
            retourne le contenu de fZ

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=3., fY=4., fZ=6.)
            >>> a.v3dz()
            6.0

        """

        return self.fZ

    #-----
    def rot3dx(self, ath: float=0.) -> Vect3D:

        """
            effectue une rotation autour de l'axe x d'un angle ath en radian

            :param: ath (angle en radian)
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=1., fZ=1.)
            >>> print(a.rot3dx(ath=math.radians(+45.)))
            Vect3D  --> (X,Y,Z) = (    1.000,    0.000,    1.414) mm

        """

        return Vect3D(fX=1.*self.v3dx() + 0.*self.v3dy() + 0.*self.v3dz(),
                      fY=0.*self.v3dx() + math.cos(ath)*self.v3dy() - math.sin(ath)*self.v3dz(),
                      fZ=0.*self.v3dx() + math.sin(ath)*self.v3dy() + math.cos(ath)*self.v3dz())

    #-----
    def rot3dy(self, ath: float=0.) -> Vect3D:

        """
            effectue une rotation autour de l'axe y d'un angle ath en radian

            :param: ath (angle en radian)
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=1., fZ=1.)
            >>> print(a.rot3dy(ath=math.radians(+45.)))
            Vect3D  --> (X,Y,Z) = (    1.414,    1.000,    0.000) mm

        """

        return Vect3D(fX=math.cos(ath)*self.v3dx() + 0.*self.v3dy() + math.sin(ath)*self.v3dz(),
                      fY=0.*self.v3dx() + 1.*self.v3dy() + 0.*self.v3dz(),
                      fZ=-math.sin(ath)*self.v3dx() + 0.*self.v3dy() + math.cos(ath)*self.v3dz())

    #-----
    def rot3dz(self, ath: float=0.) -> Vect3D:

        """
            effectue une rotation autour de l'axe z d'un angle ath en radian

            :param: ath (angle en radian)
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=1., fZ=1.)
            >>> print(a.rot3dz(ath=math.radians(+45.)))
            Vect3D  --> (X,Y,Z) = (    0.000,    1.414,    1.000) mm

        """

        return Vect3D(fX=math.cos(ath)*self.v3dx() - math.sin(ath)*self.v3dy() + 0.*self.v3dz(),
                      fY=math.sin(ath)*self.v3dx() + math.cos(ath)*self.v3dy() + 0.*self.v3dz(),
                      fZ=0.*self.v3dx() + 0.*self.v3dy() + 1.*self.v3dz())

    #-----
    def norm3d(self) -> float:

        """
            calcule la norme du Vect3D

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=1., fY=1., fZ=1.)
            >>> print(a.norm3d())
            1.7320508075688772

        """

        return math.sqrt(self.v3dx()*self.v3dx() + self.v3dy()*self.v3dy() + self.v3dz()*self.v3dz())

    #-----
    def prodvect3d(self, v3d: Vect3D) -> Vect3D:

        """
            effectue le produit vectoriel avec un autre Vect3d

            :param: Vect3D
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=0., fZ=0.)
            >>> b = Vect3D(fX=0., fY=1., fZ=0.)
            >>> print(a.prodvect3d(b))
            Vect3D  --> (X,Y,Z) = (    0.000,    0.000,    1.000) mm

        """

        return Vect3D(fX=self.v3dy()*v3d.v3dz() - self.v3dz()*v3d.v3dy(),
                      fY=self.v3dz()*v3d.v3dx() - self.v3dx()*v3d.v3dz(),
                      fZ=self.v3dx()*v3d.v3dy() - self.v3dy()*v3d.v3dx())

    #-----
    def scalmul3d(self, k: float=1.) -> Vect3D:

        """
            effectue un produit scalaire de facteur k

            :param: float
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=2., fZ=3.)
            >>> print(a.scalmul3d(k=2.))
            Vect3D  --> (X,Y,Z) = (    2.000,    4.000,    6.000) mm

        """

        return Vect3D(fX=self.v3dx()*k,
                      fY=self.v3dy()*k,
                      fZ=self.v3dz()*k)

    #-----
    def scaldiv3d(self, k: float=1.) -> Vect3D:

        """
            effectue un produit scalaire de facteur 1/k ; k != 0. évidemment

            :param: float
            :rtype: Vect3D

            :Example:

            >>> a = Vect3D(fX=1., fY=2., fZ=3.)
            >>> print(a.scaldiv3d(k=2.))
            Vect3D  --> (X,Y,Z) = (    0.500,    1.000,    1.500) mm

        """

        return self.scalmul3d(1./k)

    #-----
    def angle2dxy(self) -> float:

        """
            calcule l'angle 2D en radian dans le plan XY du Vect3D

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=1., fY=1., fZ=0.)
            >>> math.degrees(a.angle2dxy())
            45.0

        """

        return math.atan2(self.v3dy(), self.v3dx())

    #-----
    def angle2dxz(self) -> float:

        """
            calcule l'angle 2D en radian dans le plan XZ du Vect3D

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=1., fY=0., fZ=1.)
            >>> math.degrees(a.angle2dxz())
            45.0

        """

        return math.atan2(self.v3dz(), self.v3dx())

    #-----
    def angle2dyz(self) -> float:

        """
            calcule l'angle 2D en radian dans le plan YZ du Vect3D

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Vect3D(fX=0., fY=1., fZ=1.)
            >>> math.degrees(a.angle2dyz())
            45.0

        """

        return math.atan2(self.v3dz(), self.v3dy())

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX,fY,fZ sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Vect3D(fX=3., fY=4., fZ=5.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0, 'y': 4.0, 'z': 5.0}

        """

        return {**Vect2D.getDict(self), **{"z": self.fZ}}

    #-----
    def __eq__(self, v3d: Vect3D) -> bool:

        return (self.v3dx() == v3d.v3dx()) and (self.v3dy() == v3d.v3dy()) and (self.v3dz() == v3d.v3dz())

    #-----
    def __str__(self) -> str:

        return f'Vect3D  --> (X,Y,Z) = ({self.v3dx():9.3f},{self.v3dy():9.3f},{self.v3dz():9.3f}) mm'

#----- Classe représentant un vecteur 3 dimensions constructeur par dict
class Vect3Ddict(Vect3D):

    """

        Classe Vect3Ddict
        =================

        La classe Vect3Ddict représente un vecteur 3 dimensions construit par dict

        :datas:

            self.dictVect3D: dict

        :Example:

        >>> a = Vect3Ddict({"x":3., "y":4., "z":6.})
        >>> print(a)
        Vect3D  --> (X,Y,Z) = (    3.000,    4.000,    6.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictVect3D: dict) -> None:

        self.dictVect3D = dictVect3D
        if "x" in self.dictVect3D and isinstance(self.dictVect3D["x"], float) and\
           "y" in self.dictVect3D and isinstance(self.dictVect3D["y"], float) and\
           "z" in self.dictVect3D and isinstance(self.dictVect3D["z"], float):
            Vect3D.__init__(self, fX=self.dictVect3D["x"], fY=self.dictVect3D["y"], fZ=self.dictVect3D["z"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Vect3Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un point 1 dimension
class Point1D:

    """

        Classe Point1D
        ==============

        La classe Point1D représente un point 1 dimension

        :datas:

            self.fX: float

        :Example:

        >>> a = Point1D(fX=3.)
        >>> print(a)
        Point1D --> (X) = (    3.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fX: float=0.) -> None:

        self.fX = fX

    #-----
    def p1dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point1D(fX=3.)
            >>> a.p1dx()
            3.0

        """

        return self.fX

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Point1D(fX=3.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0}

        """

        return {"x": self.fX}

    #-----
    def __eq__(self, p1d: Point1D) -> bool:

        return self.p1dx() == p1d.p1dx()

    #-----
    def __str__(self) -> str:

        return f'Point1D --> (X) = ({self.p1dx():9.3f}) mm'

#----- Classe représentant un point 1 dimension constructeur par dict
class Point1Ddict(Point1D):

    """

        Classe Point1Ddict
        ==================

        La classe Point1Ddict représente un point 1 dimension construit par dict

        :datas:

            self.dictPoint1D: dict

        :Example:

        >>> a = Point1Ddict({"x":3.})
        >>> print(a)
        Point1D --> (X) = (    3.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictPoint1D: dict) -> None:

        self.dictPoint1D = dictPoint1D
        if "x" in self.dictPoint1D and isinstance(self.dictPoint1D["x"], float):
            Point1D.__init__(self, fX=self.dictPoint1D["x"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Point1Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un point 2 dimensions
class Point2D(Point1D):

    """

        Classe Point2D
        ==============

        La classe Point2D représente un point 2 dimensions
        hérite de Point1D

        :datas:

            self.fY: float

        :Example:

        >>> a = Point2D(fX=3., fY=4.)
        >>> print(a)
        Point2D --> (X,Y) = (    3.000,    4.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    __nbround = 3

    #-----
    def __init__(self, fX: float=0., fY: float=0.) -> None:

        Point1D.__init__(self, fX)
        self.fY = fY

    #-----
    def p2dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point2D(fX=3., fY=4.)
            >>> a.p2dx()
            3.0

        """

        return Point1D.p1dx(self)

    #-----
    def p2dy(self) -> float:

        """
            retourne le contenu de fY

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point2D(fX=3., fY=4.)
            >>> a.p2dy()
            4.0

        """

        return self.fY

    #-----
    def trans2d(self, v2d: Vect2D) -> Point2D:

        """
            effectue la translation du Point2D selon un vecteur Vect2D

            :param: Vect2D v2d
            :rtype: Point2D

            :Example:

            >>> a = Point2D(fX=1., fY=2.)
            >>> v = Vect2D(fX=3., fY=4.)
            >>> print(a.trans2d(v2d=v))
            Point2D --> (X,Y) = (    4.000,    6.000) mm

        """

        return Point2D(fX=self.p2dx() + v2d.v2dx(),
                       fY=self.p2dy() + v2d.v2dy())

    #-----
    def dist2d(self, p2d: Point2D) -> float:

        """
            calcule la distance avec un autre Point2D

            :param: Point2D p2d
            :rtype: float

            :Example:

            >>> a = Point2D(fX=1., fY=2.)
            >>> b = Point2D(fX=3., fY=4.)
            >>> a.dist2d(p2d=b)
            2.8284271247461903

        """

        return (p2d - self).norm2d()

    #-----
    def mid2d(self, p2d: Point2D) -> Point2D:

        """
            retourne le Point2D millieu entre l'occurence et un autre Point2D

            :param: Point2D p2d
            :rtype: Point2D

            :Example:

            >>> a = Point2D(fX=1., fY=2.)
            >>> b = Point2D(fX=3., fY=4.)
            >>> print(a.mid2d(p2d=b))
            Point2D --> (X,Y) = (    2.000,    3.000) mm

        """

        return Point2D(fX=(self.p2dx() + p2d.p2dx())/2.,
                       fY=(self.p2dy() + p2d.p2dy())/2.)

    #-----
    def lin2d(self, k: float, p2d: Point2D) -> Point2D:

        """
            retourne le Point2D interpolation linéaire de facteur k entre l'occurence
            et un autre Point2D ( self*(1-k) + p2d*k )
            utiliser avec précaution
            si k=0. return self
            si k=1. return p2d

            :param1: float k
            :param2: Point2D p2d
            :rtype: Point2D

            :Example:

            >>> a = Point2D(fX=1., fY=2.)
            >>> b = Point2D(fX=3., fY=4.)
            >>> print(a.lin2d(k=1./3., p2d=b))
            Point2D --> (X,Y) = (    1.667,    2.667) mm

        """

        return Point2D(fX=self.p2dx()*(1. - k) + p2d.p2dx()*k,
                       fY=self.p2dy()*(1. - k) + p2d.p2dy()*k)

    #-----
    def round2d(self) -> tuple:

        """
            arrondi les coordonnées de l'instance
            utilise la variable globale __round
            utile pour la présentation en dxf

            :param: aucun
            :rtype: tuple

            :Example:

            >>> a = Point2D(fX=1./3., fY=2./3.)
            >>> print(a.round2d())
            (0.333, 0.667)

        """

        return round(self.p2dx(), Point2D.__nbround), round(self.p2dy(), Point2D.__nbround)

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX,fY sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Point2D(fX=3., fY=4.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0, 'y': 4.0}

        """

        return {**Point1D.getDict(self), **{"y": self.fY}}

    #-----
    def __eq__(self, p2d: Point2D) -> bool:

        return (self.p2dx() == p2d.p2dx()) and (self.p2dy() == p2d.p2dy())

    #-----
    def __sub__(self, p2d: Point2D) -> Vect2D:

        """
            retourne le Vect2D représentatif de la différence de 2 Point2D
            on effectue self - p2d

            :param: Point2D p2d
            :rtype: Vect2D

            :Example:

            >>> a = Point2D(fX=1., fY=1.)
            >>> b = Point2D(fX=2., fY=2.)
            >>> print(a - b)
            Vect2D  --> (X,Y) = (   -1.000,   -1.000) mm

        """

        return Vect2D(fX=self.p2dx() - p2d.p2dx(),
                      fY=self.p2dy() - p2d.p2dy())

    #-----
    def __str__(self) -> str:

        return f'Point2D --> (X,Y) = ({self.p2dx():9.3f},{self.p2dy():9.3f}) mm'

#----- Classe représentant un point 2 dimensions constructeur par dict
class Point2Ddict(Point2D):

    """

        Classe Point2Ddict
        ==================

        La classe Point2Ddict représente un point 2 dimensions construit par dict

        :datas:

            self.dictPoint2D: dict

        :Example:

        >>> a = Point2Ddict({"x":3., "y":4.})
        >>> print(a)
        Point2D --> (X,Y) = (    3.000,    4.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictPoint2D: dict) -> None:

        self.dictPoint2D = dictPoint2D
        if "x" in self.dictPoint2D and isinstance(self.dictPoint2D["x"], float) and\
           "y" in self.dictPoint2D and isinstance(self.dictPoint2D["y"], float):
            Point2D.__init__(self, fX=self.dictPoint2D["x"], fY=self.dictPoint2D["y"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Point2Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un point 3 dimensions
class Point3D(Point2D):

    """

        Classe Point3D
        ==============

        La classe Point3D représente un point 3 dimensions
        hérite de Point2D

        :datas:

            self.fZ: float

        :Example:

        >>> a = Point3D(fX=3., fY=4., fZ=6.)
        >>> print(a)
        Point3D --> (X,Y,Z) = (    3.000,    4.000,    6.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fX: float=0., fY: float=0., fZ: float=0.) -> None:

        Point2D.__init__(self, fX, fY)
        self.fZ = fZ

    #-----
    def p3dx(self) -> float:

        """
            retourne le contenu de fX

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point3D(fX=3., fY=4., fZ=6.)
            >>> a.p3dx()
            3.0

        """

        return self.p2dx()

    #-----
    def p3dy(self) -> float:

        """
            retourne le contenu de fY

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point3D(fX=3., fY=4., fZ=6.)
            >>> a.p3dy()
            4.0

        """

        return self.p2dy()

    #-----
    def p3dz(self) -> float:

        """
            retourne le contenu de fZ

            :param: aucun
            :rtype: float

            :Example:

            >>> a = Point3D(fX=3., fY=4., fZ=6.)
            >>> a.p3dz()
            6.0

        """

        return self.fZ

    #-----
    def trans3d(self, v3d: Vect3D) -> Point3D:

        """
            effectue la translation du Point3D selon un vecteur Vect3D

            :param: Vect3D v3d
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> v = Vect3D(fX=3., fY=4., fZ=5.)
            >>> print(a.trans3d(v3d=v))
            Point3D --> (X,Y,Z) = (    4.000,    6.000,    8.000) mm

        """

        return Point3D(fX=self.p3dx() + v3d.v3dx(),
                       fY=self.p3dy() + v3d.v3dy(),
                       fZ=self.p3dz() + v3d.v3dz())

    #-----
    def dist3d(self, p3d: Point3D) -> float:

        """
            calcule la distance avec un autre Point3D

            :param: Point3D p3d
            :rtype: float

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> b = Point3D(fX=3., fY=4., fZ=5.)
            >>> a.dist3d(p3d=b)
            3.4641016151377544

        """

        return (p3d - self).norm3d()

    #-----
    def mid3d(self, p3d: Point3D) -> Point3D:

        """
            retourne le Point3D millieu entre l'occurence et un autre Point3D

            :param: Point3D p3d
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> b = Point3D(fX=3., fY=4., fZ=5.)
            >>> print(a.mid3d(p3d=b))
            Point3D --> (X,Y,Z) = (    2.000,    3.000,    4.000) mm

        """

        return Point3D(fX=(self.p3dx() + p3d.p3dx())/2.,
                       fY=(self.p3dy() + p3d.p3dy())/2.,
                       fZ=(self.p3dz() + p3d.p3dz())/2.)

    #-----
    def lin3d(self, k: float, p3d: Point3D) -> Point3D:

        """
            retourne le Point3D interpolation linéaire de facteur k entre l'occurence
            et un autre Point3D ( self*(1-k) + p3d*k )
            utiliser avec précaution
            si k=0. return self
            si k=1. return p3d

            :param1: float k
            :param2: Point3D p3d
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> b = Point3D(fX=3., fY=4., fZ=5.)
            >>> print(a.lin3d(k=1./3., p3d=b))
            Point3D --> (X,Y,Z) = (    1.667,    2.667,    3.667) mm

        """

        return Point3D(fX=self.p3dx()*(1. - k) + p3d.p3dx()*k,
                       fY=self.p3dy()*(1. - k) + p3d.p3dy()*k,
                       fZ=self.p3dz()*(1. - k) + p3d.p3dz()*k)

    #-----
    def p3dto2dxy(self) -> Point2D:

        """
            retourne le Point2D projection du Point3D sur le plan XY

            :param: aucun
            :rtype: Point2D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> print(a.p3dto2dxy())
            Point2D --> (X,Y) = (    1.000,    2.000) mm

        """

        return Point2D(fX=self.p3dx(),
                       fY=self.p3dy())

    #-----
    def p3dto2dzy(self) -> Point2D:

        """
            retourne le Point2D projection du Point3D sur le plan ZY
            le résultat est dans le plan XY

            :param: aucun
            :rtype: Point2D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> print(a.p3dto2dzy())
            Point2D --> (X,Y) = (    3.000,    2.000) mm

        """

        return Point2D(fX=self.p3dz(),
                       fY=self.p3dy())

    #-----
    def scalmul3d(self, k: float=1.) -> Point3D:

        """
            effectue un produit scalaire de facteur k

            :param: float
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> print(a.scalmul3d(k=2.))
            Point3D --> (X,Y,Z) = (    2.000,    4.000,    6.000) mm

        """

        return Point3D(fX=self.p3dx()*k,
                       fY=self.p3dy()*k,
                       fZ=self.p3dz()*k)

    #-----
    def scaldiv3d(self, k: float=1.) -> Point3D:

        """
            effectue un produit scalaire de facteur 1/k ; k != 0. évidemment

            :param: float
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=2., fZ=3.)
            >>> print(a.scaldiv3d(k=2.))
            Point3D --> (X,Y,Z) = (    0.500,    1.000,    1.500) mm

        """

        return self.scalmul3d(1./k)

    #-----
    def getDict(self) -> dict:

        """
            retourne le contenu de fX,fY,fZ sous forme de dictionnaire

            :param: aucun
            :rtype: dict

            :Example:

            >>> a = Point3D(fX=3., fY=4., fZ=5.)
            >>> print(f'{a.getDict()}')
            {'x': 3.0, 'y': 4.0, 'z': 5.0}

        """

        return {**Point2D.getDict(self), **{"z": self.fZ}}

    #-----
    def __eq__(self, p3d: Point3D) -> bool:

        return (self.p3dx() == p3d.p3dx()) and (self.p3dy() == p3d.p3dy()) and (self.p3dz() == p3d.p3dz())

    #-----
    def __add__(self, p3d: Point3D) -> Point3D:

        """
            retourne le Point3D représentatif de la somme de 2 Point3D

            :param: Point3D p3d
            :rtype: Point3D

            :Example:

            >>> a = Point3D(fX=1., fY=1., fZ=1.)
            >>> b = Point3D(fX=2., fY=2., fZ=2.)
            >>> print(a + b)
            Point3D --> (X,Y,Z) = (    3.000,    3.000,    3.000) mm

        """

        return Point3D(fX=self.p3dx() + p3d.p3dx(),
                       fY=self.p3dy() + p3d.p3dy(),
                       fZ=self.p3dz() + p3d.p3dz())

    #-----
    def __sub__(self, p3d: Point3D) -> Vect3D:

        """
            retourne le Vectd3D représentatif de la différence de 2 Point3D
            on effectue self - p3d

            :param: Point3D p3d
            :rtype: Vect3D

            :Example:

            >>> a = Point3D(fX=1., fY=1., fZ=1.)
            >>> b = Point3D(fX=2., fY=2., fZ=2.)
            >>> print(a - b)
            Vect3D  --> (X,Y,Z) = (   -1.000,   -1.000,   -1.000) mm

        """

        return Vect3D(fX=self.p3dx() - p3d.p3dx(),
                      fY=self.p3dy() - p3d.p3dy(),
                      fZ=self.p3dz() - p3d.p3dz())

    #-----
    def __str__(self) -> str:

        return f'Point3D --> (X,Y,Z) = ({self.p3dx():9.3f},{self.p3dy():9.3f},{self.p3dz():9.3f}) mm'

#----- Classe représentant un point 3 dimensions constructeur par dict
class Point3Ddict(Point3D):

    """

        Classe Point3Ddict
        ==================

        La classe Point3Ddict représente un point 3 dimensions construit par dict

        :datas:

            self.dictPoint3D: float

        :Example:

        >>> a = Point3Ddict({"x":3., "y":4., "z":6.})
        >>> print(a)
        Point3D --> (X,Y,Z) = (    3.000,    4.000,    6.000) mm

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictPoint3D: dict) -> None:

        self.dictPoint3D = dictPoint3D
        if "x" in self.dictPoint3D and isinstance(self.dictPoint3D["x"], float) and\
           "y" in self.dictPoint3D and isinstance(self.dictPoint3D["y"], float) and\
           "z" in self.dictPoint3D and isinstance(self.dictPoint3D["z"], float):
            Point3D.__init__(self, fX=self.dictPoint3D["x"], fY=self.dictPoint3D["y"], fZ=self.dictPoint3D["z"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour Point3Ddict')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

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
