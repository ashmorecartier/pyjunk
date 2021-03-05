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

import json
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# paramétres globaux
_comment = "paramétrage d'une voile junk (Johanna)"
_date = "date de création 2021/02/04"
_auteur = "auteur Marc Jourdain"

# paramétres voile
filedxf = "./examples/johanna.dxf" 
filestl = "./examples/johanna.stl"
nStepsDxf = 20
nStepsStl = 40
fAtwist = 10.0

# liste des batons (guindant [x,y,z] - chute [x,y,z]) 
listeBatonsxyz = [
    ([0.00, 0.00,    0.00], [3480.83, 0.00,  365.85]), #1
    ([0.00, 0.00,  700.00], [3480.83, 0.00, 1065.85]), #2
    ([0.00, 0.00, 1400.00], [3480.83, 0.00, 1765.85]), #3
    ([0.00, 0.00, 2100.00], [3480.83, 0.00, 2465.85]), #4
    ([0.00, 0.00, 2800.00], [3480.83, 0.00, 3165.85]), #5
    ([0.00, 0.00, 3150.00], [3061.17, 0.00, 4846.83]), #6
    ([0.00, 0.00, 3325.00], [2154.82, 0.00, 6083.04]), #7
    ([0.00, 0.00, 3412.00], [ 905.87, 0.00, 6793.24])  #8
]

# liste des caractéristiques des panneaux
# numéro (commence à 1), fChainLuff, fChainLeech, fCouture, model
listePanneauxDesc = [
    (1, 2.0, 2.0, 12.0, {"nameModel": "ModelTube",
                         "paramModel": {"rpdepthmin": 15.0, "rpdepthmax": 85.0, "creuxmax": 100.0 }
                        }),
    (2, 2.0, 2.0, 12.0, {"nameModel": "ModelTube",
                         "paramModel": {"rpdepthmin": 15.0, "rpdepthmax": 85.0, "creuxmax": 100.0 }
                        }),
    (3, 2.0, 2.0, 12.0, {"nameModel": "ModelTube",
                         "paramModel": {"rpdepthmin": 15.0, "rpdepthmax": 85.0, "creuxmax": 100.0 }
                        }),
    (4, 2.0, 2.0, 12.0, {"nameModel": "ModelTube",
                         "paramModel": {"rpdepthmin": 15.0, "rpdepthmax": 85.0, "creuxmax": 100.0 }
                        }),
    (5, 2.0, 2.0, 12.0, {"nameModel": "ModelParabolique",
                         "paramModel": {"rpdepth": 35.0, "creuxmax": 80.0 }
                        }),
    (6, 2.0, 2.0, 12.0, {"nameModel": "ModelParabolique",
                         "paramModel": {"rpdepth": 35.0, "creuxmax": 60.0 }
                        }),
    (7, 2.0, 2.0, 12.0, {"nameModel": "ModelFlat"
                        })
]

listeBatons = []
for i in listeBatonsxyz:
    dictPointGuindant = {"type": "Guindant", "point3D": {"x": i[0][0], "y": i[0][1], "z": i[0][2]}}
    dictPointChute    = {"type": "Chute",    "point3D": {"x": i[1][0], "y": i[1][1], "z": i[1][2]}}
    listeBatons.append([dictPointGuindant, dictPointChute])

listePanneaux = []
j = 0
for i in listePanneauxDesc:
    dictPanneau = {}
    dictPanneau["numPanneau"] = i[0]
    dictPanneau["batons"] = [{"type": "Bas", "extremites": listeBatons[j]}, {"type": "Haut", "extremites": listeBatons[j+1]}]
    dictPanneau["_comment-fChainLuff"]  = "Côté guidant pourcentage de fLluff valant creux de la chainette (flottant compris entre >= 0. et <= 10., par défaut 2.)"
    dictPanneau["fChainLuff"] = i[1]
    dictPanneau["_comment-fChainLeech"] = "Côté chute pourcentage de fLleech valant creux de la chainette (flottant compris entre >= 0. et <= 10., par défaut 2.)"
    dictPanneau["fChainLeech"] = i[2]
    dictPanneau["_comment-fCouture"] = "Largeur de la couture (flottant compris entre >= 0. et <= 24., par défaut 12.°)"
    dictPanneau["fCouture"] = i[3]
    dictPanneau["_comment-model"] = "Model tube, un modèle avec un creux donné entre deux positions définies en pourcentage"
    dictPanneau["model"] = i[4]
    listePanneaux.append(dictPanneau)
    j += 1

dictGlobal = {
    "_comment": _comment,
    "_date": _date,
    "_auteur": _auteur,
    "voile": {
        "_comment-filedxf": "Ficher dxf de sortie",
        "filedxf": filedxf,
        "_comment-filestl": "Ficher stl de sortie",
        "filestl": filestl,
        "_comment-nStepsDxf": "Nombre de pas de subdivision (entier compris entre >= 5 et <= 500, par défaut 20)",
        "nStepsDxf": nStepsDxf,
        "_comment-nStepsStl": "Nombre de pas de subdivision (entier compris entre >= 5 et <= 500, par défaut 20)",
        "nStepsStl": nStepsStl,
        "_comment-fAtwist": "Angle en degrés du vrillage de la voile (flottant compris entre >= 0. et <= 24., par défaut 0°)",
        "fAtwist": fAtwist,
        "_comment-panneaux": "Description des différents panneaux du bas vers le haut, chaque panneau est décrit par 2 batons, bas et haut",
        "panneaux": listePanneaux
    }
}

print(f'{json.dumps(dictGlobal, indent=4)}')