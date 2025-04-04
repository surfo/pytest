import pytest
import requests
from jsonschema import validate, ValidationError
import urllib3
from http import HTTPStatus
# Base URL de la API
BASE_URL = "https://walletchallenge-back.onrender.com" #"https://walletchallenge-back.onrender.com/" #

HEADERS = {"Content-Type": "application/json"}

# Esquema JSON para validar la respuesta del endpoint /wallet/sesion
# https://regex101.com/
# Las pruebas se rigen acorde al contrato
# https://walletchallenge-back.onrender.com/docs#/
SESION_SCHEMA = {
    "type": "object",
    "additionalItems": False,
    "properties": {
        "access_token": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9]{20,40}\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9_-]+$"
        },
        "token_type": 
            {"type": "string",
            "pattern":"^bearer$"},
        "access_token_expires": 
            {"type": "number",
            "pattern":" ^\\d+$"},
        "tarjetas": {
            "additionalItems": False,
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "descripcion": 
                        {"type": "string",
                        "pattern":"^[A-Z\\s]{1,40}$"},
                    "numero": 
                        {"type": "string",
                        "pattern":"^[0-9]{12,19}$"}
                },
                    "required": ["descripcion", "numero"]
            }
        }
    },
    "required": ["access_token", "token_type", "access_token_expires", "tarjetas"]
}

# Crear sesión
sesion = requests.session()

def test_sesion_200():
    """docstring en Python: Validar la respuesta correcta (200) con el esquema JSON."""
    # Desactivar advertencias de SSL
    urllib3.disable_warnings()
    url = f"{BASE_URL}/wallet/sesion"
    payload = {"username": "challenge", "password": "challenge"}
    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)

    assert response.status_code == 200, f"El código de estado no es 200. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"
    assert response.elapsed.total_seconds() <= 3.0, f"Timeout: test_sesion_200 demoro mas de 3 seg. Duracion: {response.elapsed.total_seconds()}"
    try:
        validate(instance=response.json(), schema=SESION_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Validación JSON fallida: {e}")
    # Si la autenticación es exitosa, agregar el token a los headers de la sesión

    if response.status_code == 200:
        sesion.headers.update(({'Authorization': 'Bearer ' +            response.json().get("access_token")}))

def test_sesion_500():
    urllib3.disable_warnings()
    """docstring en Python: Probar error interno del servidor (500)."""
    url = f"{BASE_URL}/wallet/sesion"
    payload = {"username": "500", "password": "challenge"}
    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)

    assert response.status_code == 500, f"El código de estado no es 500. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"


def test_sesion_401():
    urllib3.disable_warnings()
    """docstring en Python: Probar credenciales inválidas (401)."""
    url = f"{BASE_URL}/wallet/sesion"
    payload = {"username": "invalid_user", "password": "challenge"}
    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)

    assert response.status_code == 401, f"El código de estado no es 401. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"

    
def test_sesion_404():
    urllib3.disable_warnings()
    """docstring en Python: Probar 404 path not found (404)."""
    url = f"{BASE_URL}/wallet/sesion1"
    payload = {
                "username": "challengel", 
                "password": "challenge"
              }

    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)

    assert response.status_code == 404,f"El código de estado no es 404. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"
    
def test_sesion_400():
    urllib3.disable_warnings()
    """docstring en Python: Probar Bad Request (400)."""
    url = f"{BASE_URL}/wallet/sesion"
    payload = None    
    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)
    assert response.status_code == 400,f"El código de estado no es 400. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"
   
def test_sesion_422():
    urllib3.disable_warnings()
    """docstring en Python: Probar json invalido(422)."""
    url = f"{BASE_URL}/wallet/sesion"
    payload = "json invalido" 
    response = sesion.post(url, json=payload, headers=HEADERS, verify=False)
    assert response.status_code == 422, f"El código de estado no es 422. Error: {response.status_code}: {HTTPStatus(response.status_code).phrase}"
   