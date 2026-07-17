import time
import pytest
from conftest import load_json

def cumple_contrato(data: dict) -> bool:
    """Valida los tipos del contrato requeridos para el usuario."""
    required_keys = {
        "id": int,
        "name": str,
        "username": str,
        "email": str
    }
    for key, expected_type in required_keys.items():
        if key not in data:
            return False
        if not isinstance(data[key], expected_type):
            return False
    return True


# 1. test_listar_users: Status 200 y 10 usuarios
def test_listar_users(api):
    response = api.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 10


# 2. test_detalle_cumple_contrato: Status 200 y validación de contrato
def test_detalle_cumple_contrato(api):
    response = api.get("/users/1")
    assert response.status_code == 200
    user_detail = response.json()
    assert cumple_contrato(user_detail) is True


# 3. test_crear_user: Status 201, name generado con time.time_ns() y verificado en el eco
@pytest.mark.parametrize("payload", load_json("users_payloads.json"))
def test_crear_user(api, payload):
    # Generar un nombre único dinámico
    unique_name = f"RNR {time.time_ns()}"
    
    # Clonar payload base e inyectar el nombre dinámico
    user_data = payload.copy()
    user_data["name"] = unique_name
    
    response = api.post("/users", json=user_data)
    assert response.status_code == 201
    
    response_data = response.json()
    assert response_data["name"] == unique_name


# 4. test_actualizar_user: Status 200 y coincidencia del campo actualizado
def test_actualizar_user(api):
    updated_email = f"user1.{time.time_ns()}@testdomain.com"
    update_payload = {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": updated_email,
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874",
            "geo": { "lat": "-37.3159", "lng": "81.1496" }
        },
        "phone": "1-770-736-8031 x56442",
        "website": "hildegard.org",
        "company": {
            "name": "Romaguera-Crona",
            "catchPhrase": "Multi-layered client-server neural-net",
            "bs": "harness real-time e-markets"
        }
    }
    
    response = api.put("/users/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["email"] == updated_email


# 5. test_eliminar_user: Status 200 y cuerpo vacío {}
def test_eliminar_user(api):
    response = api.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {}