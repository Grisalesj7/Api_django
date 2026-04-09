#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Entrar a la carpeta donde está el manage.py
cd sistema_pedidos

# Ejecutar las migraciones para crear las tablas
python manage.py migrate

# Recolectar archivos estáticos (CSS, Imágenes)
python manage.py collectstatic --no-input

# Crear tu usuario (Cámbialos por los tuyos)
export DJANGO_SUPERUSER_PASSWORD="1234"
python manage.py createsuperuser --noinput --username admin --email admin@ejemplo.com || true