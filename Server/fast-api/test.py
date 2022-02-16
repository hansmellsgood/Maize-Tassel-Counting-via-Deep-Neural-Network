import unittest

import pytest
from main2 import *
from fastapi.testclient import TestClient
# .assertEqual(a, b)
# .assertTrue(x)
# .assertFalse(x)
# .assertIsNone(x)
# .assertIs(a, b)
# .assertIsNot(a, b)
# .assertIn(a, b)
# .assertNotIn(a, b)
# .assertIsInstance(a, b)
# .assertNotIsInstance(a,b)

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)
#https://fastapi.tiangolo.com/tutorial/testing/
sample_image = "test.jpg"

class MyTestCase(unittest.TestCase):
    def test_predict(self):
        response = client.post(
            "/predict",
            sample_image)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(), {"msg": "Hello World"})

    # Utility Function testing
    def test_read_image(self):
        self.assertEqual(True, 1)

    def test_resize_image(self):
        self.assertEqual(True, True)

    def test_normalize_image(self):
        self.assertEqual(True, False)

    def test_tensor_image(self):
        self.assertEqual(True, False)

    def test_zero_padding_image(self):
        self.assertEqual(True, False)

    def test_density_map(self):
        self.assertEqual(True, False)

    # Connection Testing
    def test_server_connection(self):
        self.assertEqual(True, False)

    def test_client_connection(self):
        self.assertEqual(True, False)

    # Main Functions Testing
    def test_predict(self):
        self.assertEqual(True, False)

    # Model testing
    def test_density_model(self):
        self.assertEqual(True, 1)

    def test_yolo_model(self):
        sample_image = "test.jpg"
        yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
        yolo_output = yolo_model(sample_image)


        self.assertEqual(True, 1)

    def test_fasterrcnn_model(self):
        self.assertEqual(True, 1)

if __name__ == '__main__':
    unittest.main()
