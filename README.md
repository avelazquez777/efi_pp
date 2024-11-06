# API de Tienda de celulares

Este proyecto es una API RESTful para gestionar el stock de equipos. Utiliza Flask como framework web y Flask-JWT-Extended para la autenticación JWT. Los datos de stock se almacenan en una base de datos MySQL y son manipulados mediante SQLAlchemy.

## Requisitos

- Python 3.x
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- MySQL (o cualquier otra base de datos compatible con SQLAlchemy)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu máquina local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/efi_pp.git
cd gestion_stock
```

### 2. Crear y activar un entorno virtual

Si no tienes un entorno virtual creado, crea uno e instálalo.

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### 3. Instalar dependencias

Instala las dependencias necesarias utilizando `pip`.

```bash
pip install -r requirements.txt
```

### 4. Configuración de la base de datos

Configura la base de datos de MySQL en el archivo `.env` o en la configuración de la aplicación, asegurándote de que los detalles de conexión son correctos.

Ejemplo de archivo `.env`:

```
DATABASE_URI=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_base_de_datos
SECRET_KEY=tu_clave_secreta
```

### 5. Ejecutar la migración de base de datos

Si estás usando migraciones de base de datos con Alembic o Flask-Migrate, asegúrate de ejecutar las migraciones.

```bash
flask db upgrade
```

### 6. Ejecutar la aplicación

Para ejecutar el servidor Flask en modo de desarrollo, usa el siguiente comando:

```bash
flask run
```

La API estará disponible en `http://localhost:5000`.

## Endpoints

### 1. `GET /stocks`

Este endpoint devuelve todos los stocks disponibles en la base de datos.

- **Autenticación**: Necesitas estar autenticado con un token JWT válido.
- **Respuesta**: Devuelve una lista de objetos `stock` en formato JSON.

Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "cantidad": 100,
    "ubicacion": "Almacén A",
    "equipo_id": 1,
    "fecha_actualizacion": "2024-11-05T14:35:00",
    "equipo": {
      "id": 1,
      "nombre": "Equipo 1"
    }
  }
]
```

### 2. `POST /stocks`

Este endpoint crea un nuevo stock. Solo un administrador puede crear nuevos stocks.

- **Autenticación**: Necesitas estar autenticado con un token JWT válido y ser un administrador.
- **Cuerpo de la solicitud** (JSON):
  ```json
  {
    "cantidad": 50,
    "ubicacion": "Almacén B",
    "equipo_id": 2
  }
  ```
- **Respuesta**: Devuelve el stock recién creado.

Ejemplo de respuesta:
```json
{
  "id": 2,
  "cantidad": 50,
  "ubicacion": "Almacén B",
  "equipo_id": 2,
  "fecha_actualizacion": "2024-11-05T14:35:00"
}
```

### 3. `DELETE /stocks/<int:id>/delete`

Este endpoint elimina un stock por su `id`. Solo un administrador puede eliminar stocks.

- **Autenticación**: Necesitas estar autenticado con un token JWT válido y ser un administrador.
- **Parámetros de la URL**: `id` del stock a eliminar.
- **Respuesta**: Devuelve un mensaje de confirmación.

Ejemplo de respuesta:
```json
{
  "Mensaje": "Stock eliminado con éxito"
}
```

## Autenticación

La autenticación se maneja con JWT. Para acceder a los endpoints que requieren autenticación, debes enviar un token JWT en el encabezado de la solicitud.

Ejemplo de encabezado de autorización:

```
Authorization: Bearer <tu_token_jwt>
```

## Estructura del Proyecto

```plaintext
.
├── app.py                # Archivo principal de la aplicación Flask
├── models.py             # Definición de los modelos de base de datos
├── schemas.py            # Definición de los esquemas para la serialización
├── config.py             # Configuraciones de la aplicación
├── .env                  # Variables de entorno (base de datos, clave secreta)
├── requirements.txt      # Dependencias del proyecto
├── migrations/           # Directorio de migraciones de base de datos
├── README.md             # Documentación del proyecto
```

## Descripción de los Modelos

### Modelo `Stock`

El modelo `Stock` tiene los siguientes campos:

- `id`: Identificador único del stock (clave primaria).
- `cantidad`: La cantidad disponible del equipo en stock.
- `ubicacion`: La ubicación física del stock.
- `equipo_id`: Clave foránea que referencia al equipo al que pertenece el stock.
- `fecha_actualizacion`: Fecha y hora de la última actualización del stock.

### Modelo `Equipo`

El modelo `Equipo` tiene los detalles del equipo. La relación entre `Stock` y `Equipo` es de uno a muchos, es decir, un equipo puede tener múltiples stocks asociados.

## Contribuciones

Si deseas contribuir al proyecto, realiza un fork del repositorio, crea una nueva rama, realiza tus cambios y luego envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
```

Este archivo `README.md` contiene todos los detalles básicos sobre cómo configurar y usar la API, qué hace cada endpoint, y cómo manejar la autenticación. También incluye instrucciones sobre cómo instalar y ejecutar el proyecto, así como detalles sobre la estructura del código. Asegúrate de ajustar cualquier detalle específico (como las URL de la base de datos) según tu configuración.
