# Pyjunk

Pyjunk est un programme écrit en Python3 qui peut aider à la conception de voiles de [jonque](https://www.junkrigassociation.org/).

A partir d'un fichier json décrivant les différents panneaux, Pyjunk calcule un fichier [stl](https://fr.wikipedia.org/wiki/Fichier_de_st%C3%A9r%C3%A9olithographie) représentant la voile en 3D et un fichier [dxf](https://fr.wikipedia.org/wiki/Drawing_eXchange_Format) représentant les développés de chaque panneau.

Ces 2 fichiers nécessitent un "viewer" spécifique.

## Installation

Avec git

```bash
git clone https://github.com/ashmorecartier/Pyjunk
```

2 extensions sont indispensables : 
* [ezdxf](https://pypi.org/project/ezdxf/),
* [numpy-stl](https://numpy-stl.readthedocs.io/en/latest/usage.html). 


## Usage

Avec un fichier exemple fourni :
```bash
cd Pyjunk; ./pyjunk.sh
```
ou, avec votre propre fichier json

```bash
cd Pyjunk; ./pyjunk.sh <votre fichier.json>
```

## Description du json décrivant une voile junk


Dans un système de coordonnées :
* axe x: d'avant en arrière sur l'axe du bateau,
* axe z: de bas en haut

On peut commencer en (0, 0, 0) 

De haut en bas, le fichier contient :
* des données globales pour le traitement,
* une voile,
* des panneaux,
* deux batons,
* deux extrémités,
* un point.

De bas en haut, maintenant :

* un point a la représentantion suivante dans le repère précédemment décrit :
```json
    "point3D": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    }
```
* une extrémité est un point avec un type ("Guindant" ou "Chute") :
```json
    "type": "Guindant",
    "point3D": {
        ...
    }
```
* un baton a un type ("Haut" ou "Bas") et 2 extrémités :
```json
    "type": "Haut",
    "extremites": [
        {
            "type": "Guindant",
                ...
        },
        {
            "type": "Chute",
                ...
        }
    ]
```
* un panneau a un numéro, 2 batons ("Bas" et "Haut"), un pourcentage de chainette guindant et chute, une largeur de couture sur la partie haute et un modèle de creux (on y reviendra):
```json
    "numPanneau": 1,
    "batons": [
        {
            "type": "Bas",
            "extremites": [
                ...
            ]
        },
        {
            "type": "Haut",
            "extremites": [
                ...
            ]
        }
    ],
    "fChainLuff": 2.0,
    "fChainLeech": 2.0,
    "fCouture": 12.0,
    "model": {
        "nameModel": "ModelTube",
        "paramModel": {
            "rpdepthmin": 15.0,
            "rpdepthmax": 85.0,
            "creuxmax": 100.0
        }
    }
```
* une voile a un nom de ficher dxf en sortie, un nom de fichier stl en sortie, un nombre de subdivisions horizontales, un nombre de subdivisions verticales et un ou plusieurs panneaux :
```json
    "voile": {
        "filedxf": "./examples/johanna.dxf",
        "filestl": "./examples/johanna.stl",
        "nStepsDxf": 20,
        "nStepsStl": 40,
        "fAtwist": 10.0,
        "panneaux": [
            {
                "numPanneau": 1,
                ...
            },
            {   "numPanneau": 2,
                ...
            },
            ...
        ]
    }
 
```
* une description générale au plus haut niveau :
```json
{
    "_comment": "paramétrage d'une voile junk (Johanna)",
    "_date": "date de création 2021/02/04",
    "_auteur": "auteur Marc Jourdain",
    "voile": {
        ...
    }
} 
```


Rassurez-vous, il existe un outil (tools/CreateJson.py) qui fabrique le json à partir d'un tableau de cotes. Il existe également une feuille de calcul (tools/Modele.ods).

## Modèles de creux

Pyjunk prend en compte un modèle de creux panneau par panneau. On entend par ceci que le creux du panneau va varier du guindant à la chute. Il existe actuellement 3 modèles de creux possibles :

* le modèle "flat", le creux est nul,
```json
    "model": {
        "nameModel": "ModelFlat"
    }
```
* le modèle "parabolique", le creux part de 0, passe par un maximum, puis finit à 0,
```json
    "model": {
        "nameModel": "ModelParabolique",
        "paramModel": {
            "rpdepth": 35.0,
            "creuxmax": 80.0
        }
    }
```
* le modèle "tube", le creux part de 0, puis est constant, puis finit à 0.
```json
    "model": {
        "nameModel": "ModelTube",
        "paramModel": {
            "rpdepthmin": 15.0,
            "rpdepthmax": 85.0,
            "creuxmax": 100.0
        }
    }
```

## License
[MIT](https://choosealicense.com/licenses/mit/)