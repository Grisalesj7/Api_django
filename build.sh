#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar comandos usando la ruta del archivo manage.py desde la raíz
# Si tu archivo está en sistema_pedidos/manage.py, usamos esa ruta:
python sistema_pedidos/manage.py migrate
python sistema_pedidos/manage.py collectstatic --no-input

# Crear superusuario
export DJANGO_SUPERUSER_PASSWORD="1234"
python sistema_pedidos/manage.py createsuperuser --noinput --username admin --email admin@ejemplo.com || true