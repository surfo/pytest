# Automatización de Pruebas con Pytest

Este proyecto utiliza **Pytest** para la automatización de pruebas en APIs. A continuación, se describen los pasos para la ejecución de pruebas, configuración del entorno y generación de reportes.

## 📌 Requisitos Previos

Instalar dependencias:

- Python 3.9 o superior
- `pip` actualizado
- Dependencias definidas en `requirements.txt`
     

## 📂 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone git@github.com:surfo/pytest.git
   ```
2. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # En Windows
   ```
Activarlo abriendo el activate por consola 

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠 Validación de Esquemas con Pytest

### 📌 Importancia de validar esquemas
La validación de esquemas en pruebas de API es fundamental para garantizar que las respuestas de los servicios cumplen con el contrato definido. Esto permite:
- Detectar cambios inesperados en las respuestas de la API.
- Asegurar la consistencia de los datos entre servicios.
- Reducir errores en integraciones con otros sistemas.

### 📄 Ejemplo de validación con `jsonschema`
Para validar la estructura de una respuesta JSON, se puede utilizar la librería `jsonschema` en conjunto con Pytest:

```python
from jsonschema import validate, ValidationError
import pytest

# Definición del esquema esperado
SESION_SCHEMA = {
    "type": "object",
    "additionalItems": False,
    "properties": {
        "access_token": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9]{20,40}\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9_-]+$"
        },
        "token_type": {
            "type": "string",
            "pattern": "^bearer$"
        },
        "access_token_expires": {
            "type": "number"
        },
        "tarjetas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "descripcion": {
                        "type": "string",
                        "pattern": "^[A-Z\\s]{1,40}$"
                    },
                    "numero": {
                        "type": "string",
                        "pattern": "^[0-9]{12,19}$"
                    }
                },
                "required": ["descripcion", "numero"]
            }
        }
    },
    "required": ["access_token", "token_type", "access_token_expires", "tarjetas"]
}

def test_validar_esquema(response_json):
    """ Verifica que la respuesta cumple con el esquema definido """
    try:
        validate(instance=response_json, schema=SESION_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Validación de esquema fallida: {e}")
```

- type:

Define el tipo de datos esperado. Por ejemplo, "type": "object" indica que la respuesta debe ser un objeto JSON.

Para cada campo dentro del objeto, se especifica si es un string, number, array, etc.

- additionalItems:

Se usa en arrays para indicar si se permiten elementos adicionales que no estén definidos en el esquema. En este caso, "additionalItems": False significa que no se permiten elementos extra fuera de los definidos.

- properties:

Especifica los atributos que debe tener el objeto y sus validaciones. Cada propiedad incluye su propio tipo y reglas.

- pattern:

Usa expresiones regulares para validar el formato de los datos.

Ejemplo: "pattern": "^[a-zA-Z0-9]{20,40}\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9_-]+$"

Valida que access_token tenga el formato de un JWT (JSON Web Token).

- required:

Lista de atributos obligatorios que deben estar presentes en la respuesta de la API.

Si falta alguno, la validación fallará.

## Distintos test 

## 200 OK (Solicitud Exitosa)

## 500 Internal Server Error (Error Interno del Servidor)

## 401 Unauthorized (No Autorizado)

## 404 Not Found (No Encontrado)

## 400 Bad Request (Solicitud Incorrecta)

## 422 Unprocessable Entity (Entidad No Procesable)




## 🚀 Ejecución de Pruebas

### Ejecutar todas las pruebas:
```bash
pytest test_login.py
```

### Ejecutar pruebas específicas por nombre:
```bash
pytest -k "test_nombre_prueba" 
```

### Ejecutar pruebas de un módulo específico:
```bash
pytest tests/unit/test_modulo.py 
```

### Ejecutar pruebas con diferentes niveles de detalle:
- **Modo detallado:**
  ```bash
  pytest -v
  ```
- **Mostrar solo fallos:**
  ```bash
  pytest -q --tb=short
  ```
- **Ejecutar pruebas fallidas nuevamente:**
  ```bash
  pytest --lf
  ```




## ⚙️ Configuración en GitLab CI/CD

El siguiente `gitlab-ci.yml` define un job para ejecutar las pruebas automatizadas:
```yaml
test_api:
  image: $python:3.9_xx
  variables:    
  before_script:
    - python3.9 -m venv venv  # Crear el entorno virtual
    - ls -la
    - ls -la venv
    - source venv/bin/activate
    - pip install -r requirements.txt --timeout 90
  stage: test  # Este job pertenece al stage 'test'
  script:
    -       
      # Ejecuta tests dependiendo del nombre del proyecto
      echo "PROJECT_NAME: $PROJECT_NAME"

      if [ "$PROJECT_NAME" == "Nombre_proyecto" ]; then
        echo "Ejecutando tests"
        pytest -k "test_session_200" --alluredir=allure-results
      fi
      
  artifacts:
    paths:
      - requirements.txt
      - allure-results  # Guardar los resultados de Allure como artefacto
    expire_in: 1 day
  tags:
    - qa
```

## ❗ Consideraciones Finales
- Todas las pruebas tiene que ser independientes y no depender de un orden de ejecución.
- Mantener las pruebas organizadas en carpetas (`unit`, `integration`).

