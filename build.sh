#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# --- COMANDO INTELIGENTE ---
# Busca manage.py y ejecuta las migraciones donde sea que esté
find . -name "manage.py" -exec python {} migrate \;
find . -name "manage.py" -exec python {} collectstatic --no-input \;

# Crear superusuario (ajusta tus datos)
export DJANGO_SUPERUSER_PASSWORD="1234"
find . -name "manage.py" -exec python {} createsuperuser --noinput --username admin --email admin@ejemplo.com \; || true