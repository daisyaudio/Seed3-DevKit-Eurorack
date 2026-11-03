#!/bin/bash

echo "Generating Production and Review Materials for the project in this directory"

files=(*.kicad_pro)

if [[ ${#files[@]} -eq 0 ]]; then
	echo "Error: No KiCad project file found in the directory. Please run this script from a folder containing a .kicad_pro file."
	exit 1
elif [[ ${#files[@]} -gt 1 ]]; then
	echo "Error: More than one KiCad project file found in the directory. Please ensure only one .kicad_pro file exists."
	exit 1
fi

PROJECTFILE="${files[0]}"

# TODO: This should live somewhere permanent if it's not in the directory..
JOBFILE="GenProdMats.kicad_jobset"

if [[ ! -f "${JOBFILE}" ]]; then
	echo "Error: Job file '${JOBFILE}' not found. Please ensure it exists in the current directory."
	exit 1
fi

echo "Generating materials for project: ${PROJECTFILE}"
echo "Cleaning previously generated files..."
rm -r production/ review/
echo "Running KiCad Jobset..."
kicad-cli jobset run --stop-on-error --file=${JOBFILE} ${PROJECTFILE}
echo "Done."

echo "Beginning post-processing..."

# Get abs path to script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "${SCRIPT_DIR}/rename_centroid_fields.py"
python "${SCRIPT_DIR}/bom_append_avlpn.py"

echo "post-processing: zipping gerbers"

PROD_DIR="./production/"
GERBER_DIR_BASENAME=$(ls -d "$PROD_DIR"*/ | head -1 | xargs basename)

zip -r $PROD_DIR/$GERBER_DIR_BASENAME.zip $PROD_DIR/$GERBER_DIR_BASENAME

echo "Done."
