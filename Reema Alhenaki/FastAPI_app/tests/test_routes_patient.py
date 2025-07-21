from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_patient_route():
    response = client.post("/patients/", json={
        "RegistrationDate": "2024-01-01T00:00:00",  
        "FirstName": "Reema",
        "MiddleName": "User",
        "LastName": "Example",
        "Gender": 1,
        "DateofBirth": "1995-03-10T00:00:00",
        "NationalityID": "SAU",
        "FirstVisit": "2024-01-01T00:00:00",
        "LastVisit": "2024-01-01T00:00:00",
        "NoOfVisit": 1,
        "MobileNumber": 111222333  #int not string
    })
    assert response.status_code == 200

def test_invalid_mobile_patient_route():
    response = client.post("/patients/", json={
        "RegistrationDate": "2024-01-01T00:00:00",
        "FirstName": "Reema",
        "MiddleName": "User", 
        "LastName": "Example",
        "Gender": 1, 
        "DateofBirth": "1995-03-10T00:00:00",
        "NationalityID": "SAU", 
        "FirstVisit": "2024-01-01T00:00:00",
        "LastVisit": "2024-01-01T00:00:00", 
        "NoOfVisit": 1,
        "MobileNumber": "011122233"
    })
    assert response.status_code == 422
