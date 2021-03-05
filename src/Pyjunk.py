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
    Pyjunk.py rassemble la définition des classes:
        Baton
            BatonMillieu(Baton)
        Panneau
        Saildatas
        Loadjson
"""

from __future__ import annotations

import sys
import pathlib
import argparse
import locale
import json
import math

import Direction as di
import Models as md
import Chainette as ch
import Developp as de

#----- constantes pour finir le programme
NORMAL_TERMINATION = 0
ABNORMAL_TERMINATION = 1

try:

    import ezdxf

except ImportError:

    print(f'Probleme de chargement de la librairie ezdxf')
    print(f'Utiliser votre installateur préféré pour installer ezdxf')
    sys.exit(ABNORMAL_TERMINATION)

# instructions pour éviter un warning désagréable de "from stl import mesh"
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

try:

    import numpy as np
    from stl import mesh

except ImportError:

    print(f'Probleme de chargement de la librairie numpy-stl')
    print(f'Utiliser votre installateur préféré pour installer numpy-stl')
    sys.exit(ABNORMAL_TERMINATION)

#----- Classe représentant un baton
class Baton:

    """

        Classe Baton
        ============

        La classe Baton contient les données d'un baton avec 2 extremités

        :datas:

            self.dictBaton:    dict
            self.type:         str
            self.lextremites:  list
            self.fHtGuindant:  float
            self.fHtChute:     float
            self.dictV3dBaton: dict

        :Example:

        >>> p1 = {"type": "Guindant", "point3D": {"x":10.,"y":10.,"z":10.}}
        >>> p2 = {"type": "Chute", "point3D": {"x":20.,"y":20.,"z":20.}}
        >>> dict = {"type": "Bas","extremites": [p1, p2]}
        >>> print(f'{Baton(dict)}')
        Baton : Bas
        Guindant   : Point3D --> (X,Y,Z) = (   10.000,   10.000,   10.000) mm
        Chute      : Point3D --> (X,Y,Z) = (   20.000,   20.000,   20.000) mm
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

   """

    #-----
    def __init__(self, dictBaton: dict) -> None:

        self.dictBaton = dictBaton

        # Type : obligatoire
        if "type" in self.dictBaton:
            self.type = self.dictBaton["type"]
        else:
            print(f'< !!!! > Pas de clé "type" dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        self.lextremites = []
        if "extremites" in self.dictBaton:
            for i in self.dictBaton["extremites"]:
                extremite3D = di.Extremite3D(dictExtremite3D=i)
                self.lextremites.append(extremite3D)
        else:
            print(f'< !!!! > aucune extremites présentes dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # il n'y a que 2 extremites par baton
        if len(self.lextremites) != 2:
            print(f'< !!!! > Il n\'y a pas 2 extrémités par baton dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # le guindant est à l'extrémité 0 et la chute à l'extrémité 1
        if not (self.lextremites[0].getType() == "Guindant" and \
                self.lextremites[1].getType() == "Chute"):
            print(f'< !!!! > Organisation incorrecte des extrémités d\'un baton dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        self.fHtGuindant = self.lextremites[0].getHt()
        self.fHtChute = self.lextremites[1].getHt()

        self.dictV3dBaton = self.lextremites[1] - self.lextremites[0]

    #-----
    def getType(self) -> str:

        """ retourne le type """

        return self.type

    #-----
    def getHtsGuindant(self) -> tuple:

        """ retourne la hauteur guidant """

        return (self.fHtGuindant, )

    #-----
    def getHtsChute(self) -> tuple:

        """ retourne la hauteur chute """

        return (self.fHtChute, )

    #-----
    def getV3dDict(self) -> dict:

        """ retourne le vecteur du baton """

        return self.dictV3dBaton

    #-----
    def applyTwists(self, fHtMinChute: float, fHtMaxChute: float, fAtwistr: float) -> dict:

        """ applique le twist à chaque extrémités """

        dictBaton = self.dictBaton
        del dictBaton["extremites"]
        fAtwistrLocal = fAtwistr*(self.fHtChute - fHtMinChute)/(fHtMaxChute - fHtMinChute)
        lextremites = []
        for i in self.lextremites:
            lextremites.append(i.applyTwists(fAtwistr=fAtwistrLocal))
        dictBaton["extremites"] = lextremites
        return dictBaton

    #-----
    def startCalcs(self, fraction: float) -> dict:

        """ calcule la fraction entre les 2 extrémités du baton """

        return self.lextremites[0].lin3d(k=fraction, extremite3D=self.lextremites[1])

    #-----
    def __str__(self) -> str:

        strMsg = f'Baton : {self.type}\n'
        strMsg += f'{self.lextremites[0]}\n'
        strMsg += f'{self.lextremites[1]}\n'

        return strMsg

#-----
class BatonMillieu(Baton):

    """

        Classe BatonMillieu
        ===================

        La classe BatonMillieu est une spécialisation de Baton qui retourne un Baton millieu de 2 Batons

        :datas:

        :Example:

        >>> p11 = {"type": "Guindant", "point3D": {"x":10.,"y":10.,"z":10.}}
        >>> p21 = {"type": "Chute", "point3D": {"x":20.,"y":20.,"z":20.}}
        >>> dict1 = {"type": "Bas","extremites": [p11, p21]}
        >>> bas = Baton(dict1)
        >>> print(f'{bas}')
        Baton : Bas
        Guindant   : Point3D --> (X,Y,Z) = (   10.000,   10.000,   10.000) mm
        Chute      : Point3D --> (X,Y,Z) = (   20.000,   20.000,   20.000) mm
        <BLANKLINE>
        >>> p12 = {"type": "Guindant", "point3D": {"x":20.,"y":20.,"z":100.}}
        >>> p22 = {"type": "Chute", "point3D": {"x":40.,"y":40.,"z":200.}}
        >>> dict2 = {"type": "Haut","extremites": [p12, p22]}
        >>> haut = Baton(dict2)
        >>> print(f'{haut}')
        Baton : Haut
        Guindant   : Point3D --> (X,Y,Z) = (   20.000,   20.000,  100.000) mm
        Chute      : Point3D --> (X,Y,Z) = (   40.000,   40.000,  200.000) mm
        <BLANKLINE>
        >>> m = BatonMillieu(baton1=bas, baton2=haut)
        >>> print(f'{m}')
        Baton : Millieu
        Guindant   : Point3D --> (X,Y,Z) = (   15.000,   15.000,   55.000) mm
        Chute      : Point3D --> (X,Y,Z) = (   30.000,   30.000,  110.000) mm
        <BLANKLINE>

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    def __init__(self, baton1: Baton, baton2: Baton) -> None:

        dictMid1 = baton1.lextremites[0].mid3d(extremite3D=baton2.lextremites[0])
        dictMid2 = baton1.lextremites[1].mid3d(extremite3D=baton2.lextremites[1])
        dictExtremites = {"extremites": [dictMid1, dictMid2]}
        Baton.__init__(self, dictBaton={**{"type": "Millieu"}, **dictExtremites})

#----- Classe représentant les données d'un panneau de voile Junk
class Panneau:

    """

        Classe Panneau
        ==============

        La classe Panneau contient les données d'un panneau de voile Junk

        :datas:

            self.dictPanneau:  dict
            self.tHtsGuindant: tuple
            self.tHtsChute:    tuple
            self.numPanneau:   int
            self.lbatons:      list
            self.fChainLuff:   float
            self.fChainLuffp:  float
            self.fChainLeech:  float
            self.fChainLeechp: float
            self.fCouture:     float
            self.dictModel:    dict
            self.model:        Model
            self.lPoints:      list
            self.developp:     Developp

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, k: int, dictPanneau: dict) -> None:

        self.dictPanneau = dictPanneau

        self.tHtsGuindant = ()
        self.tHtsChute = ()

        #----- Nous chargeons les données globales pour chaque panneau
        # numPanneau : Entier, par défaut 0
        self.numPanneau = 0
        if "numPanneau" in self.dictPanneau and \
           isinstance(self.dictPanneau["numPanneau"], int):
            self.numPanneau = self.dictPanneau["numPanneau"]
        else:
            print(f'< !!!! > Pas de clé "numPanneau" ou clé incorrecte dans le Json valeur par défaut affectée 0')

        if self.numPanneau != k:
            print(f'< !!!! > séquence de panneaux incorrecte')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        #----- On s'occupe des batons
        self.lbatons = []
        if "batons" in self.dictPanneau:
            for i in self.dictPanneau["batons"]:
                baton = Baton(dictBaton=i)
                self.lbatons.append(baton)
        else:
            print(f'< !!!! > aucun baton présents dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # il doit y avoir 2 batons par panneau
        if len(self.lbatons) != 2:
            print(f'< !!!! > Il n\'y a pas 2 batons par panneau dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # le baton bas est à l'index 0 et le baton haut est à l'index 1
        if not (self.lbatons[0].getType() == "Bas" and \
                self.lbatons[1].getType() == "Haut"):
            print(f'< !!!! > Organisation incorrecte des batons par panneau dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # récupération hauteurs au guindant et à la chute
        self.tHtsChute += self.lbatons[0].getHtsChute()
        self.tHtsGuindant += self.lbatons[0].getHtsGuindant()

        # récupération hauteurs au guindant et à la chute
        self.tHtsChute += self.lbatons[1].getHtsChute()
        self.tHtsGuindant += self.lbatons[1].getHtsGuindant()

        # fChainLuff : flottant compris entre >= 0. et <= 10., par défaut 2.
        self.fChainLuff = 2.
        if "fChainLuff" in self.dictPanneau and \
           isinstance(self.dictPanneau["fChainLuff"], float) and \
           self.dictPanneau["fChainLuff"] >= 0. and \
           self.dictPanneau["fChainLuff"] <= 10.:
            self.fChainLuff = self.dictPanneau["fChainLuff"]
        else:
            print(f'< !!!! > Pas de clé "fChainLuff" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.fChainLuffp = self.fChainLuff/100.

        # fChainLeech : flottant compris entre >= 0. et <= 10., par défaut 2.
        self.fChainLeech = 2.
        if "fChainLeech" in self.dictPanneau and \
           isinstance(self.dictPanneau["fChainLeech"], float) and \
           self.dictPanneau["fChainLeech"] >= 0. and \
           self.dictPanneau["fChainLeech"] <= 10.:
            self.fChainLeech = self.dictPanneau["fChainLeech"]
        else:
            print(f'< !!!! > Pas de clé "fChainLeech" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.fChainLeechp = self.fChainLeech/100.

        # fCouture : flottant compris entre >= 0. et <= 24., par défaut 12.
        self.fCouture = 12.
        if "fCouture" in self.dictPanneau and \
        isinstance(self.dictPanneau["fCouture"], float) and \
        self.dictPanneau["fCouture"] >= 0. and \
        self.dictPanneau["fCouture"] <= 24.:
            self.fCouture = self.dictPanneau["fCouture"]
        else:
            print(f'< !!!! > Pas de clé "fCouture" ou clé incorrecte dans le Json valeur par défaut affectée')

        # model : dict, par défaut {"nameModel": "ModelFlat"}
        self.dictModel = {"nameModel": "ModelFlat"}
        if "model" in self.dictPanneau and \
           isinstance(self.dictPanneau["model"], dict):
            self.dictModel = self.dictPanneau["model"]
        else:
            print(f'< !!!! > Pas de clé "model" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.model = md.ModelSwitch(self.dictModel).getModel()

        # la liste des points répartis sur la surface
        self.lPoints = []

        # le développé du panneau
        self.developp = de.Developp({"numPanneau": self.numPanneau})

    #-----
    def getHtsGuindant(self) -> tuple:

        """ retourne le tuple des hauteurs au guindant """

        return self.tHtsGuindant

    #-----
    def getHtsChute(self) -> tuple:

        """ retourne le tuple des hauteurs à la chute """

        return self.tHtsChute

    #-----
    def applyTwists(self, fHtMinChute: float, fHtMaxChute: float, fAtwistr: float) -> dict:

        """ lance le calcul du twist de chaque baton """

        dictPanneau = self.dictPanneau
        del dictPanneau["batons"]
        lbatons = []
        for i in self.lbatons:
            lbatons.append(i.applyTwists(fHtMinChute=fHtMinChute, fHtMaxChute=fHtMaxChute, fAtwistr=fAtwistr))
        dictPanneau["batons"] = lbatons
        return dictPanneau

    #-----
    def startCalcs(self, nStepsDxf: int, nStepsStl: int) -> None:

        """ lance les calculs dans un panneau

            c'est la partie importante du programme
            1. on calcule un baton milieu du baton bas et du baton haut
            2. chaque panneau est découpé en nStepsDxf+1 tranches verticales
            3. ensuite, pour chaque tranche, on cherche la chainette correspondant au creux local
               et qui s'appuie sur le haut et le bas
            4. on peut alors calculer le developpé du panneau
            5. dans chaque chainette découpée en nStepStl+1 de chaque côté on calcule les points
               de la surface.

        """

        # calcul du baton millieu ... trivial, ce sera l'axe X', on le norme
        batonMil = BatonMillieu(baton1=self.lbatons[0], baton2=self.lbatons[1])
        direction3DMil = di.Direction3D(dictDirection3D=batonMil.getV3dDict())
        dictV3dMilNorm = direction3DMil.scaldiv3d(direction3DMil.norm3d())

        # découpe du panneau en section verticale
        for i in range(nStepsDxf+1):

            # la fraction dans la longueur du panneau
            frac = float(i)/float(nStepsDxf)

            # on applique le découpage aux 3 batons
            dictBas = self.lbatons[0].startCalcs(fraction=frac)
            dictHaut = self.lbatons[1].startCalcs(fraction=frac)
            dictMil = batonMil.startCalcs(fraction=frac)

            # le point origine du nouveau repère est la position sur le baton millieu, au format np
            npMil = np.array([dictMil['point3D']['x'], dictMil['point3D']["y"], dictMil['point3D']["z"]])

            # on calcule le vecteur dictBas <-> dictHaut, l'axe Z', on le norme
            dictV3dBasHaut = di.Extremite3D(dictExtremite3D=dictHaut) - di.Extremite3D(dictExtremite3D=dictBas)
            direction3DBasHaut = di.Direction3D(dictDirection3D=dictV3dBasHaut)
            dictV3dBasHautNorm = direction3DBasHaut.scaldiv3d(direction3DBasHaut.norm3d())

            # puis, par produit vectoriel de dictV3dMil (X') par dictV3dBasHaut (Z'), on obtient l'axe -Y'
            # on le norme, noter le - dans le scaldiv3d pour avoir le Y'
            dictV3dY = direction3DMil.prodvect3d(direction=direction3DBasHaut)
            direction3DY = di.Direction3D(dictDirection3D=dictV3dY)
            dictV3dYNorm = direction3DY.scaldiv3d(-direction3DY.norm3d())

            # on a donc un nouveau repère, d'où une matrice de passage du nouveau repère à l'ancien
            # sous format np
            npPassage = np.array([
                [dictV3dMilNorm['vect3D']['x'], dictV3dYNorm['vect3D']['x'], dictV3dBasHautNorm['vect3D']['x']],
                [dictV3dMilNorm['vect3D']['y'], dictV3dYNorm['vect3D']['y'], dictV3dBasHautNorm['vect3D']['y']],
                [dictV3dMilNorm['vect3D']['z'], dictV3dYNorm['vect3D']['z'], dictV3dBasHautNorm['vect3D']['z']]
                                 ])

            # on calcule la chainette locale (pour cette section)
            dictChainette = {}
            dictChainette["ecartement"] = di.Extremite3D(dictExtremite3D=dictBas) \
                                         .dist3d(di.Extremite3D(dictExtremite3D=dictHaut))
            dictChainette["creux"] = self.model.getCreux(fraction=frac)
            chainette = ch.Chainettedict(dictChainette)

            # on peut dès lors incrémenter le calcul du développé du panneau pour cette section
            dictDevelopp = {}
            dictDevelopp["index"] = i
            dictDevelopp["dictBas"] = {"point3D": dictBas["point3D"]}
            dictDevelopp["dictHaut"] = {"point3D": dictHaut["point3D"]}
            dictDevelopp["dictMil"] = {"point3D": dictMil["point3D"]}
            dictDevelopp["fCouture"] = self.fCouture
            dictDevelopp["frac"] = chainette.compCurv(fX=dictChainette["ecartement"]/2.) / \
                                   (dictChainette["ecartement"]/2.)
            self.developp.comp(dictDevelopp=dictDevelopp)

            # on calcule les points de la surface
            lPointsChainette = []
            for j in range(nStepsStl+1):

                # dans l'espace 2D de la chainette, on calcule la profondeur de la chainette
                fX = (float(j) * dictChainette["ecartement"]) / (2. * float(nStepsStl))
                fY = chainette.comp(fX=fX)

                # la chainette étant symétrique, avec un calcul on fait 2 points au format np
                # et dans l'espace de la chainette
                npPoint1 = np.array([0., fY, fX])
                npPoint2 = np.array([0., fY, -fX])

                # on convertit ce point dans le repère normal
                npPoint1N = npPassage @ npPoint1 + npMil
                npPoint2N = npPassage @ npPoint2 + npMil
                lPointsChainette.append([npPoint1N, npPoint2N])

            self.lPoints.append(lPointsChainette)

        # on horizontalize le panneau développé
        self.developp.horiz()

    #-----
    def createStl(self, nStepsDxf: int, nStepsStl: int) -> list:

        """
            retourne le tableau des sommets des triangles dans le panneau
            en traitant simultanément les 2 côtés de la chainete, on récupère un quadrilatère
            que l'on divise en 2 triangles
        """

        lFacettes = []
        for i in range(nStepsDxf):
            lChain1 = self.lPoints[i]
            lChain2 = self.lPoints[i+1]
            for j in range(nStepsStl):
                lPoint11 = lChain1[j]
                lPoint12 = lChain1[j+1]
                lPoint21 = lChain2[j]
                lPoint22 = lChain2[j+1]
                lFacettes.append([lPoint11[0].tolist(), lPoint21[0].tolist(), lPoint22[0].tolist()])
                lFacettes.append([lPoint11[0].tolist(), lPoint12[0].tolist(), lPoint22[0].tolist()])
                lFacettes.append([lPoint11[1].tolist(), lPoint21[1].tolist(), lPoint22[1].tolist()])
                lFacettes.append([lPoint11[1].tolist(), lPoint12[1].tolist(), lPoint22[1].tolist()])

        return lFacettes

    #-----
    def createDxf(self, drawing: ezdxf.document.Drawing) -> None:

        """ charge les points du développé de chaque panneau dans un bloc """

        blockPanneau = drawing.blocks.new(name='Panel #'+str(self.numPanneau))
        self.developp.createDxf(block=blockPanneau)

    #-----
    def __str__(self) -> None:

        strMsg = f'Panneau numéro : {self.numPanneau:>9d}\n'
        strMsg += f'--> Chainette guindant     : {self.fChainLuff:>9.3f}% <=> {self.fChainLuffp:>9.3f}\n'
        strMsg += f'--> Chainette chute        : {self.fChainLeech:>9.3f}% <=> {self.fChainLeechp:>9.3f}\n'
        strMsg += f'--> Largeur de la couture  : {self.fCouture:>9.3f}\n'
        strMsg += f'{self.model}'
        strMsg += f'--> {self.lbatons[0]}'
        strMsg += f'--> {self.lbatons[1]}'
        return strMsg

#----- Classe représentant les données de la voile Junk
class Saildatas:

    """

        Classe Saildatas
        ================

        La classe Saildatas contient les données de la voile

        :datas:

            self.dictVoile:      dict
            self.tHtsGuindant:   tuple
            self.tHtsChute:      tuple
            self.fileDxf:        str
            self.fileStl:        str
            self.nStepsDxf:      int
            self.nStepsStl:      int
            self.fAtwist:        float
            self.fAtwistr:       float
            self.lpanneaux:      list
            self.fHtMinChute:    float
            self.fHtMaxChute:    float
            self.fHtMinGuindant: float
            self.fHtMaxGuindant: float

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, dictVoile: dict) -> None:

        # on sauv dictVoile
        self.dictVoile = dictVoile

        # Hauteurs au guindant et à la chute
        self.tHtsGuindant = ()
        self.tHtsChute = ()

        #----- Nous commencons par les données globales - les clés suivantes :

        # filedxf: str
        if "filedxf" in self.dictVoile and \
           isinstance(self.dictVoile["filedxf"], str):
            self.fileDxf = self.dictVoile["filedxf"]
        else:
            print(f'< !!!! > Pas de clé "filedxf" ou clé incorrecte dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # filestl: str
        if "filestl" in self.dictVoile and \
           isinstance(self.dictVoile["filestl"], str):
            self.fileStl = self.dictVoile["filestl"]
        else:
            print(f'< !!!! > Pas de clé "filestl" ou clé incorrecte dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # nStepsDxf : entier compris entre >= 5 et <= 500, par défaut 20
        self.nStepsDxf = 20
        if "nStepsDxf" in self.dictVoile and \
            isinstance(self.dictVoile["nStepsDxf"], int) and \
            self.dictVoile["nStepsDxf"] >= 5 and \
            self.dictVoile["nStepsDxf"] <= 500:
            self.nStepsDxf = self.dictVoile["nStepsDxf"]
        else:
            print(f'< !!!! > Pas de clé "nStepsDxf" ou clé incorrecte dans le Json valeur par défaut affectée')

        # nStepsStl : entier compris entre >= 5 et <= 500, par défaut 20
        self.nStepsStl = 20
        if "nStepsStl" in self.dictVoile and \
            isinstance(self.dictVoile["nStepsStl"], int) and \
            self.dictVoile["nStepsStl"] >= 5 and \
            self.dictVoile["nStepsStl"] <= 500:
            self.nStepsStl = self.dictVoile["nStepsStl"]
        else:
            print(f'< !!!! > Pas de clé "nStepsStl" ou clé incorrecte dans le Json valeur par défaut affectée')

        # fAtwist : flottant compris entre >= 0. et <= 24., par défaut 0.
        # A noter que le twist est appliqué tribord amures (donc négatif)
        self.fAtwist = 0.
        if "fAtwist" in self.dictVoile and \
        isinstance(self.dictVoile["fAtwist"], float) and \
        self.dictVoile["fAtwist"] >= 0. and \
        self.dictVoile["fAtwist"] <= 24.:
            self.fAtwist = -self.dictVoile["fAtwist"]
        else:
            print(f'< !!!! > Pas de clé "fAtwist" ou clé incorrecte dans le Json valeur par défaut affectée')
        self.fAtwistr = math.radians(self.fAtwist)

        # Lecture des différents panneaux
        self.lpanneaux = []
        if "panneaux" in self.dictVoile:
            k = 0
            for i in self.dictVoile["panneaux"]:
                k += 1
                panneau = Panneau(k=k, dictPanneau=i)
                self.tHtsGuindant += panneau.getHtsGuindant()
                self.tHtsChute += panneau.getHtsChute()
                self.lpanneaux.append(panneau)
        else:
            print(f'< !!!! > aucun panneau présents dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        self.fHtMinChute = min(self.tHtsChute)
        self.fHtMaxChute = max(self.tHtsChute)
        self.fHtMinGuindant = min(self.tHtsGuindant)
        self.fHtMaxGuindant = max(self.tHtsGuindant)

    #-----
    def applyTwists(self) -> dict:

        """
            le calcul du twist est une rotation autour de z de tout les panneaux
            on l'effectue vers tribord cad avec un angle négatif
            la quantité de rotation est linéaire selon la hauteur de la chute
        """

        dictTwist = self.dictVoile
        del dictTwist["panneaux"]
        panneaux = []
        for i in self.lpanneaux:
            panneaux.append(i.applyTwists(fHtMinChute=self.fHtMinChute, \
                                          fHtMaxChute=self.fHtMaxChute, \
                                          fAtwistr=self.fAtwistr))
        dictTwist["panneaux"] = panneaux
        return dictTwist

    #-----
    def startCalcs(self) -> None:

        """ le calcul des différentes sections, baton milieu, etc """

        for i in self.lpanneaux:
            i.startCalcs(nStepsDxf=self.nStepsDxf, nStepsStl=self.nStepsStl)

    #-----
    def createStl(self) -> None:

        """ la création du fichier stl """

        lFacettes = []
        for i in self.lpanneaux:
            lFacettes += i.createStl(nStepsDxf=self.nStepsDxf, nStepsStl=self.nStepsStl)
        voileStl = mesh.Mesh(np.zeros(len(lFacettes), dtype=mesh.Mesh.dtype))
        voileStl.vectors = lFacettes
        voileStl.save(self.fileStl)
        print(f'Fichier stl "{self.fileStl}" --> créé')

    #-----
    def createDxf(self) -> None:

        """ la création du fichier stl """

        #----- definition du dessin
        drawingDraw = ezdxf.new(dxfversion='AC1032', setup=True)

        #----- definition d'un layer de base
        layerVoile = drawingDraw.layers.new(name='Voile')
        layerVoile.off()
        layerVoile.lock()

        #----- mise en place du dessin de chaque développé
        for i in self.lpanneaux:
            i.createDxf(drawing=drawingDraw)

        #----- on sauve
        drawingDraw.saveas(self.fileDxf)
        print(f'Fichier dxf "{self.fileDxf}" --> créé')

    #-----
    def __str__(self) -> str:

        strMsg = f'SailDatas :\n'
        strMsg += f'--> Fichier dxf                : {self.fileDxf}\n'
        strMsg += f'--> Fichier stl                : {self.fileStl}\n'
        strMsg += f'--> Nombre de subdivisions dxf : {self.nStepsDxf:>9d}\n'
        strMsg += f'--> Nombre de subdivisions stl : {self.nStepsStl:>9d}\n'
        strMsg += f'--> Angle de Twist             : {self.fAtwist:>9.3f}° <=> {self.fAtwistr:>9.3f} rad\n'

        for i in self.lpanneaux:
            strMsg += f'\n'
            strMsg += str(i)

        return strMsg

#----- Classe de trancodage du fichier Json de paramétrage de la voile
class Loadjson:

    """

        Classe Loadjson
        ===============

        Classe de lecture du Json - transcodage en dict python

        :datas:

            self.params: json

        .. seealso::
        .. warning::
        .. note::
        .. todo::

    """

    #-----
    def __init__(self, fileIn) -> None:

        try:

            self.params = json.load(fileIn)

        except json.JSONDecodeError as err:

            print(f'Le fichier Json est incorrect')
            print(f'--> message : {err.msg}')
            print(f'--> pos     : {err.pos}')
            print(f'--> lineno  : {err.lineno}')
            print(f'--> colno   : {err.colno}')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

    #-----
    def getDict(self) -> dict:

        """ retourne le json sous forme de dict """

        return self.params

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

    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    sProg = f'pyjunk.py'
    sDescription = f'Développé d\'une voile Junk'
    sEpilog = f'Author : Marc JOURDAIN 2021'

    parser = argparse.ArgumentParser(prog=sProg,
                                     description=sDescription,
                                     epilog=sEpilog)

    msgHelpinJson = f'fichier de paramétrage au format Json'
    parser.add_argument(f'--fIn',
                        action='store',
                        required=True,
                        help=msgHelpinJson)

    options = parser.parse_args()

    print(f'Lecture du fichier Json : {options.fIn}')
    print()

    # tentative ouverture du fichier fIn
    try:

        fIn = open(f'{options.fIn}', 'r')
        encode = Loadjson(fileIn=fIn)
        dictParams = encode.getDict()
        if "_comment" in dictParams:
            print(f'--> {dictParams["_comment"]}')
        if "_date" in dictParams:
            print(f'--> {dictParams["_date"]}')
        if "_auteur" in dictParams:
            print(f'--> {dictParams["_auteur"]}')
        print(f'')
        if not "voile" in dictParams:
            print(f'Pas de clé "voile" dans le Json')
            print(f'program aborted')
            sys.exit(ABNORMAL_TERMINATION)

        # Dans un premier temps, on construit la voile de base à partir des données du Json
        junkSailBase = Saildatas(dictParams["voile"])
        # Dans un second temps, on reconstruit la voile twistée à partir du dict twisté
        # renvoyé par la fonction Panneau.applyTwists
        junkSailTwist = Saildatas(junkSailBase.applyTwists())
        # Dans un troisième temps, on lance les calculs sur la voile twistée
        junkSailTwist.startCalcs()

        #print(f'{junkSailBase}')
        #print(f'{junkSailTwist}')

        # générer le stl
        junkSailTwist.createStl()

        # générer le dxf
        junkSailTwist.createDxf()

    except IOError as err:

        print(f'{options.fIn} : No such file')
        print(f'program aborted')
        #sys.exit(ABNORMAL_TERMINATION)

    finally:

        print(f'{options.fIn} --> closed')

    print()
    print(f'Fin du programme')
    sys.exit(NORMAL_TERMINATION)
