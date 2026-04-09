# Salir si hay un error
set -o errexit

# Instalar dependencias (esto se hace en la raíz)
pip install -r requirements.txt

# --- EL CAMBIO ESTÁ AQUÍ ---
# Entrar a la carpeta donde está manage.py
cd sistema_pedidos

# Ahora sí, los comandos de Django
python manage.py migrate
python manage.py collectstatic --no-input

# Crear superusuario
export DJANGO_SUPERUSER_PASSWORD="1234"
python manage.py createsuperuser --noinput --username admin --email admin@ejemplo.com || true