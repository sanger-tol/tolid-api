#!/bin/bash
APPDIR=$PWD
VENVDIR=$APPDIR/venv
PYTHONPATH=$PYTHONPATH:$APPDIR

# activate Python virtual environment
source $VENVDIR/bin/activate
python3 -m swagger_server

