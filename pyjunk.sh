#
# Lanceur de Pyjunk.py
#
# Options :
#
#		--fIn <file> : Nom du fichier de paramètre au format Json (par défaut "./examples/johanna.json")
#

SRC="./src"

if [ -z ${1} ]; then
    FILE="./examples/johanna.json"
else
    FILE=${1}
fi

${SRC}/Geom.py && \
${SRC}/Direction.py && \
${SRC}/Models.py && \
${SRC}/Zbrent.py && \
${SRC}/Zbrac.py && \
${SRC}/Chainette.py && \
${SRC}/Developp.py && \

time -p ${SRC}/Pyjunk.py --fIn ${FILE}
