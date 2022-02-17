import pytest
from main2 import *
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# def test_connection():
#     client = app.test_client()
#     url = '/dogs.html'
#     response = client.get(url)
#     assert response.status_code == 200
#     assert b"Small Breeds" in response.data
#     assert b"Large Breeds" in response.data
#     assert b"HDB Approved" in response.data

# def test_yolo_model():
#     sample_image = "test.jpg"
#     yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
#     yolo_output = yolo_model(image1)
#     url = '/dogs.html'
#     response = client.get(url)
#     assert response.status_code == 200
#     assert b"Small Breeds" in response.data
