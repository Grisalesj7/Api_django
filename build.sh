#!/usr/bin/env bash
set -o errexit

echo "--- LISTADO DE ARCHIVOS EN LA RAÍZ ---"
ls -R

echo "--- INTENTANDO INSTALAR ---"
pip install -r requirements.txt

echo "--- BUSCANDO MANAGE.PY ---"
find . -name "manage.py"