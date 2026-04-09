#!/usr/bin/env bash
# Salir inmediatamente si ocurre un error
set -o errexit

# 1. Instalar las librerías del requirements.txt
pip install -r requirements.txt

# 2. Recolectar archivos estáticos (CSS, Imágenes, JS)
# Esto es vital para que tu página no se vea sin diseño en Render
python manage.py collectstatic --no-input

# 3. Aplicar las tablas a la base de datos de la nube
python manage.py migrate

# Crear superusuario automáticamente si no existe
export DJANGO_SUPERUSER_PASSWORD="1234"
python manage.py createsuperuser --noinput --username admin --email admin@ejemplo.com || true