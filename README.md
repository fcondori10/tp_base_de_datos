# tp_base_de_datos
Trabajo práctico base de datos
# Configuración

## Se requieren las bibliotecas
```bash
pip install psycopg2
pip install djongo
pip install pymongo
```


## crear base de datos en PostgreSQL

```bash
create database tiendabd
```
### En settings.py agregar la base de datos con la contraseña y puerto correspondientes

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tiendabd',
        'USER': 'postgres',
        'PASSWORD': 'micontrasenia',
        'HOST': '127.0.0.1',
        'PORT':'5432',
    }
}
```

### En el directorio donde esta manage.py ejecutar los comandos
```bash
python manage.py makemigrations
python manage.py migrate
```

## Crear base de datos en Mongodb y una coleccion
### En settings.py configurar base de datos de MongoDB con puerto, nombre de la bd y nombre de la coleccion
```bash
MONGO_HOST = 'localhost' 
MONGO_PORT = 27017
MONGO_BD = 'mitienda'
MONGO_COLLECTION = 'productos'
```

# Ejecutar
### Para correr el proyecto ejecutar el siguiente comando e ir a la direccion para ver la pagina:
```bash
python manage.py runserver
```


