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
    Developp.py rassemble la définition des classes:
        Developp2D
            Developp(Developp2D)
"""

from __future__ import annotations

import sys
import pathlib
import math
from datetime import datetime

import Direction as di

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

#----- tableau (dictionnaire) pour les couleurs des tracés
couleur = {
    "blanc":   0,
    "rouge":   1,
    "jaune":   2,
    "vert":    3,
    "magenta": 4,
    "bleu":    5,
    "violet":  6,
    "gris":    8
}

#----- Classe représentant le modèle pour le calcul du développé
class Developp2D:

    """

        Classe Developp2D
        =================

        La classe Developp2D calcule et stocke la représentation du développé, 2D par définition

        :datas:

            self.dictDevelopp2D:          dict
            self.numPanneau:              int
            self.lendroit2DMil:           list
            self.lendroit2DHaut:          list
            self.lendroit2DBas:           list
            self.lendroit2DHautChainette: list
            self.lendroit2DBasChainette:  list
            self.lendroit2DHautCouture:   list
            self.endroit2DMil:            Endroit2D
            self.endroit2DHaut:           Endroit2D
            self.endroit2DBas:            Endroit2D

        :Example:

        >>> a = Developp2D({"numPanneau": 0})
        >>> print(a)
        --> Developp2D                :
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictDevelopp2D: dict) -> None:

        self.dictDevelopp2D = dictDevelopp2D

        if "numPanneau" in self.dictDevelopp2D and isinstance(self.dictDevelopp2D["numPanneau"], int):
            self.numPanneau = self.dictDevelopp2D["numPanneau"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp2D')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # les listes de points 2D qui seront placés dans le dxf
        self.lendroit2DMil = []
        self.lendroit2DHaut = []
        self.lendroit2DBas = []
        self.lendroit2DHautChainette = []
        self.lendroit2DBasChainette = []
        self.lendroit2DHautCouture = []

        # les points 2D précédents
        self.endroit2DMil = None
        self.endroit2DHaut = None
        self.endroit2DBas = None

    #-----
    @staticmethod
    def calc(dictCalc: dict) -> tuple:

        """
            soit 2 cercles (x-a)²+(y-b)²=r0² et (x-c)²+(y-d)²=r1², on cherche les points d'intersection
                la Distance entre les centres est D = sqrt[(c-a)²+(d-b)²]
                la condition pour qu'il y ait une intersection :
                    D < r0+r1 et D > abs(r0-r1)
                les solutions sont données par :
                    avec δ = 1/4*sqrt((D+r0+r1)(D+r0-r1)(D-r0+r1)(-D+r0+r1))
                    x1,2 = (a+c)/2 + (c-a)(r0²-r1²)/(2D²) +- 2δ(b-d)/D²
                    y1,2 = (b+d)/2 + (d-b)(r0²-r1²)/(2D²) -+ 2δ(a-c)/D²
        """

        a = dictCalc["c0"]["x"]
        b = dictCalc["c0"]["y"]
        c = dictCalc["c1"]["x"]
        d = dictCalc["c1"]["y"]
        r0 = dictCalc["r0"]
        r1 = dictCalc["r1"]

        dD = math.hypot((c-a), (d-b))
        if not (dD < (r0+r1) and dD > math.fabs(r0-r1)):
            print(f'pas de solutions')
            print(f'a -> {a} b -> {b} c -> {c} d -> {d} r0 -> {r0} r1 -> {r1}')
            print(f' --> Arrêt du programme')
            sys.exit(ABNORMAL_TERMINATION)

        part1X = (a+c)/2.
        part1Y = (b+d)/2.

        part2 = (r0*r0-r1*r1)/(2.*dD*dD)
        part2X = (c-a)*part2
        part2Y = (d-b)*part2

        delta = math.sqrt((dD+r0+r1)*(dD+r0-r1)*(dD-r0+r1)*(-dD+r0+r1))/(2.*dD*dD)
        deltaX = (b-d)*delta
        deltaY = (a-c)*delta

        x = part1X + part2X
        x1 = x + deltaX
        x2 = x - deltaX

        if x1 > x2:
            return (x1, part1Y + part2Y - deltaY)
        return (x2, part1Y + part2Y + deltaY)

    #-----
    @staticmethod
    def couture(dictCouture: dict) -> tuple:

        """
            Calcul de la couture sur le bord haut du développé
            Principe : à partir de 2 points successifs de la chainette donc une droite,
                on calcule 2 autres points décalés de fCouture et faisant un angle intérieur de angleR
                avec la droite

        """

        if "fCouture" in dictCouture and isinstance(dictCouture["fCouture"], float):
            fCouture = dictCouture["fCouture"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictCouture')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        angleR = math.radians(60.) # don't try 90°

        if "endroitDeb" in dictCouture and isinstance(dictCouture["endroitDeb"], di.Endroit2D):
            endroitDeb = dictCouture["endroitDeb"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictCouture')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "endroitFin" in dictCouture and isinstance(dictCouture["endroitFin"], di.Endroit2D):
            endroitFin = dictCouture["endroitFin"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictCouture')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        angleChainette = di.Direction2D(endroitFin - endroitDeb).angle2D()
        direction2DDeb = di.Direction2D({"vect2D": {"x": fCouture / math.tan(angleR) , "y": fCouture}})
        endroit2DCoutureDeb = endroitDeb + di.Direction2D(direction2DDeb.rot2d(angleChainette))

        angleChainette = di.Direction2D(endroitDeb - endroitFin).angle2D()
        direction2DFin = di.Direction2D({"vect2D": {"x": fCouture / math.tan(angleR) , "y": -fCouture}})
        endroit2DCoutureFin = endroitFin + di.Direction2D(direction2DFin.rot2d(angleChainette))

        return (endroit2DCoutureDeb["point2D"]["x"], endroit2DCoutureDeb["point2D"]["y"], \
                endroit2DCoutureFin["point2D"]["x"], endroit2DCoutureFin["point2D"]["y"] \
               )

    #-----
    def comp(self, dictDevelopp2D: dict) -> None:

        """
            Dans l'espace 2D le calcul a
        """

        if dictDevelopp2D["index"] == 0:

            endroit2DMil = di.Endroit2D({"point2D": {"x": 0., "y": 0.}})
            self.lendroit2DMil.append(endroit2DMil)

            fdist3DMilHaut = dictDevelopp2D["fdist3DMilHaut"]
            endroit2DHaut = di.Endroit2D({"point2D": {"x": 0., "y": fdist3DMilHaut}})
            self.lendroit2DHaut.append(endroit2DHaut)

            fdist3DMilBas = dictDevelopp2D["fdist3DMilBas"]
            endroit2DBas = di.Endroit2D({"point2D": {"x": 0., "y": -fdist3DMilBas}})
            self.lendroit2DBas.append(endroit2DBas)

            fdist3DMilHautChainette = dictDevelopp2D["fdist3DMilHautChainette"]
            endroit2DHautChainette = di.Endroit2D({"point2D": {"x": 0., "y": fdist3DMilHautChainette}})
            self.lendroit2DHautChainette.append(endroit2DHautChainette)

            fdist3DMilBasChainette = dictDevelopp2D["fdist3DMilBasChainette"]
            endroit2DBasChainette = di.Endroit2D({"point2D": {"x": 0., "y": -fdist3DMilBasChainette}})
            self.lendroit2DBasChainette.append(endroit2DBasChainette)

            self.lendroit2DHautCouture.append(endroit2DHautChainette)

        else:

            dictCalc = {}
            dictCalc['c0'] = self.endroit2DMil.p2ddict.getDict()
            dictCalc["r0"] = dictDevelopp2D["fdist3DMilMil"]
            dictCalc['c1'] = self.endroit2DHaut.p2ddict.getDict()
            dictCalc["r1"] = dictDevelopp2D["fdist3DHautMil"]
            (x, y) = Developp2D.calc(dictCalc=dictCalc)
            endroit2DMil = di.Endroit2D({"point2D": {"x": x, "y": y}})
            self.lendroit2DMil.append(endroit2DMil)

            dictCalc['c0'] = self.endroit2DMil.p2ddict.getDict()
            dictCalc["r0"] = dictDevelopp2D["fdist3DMilHaut"]
            dictCalc['c1'] = self.endroit2DHaut.p2ddict.getDict()
            dictCalc["r1"] = dictDevelopp2D["fdist3DHautHaut"]
            (x, y) = Developp2D.calc(dictCalc=dictCalc)
            endroit2DHaut = di.Endroit2D({"point2D": {"x": x, "y": y}})
            self.lendroit2DHaut.append(endroit2DHaut)

            dictCalc['c0'] = self.endroit2DMil.p2ddict.getDict()
            dictCalc["r0"] = dictDevelopp2D["fdist3DMilBas"]
            dictCalc['c1'] = self.endroit2DBas.p2ddict.getDict()
            dictCalc["r1"] = dictDevelopp2D["fdist3DBasBas"]
            (x, y) = Developp2D.calc(dictCalc=dictCalc)
            endroit2DBas = di.Endroit2D({"point2D": {"x": x, "y": y}})
            self.lendroit2DBas.append(endroit2DBas)

            dictCalc['c0'] = self.endroit2DMil.p2ddict.getDict()
            dictCalc["r0"] = dictDevelopp2D["fdist3DMilHautChainette"]
            dictCalc['c1'] = self.endroit2DHaut.p2ddict.getDict()
            dictCalc["r1"] = dictDevelopp2D["fdist3DHautHautChainette"]
            (x, y) = Developp2D.calc(dictCalc=dictCalc)
            endroit2DHautChainette = di.Endroit2D({"point2D": {"x": x, "y": y}})
            self.lendroit2DHautChainette.append(endroit2DHautChainette)

            dictCalc['c0'] = self.endroit2DMil.p2ddict.getDict()
            dictCalc["r0"] = dictDevelopp2D["fdist3DMilBasChainette"]
            dictCalc['c1'] = self.endroit2DBas.p2ddict.getDict()
            dictCalc["r1"] = dictDevelopp2D["fdist3DBasBasChainette"]
            (x, y) = Developp2D.calc(dictCalc=dictCalc)
            endroit2DBasChainette = di.Endroit2D({"point2D": {"x": x, "y": y}})
            self.lendroit2DBasChainette.append(endroit2DBasChainette)

            dictCouture = {}
            dictCouture["endroitDeb"] = self.lendroit2DHautChainette[-2]
            dictCouture["endroitFin"] = self.lendroit2DHautChainette[-1]
            dictCouture["fCouture"] = dictDevelopp2D["fCouture"]
            (x1, y1, x2, y2) = Developp2D.couture(dictCouture=dictCouture)
            endroit2DHautCouture = di.Endroit2D({"point2D": {"x": x1, "y": y1}})
            self.lendroit2DHautCouture.append(endroit2DHautCouture)
            endroit2DHautCouture = di.Endroit2D({"point2D": {"x": x2, "y": y2}})
            self.lendroit2DHautCouture.append(endroit2DHautCouture)
            #self.lendroit2DHautCouture.append(self.lendroit2DHautChainette[-1])

        self.endroit2DMil = self.lendroit2DMil[-1]
        self.endroit2DHaut = self.lendroit2DHaut[-1]
        self.endroit2DBas = self.lendroit2DBas[-1]

    #-----
    def horiz(self) -> None:

        """
            tout les points du panneau sont tournés pour être mis
            à "l'horizontale" définie par l'axe du millieu du panneau
        """

        alpha = di.Direction2D(self.lendroit2DMil[-1] - self.lendroit2DMil[0]).angle2D()

        lendroit2DMil = []
        lendroit2DHaut = []
        lendroit2DBas = []
        lendroit2DHautChainette = []
        lendroit2DBasChainette = []
        lendroit2DHautCouture = []

        for i in self.lendroit2DMil:
            lendroit2DMil.append(i.rot2d(fAth=-alpha))
        for i in self.lendroit2DHaut:
            lendroit2DHaut.append(i.rot2d(fAth=-alpha))
        for i in self.lendroit2DBas:
            lendroit2DBas.append(i.rot2d(fAth=-alpha))
        for i in self.lendroit2DHautChainette:
            lendroit2DHautChainette.append(i.rot2d(fAth=-alpha))
        for i in self.lendroit2DBasChainette:
            lendroit2DBasChainette.append(i.rot2d(fAth=-alpha))
        for i in self.lendroit2DHautCouture:
            lendroit2DHautCouture.append(i.rot2d(fAth=-alpha))

        self.lendroit2DMil = lendroit2DMil
        self.lendroit2DHaut = lendroit2DHaut
        self.lendroit2DBas = lendroit2DBas
        self.lendroit2DHautChainette = lendroit2DHautChainette
        self.lendroit2DBasChainette = lendroit2DBasChainette
        self.lendroit2DHautCouture = lendroit2DHautCouture

    #-----
    def createDxf(self, block) -> None:

        """
            la mise en place du dxf
        """

        # la ligne millieu en pointillé
        polyLineMil = block.add_lwpolyline([], dxfattribs={'color': couleur["jaune"], 'linetype': 'DOT2'})
        for i in self.lendroit2DMil:
            polyLineMil.append_points(points=[(i["point2D"]["x"], \
                                               i["point2D"]["y"])], \
                                               format='xy')

        # la ligne du haut en pointillé
        polyLineHaut = block.add_lwpolyline([], dxfattribs={'color': couleur["jaune"], 'linetype': 'DOT2'})
        for i in self.lendroit2DHaut:
            polyLineHaut.append_points(points=[(i["point2D"]["x"], \
                                                i["point2D"]["y"])], \
                                                format='xy')

        # la ligne du haut de chainette en plein
        polyLineHautChainette = block.add_lwpolyline([], dxfattribs={'color': couleur["bleu"]})
        for i in self.lendroit2DHautChainette:
            polyLineHautChainette.append_points(points=[(i["point2D"]["x"], \
                                                         i["point2D"]["y"])], \
                                                         format='xy')

        # la ligne du bas en pointillé
        polyLineBas = block.add_lwpolyline([], dxfattribs={'color': couleur["jaune"], 'linetype': 'DOT2'})
        for i in self.lendroit2DBas:
            polyLineBas.append_points(points=[(i["point2D"]["x"], \
                                               i["point2D"]["y"])], \
                                               format='xy')

        # la ligne du bas de chainette en plein
        polyLineBasChainette = block.add_lwpolyline([], dxfattribs={'color': couleur["bleu"]})
        for i in self.lendroit2DBasChainette:
            polyLineBasChainette.append_points(points=[(i["point2D"]["x"], \
                                                        i["point2D"]["y"])], \
                                                        format='xy')

        # la ligne de la couture en plein
        polyLineHautCouture = block.add_lwpolyline([], dxfattribs={'color': couleur["bleu"]})
        for i in self.lendroit2DHautCouture:
            polyLineHautCouture.append_points(points=[(i["point2D"]["x"], \
                                                       i["point2D"]["y"])], \
                                                       format='xy')

        # les lignes de section (la première et la dernière sont différentes)
        for i in range(len(self.lendroit2DBasChainette)):

            if i == 0 or i == len(self.lendroit2DBasChainette)-1:
                polyLineSection = block.add_lwpolyline([], dxfattribs={'color': couleur["bleu"]})
            else:
                polyLineSection = block.add_lwpolyline([], dxfattribs={'color': couleur["rouge"], 'lineweight': 20})

            polyLineSection.append_points(points=[(self.lendroit2DBasChainette[i]["point2D"]["x"], \
                                                   self.lendroit2DBasChainette[i]["point2D"]["y"])], \
                                                   format='xy')
            polyLineSection.append_points(points=[(self.lendroit2DHautChainette[i]["point2D"]["x"], \
                                                   self.lendroit2DHautChainette[i]["point2D"]["y"])], \
                                                   format='xy')

        # une inscription du numéro de panneau
        endroit2DDeb = di.Endroit2D(self.lendroit2DHaut[0])
        endroit2DFin = di.Endroit2D(self.lendroit2DHaut[-1])
        intHautText = di.Endroit2D(endroit2DDeb.lin2d(k=0.97, endroit2D=endroit2DFin))
        endroit2DDeb = di.Endroit2D(self.lendroit2DBas[0])
        endroit2DFin = di.Endroit2D(self.lendroit2DBas[-1])
        intBasText = di.Endroit2D(endroit2DDeb.lin2d(k=0.97, endroit2D=endroit2DFin))
        debText = intHautText.lin2d(k=0.55, endroit2D=intBasText)
        finText = intHautText.lin2d(k=0.45, endroit2D=intBasText)
        panneauNum = f'<-- bas Panneau numéro : {self.numPanneau} (chute) haut -->'
        block.add_text(panneauNum, \
                       dxfattribs={'style': 'OpenSansCondensed-Bold'} \
                      ).set_pos([debText["point2D"]["x"], debText["point2D"]["y"]], \
                                [finText["point2D"]["x"], finText["point2D"]["y"]], \
                                align='ALIGNED')

        # une inscription sur la chute
        endroit2DDeb = di.Endroit2D(self.lendroit2DMil[0])
        endroit2DFin = di.Endroit2D(self.lendroit2DMil[-1])
        debText = endroit2DDeb.lin2d(k=0.10, endroit2D=endroit2DFin)
        finText = endroit2DDeb.lin2d(k=0.15, endroit2D=endroit2DFin)
        copyRight = f'Créé par Pyjunk le {datetime.utcnow():%c} UTC±00:00'
        block.add_text(copyRight, \
                       dxfattribs={'style': 'OpenSansCondensed-Bold'} \
                      ).set_pos([debText["point2D"]["x"], debText["point2D"]["y"]], \
                                [finText["point2D"]["x"], finText["point2D"]["y"]], \
                                align='ALIGNED')

    #-----
    def __str__(self) -> str:

        strMsg = f'--> Developp2D                :\n'
        return strMsg

#----- Classe représentant le développé d'un panneau
class Developp(Developp2D):

    """

        Classe Developp
        ===============

        La classe Developp représente la partie 3D du calcul de développé

        :datas:

            self.dictDevelopp:  dict
            self.endroit3DMil:  Endroit3D
            self.endroit3DHaut: Endroit3D
            self.endroit3DBas:  Endroit3D

        :Example:

        >>> a = Developp({"numPanneau": 0})
        >>> print(a)
        --> Developp                :
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictDevelopp: dict) -> None:

        self.dictDevelopp = dictDevelopp

        # les anciens points 3D
        self.endroit3DMil = None
        self.endroit3DHaut = None
        self.endroit3DBas = None
        Developp2D.__init__(self, dictDevelopp2D=self.dictDevelopp)

    #-----
    def comp(self, dictDevelopp: dict) -> None:


        """
            La stratégie pour calculer les différents points du développé est simple.
            Ici on est dans l'espace 3D, dans la fonction hérité on est dans l'espace 2D.
            Le principe : en 3D, on mesure les distances du point recherché par rapport à
            2 autres points, on reporte ces distances en 2D à partir de 2 autres points 2D
            pour trouver le point 2D sur le développé
        """

        if "dictBas" in dictDevelopp and isinstance(dictDevelopp["dictBas"], dict):
            endroit3DBas = di.Endroit3D(dictDevelopp["dictBas"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "dictHaut" in dictDevelopp and isinstance(dictDevelopp["dictHaut"], dict):
            endroit3DHaut = di.Endroit3D(dictDevelopp["dictHaut"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "dictMil" in dictDevelopp and isinstance(dictDevelopp["dictMil"], dict):
            endroit3DMil = di.Endroit3D(dictDevelopp["dictMil"])
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "frac" in dictDevelopp and isinstance(dictDevelopp["frac"], float):
            frac = dictDevelopp["frac"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "index" in dictDevelopp and isinstance(dictDevelopp["index"], int):
            index = dictDevelopp["index"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        if "fCouture" in dictDevelopp and isinstance(dictDevelopp["fCouture"], float):
            fCouture = dictDevelopp["fCouture"]
        else:
            print(f'< !!!! > dictionnaire incorrect pour dictDevelopp')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # on charge un dictDevelopp2D
        dictDevelopp2D = {}
        dictDevelopp2D["index"] = index
        dictDevelopp2D["fCouture"] = fCouture

        if index == 0:

            # au premier tour on ne préoccupe pas de mil qui est (0, 0) par définition
            # on s'intéresse uniquement à haut, bas, hautchainette, baschainette 
            dictDevelopp2D["fdist3DMilHaut"] = endroit3DMil.dist3d(endroit3DHaut)
            dictDevelopp2D["fdist3DMilBas"] = endroit3DMil.dist3d(endroit3DBas)

            endroit3DHautChainette = di.Endroit3D(endroit3DMil.lin3d(k=frac, endroit3D=endroit3DHaut))
            dictDevelopp2D["fdist3DMilHautChainette"] = endroit3DMil.dist3d(endroit3DHautChainette)

            endroit3DBasChainette = di.Endroit3D(endroit3DMil.lin3d(k=frac, endroit3D=endroit3DBas))
            dictDevelopp2D["fdist3DMilBasChainette"] = endroit3DMil.dist3d(endroit3DBasChainette)

        else:

            # aux autres tours
            # on s'intéresse à millieu, haut, bas, hautchainette, baschainette
            dictDevelopp2D["fdist3DMilMil"] = self.endroit3DMil.dist3d(endroit3DMil)
            dictDevelopp2D["fdist3DHautMil"] = self.endroit3DHaut.dist3d(endroit3DMil)

            dictDevelopp2D["fdist3DMilHaut"] = self.endroit3DMil.dist3d(endroit3DHaut)
            dictDevelopp2D["fdist3DHautHaut"] = self.endroit3DHaut.dist3d(endroit3DHaut)

            dictDevelopp2D["fdist3DMilBas"] = self.endroit3DMil.dist3d(endroit3DBas)
            dictDevelopp2D["fdist3DBasBas"] = self.endroit3DBas.dist3d(endroit3DBas)

            endroit3DHautChainette = di.Endroit3D(endroit3DMil.lin3d(k=frac, endroit3D=endroit3DHaut))
            dictDevelopp2D["fdist3DMilHautChainette"] = self.endroit3DMil.dist3d(endroit3DHautChainette)
            dictDevelopp2D["fdist3DHautHautChainette"] = self.endroit3DHaut.dist3d(endroit3DHautChainette)

            endroit3DBasChainette = di.Endroit3D(endroit3DMil.lin3d(k=frac, endroit3D=endroit3DBas))
            dictDevelopp2D["fdist3DMilBasChainette"] = self.endroit3DMil.dist3d(endroit3DBasChainette)
            dictDevelopp2D["fdist3DBasBasChainette"] = self.endroit3DBas.dist3d(endroit3DBasChainette)

        # on lance le calcul dans l'espace 2D
        Developp2D.comp(self, dictDevelopp2D=dictDevelopp2D)

        # on sauvegarde les points pour le tour suivant
        self.endroit3DMil = endroit3DMil
        self.endroit3DHaut = endroit3DHaut
        self.endroit3DBas = endroit3DBas

    #-----
    def __str__(self) -> str:

        strMsg = f'--> Developp                :\n'
        return strMsg

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
