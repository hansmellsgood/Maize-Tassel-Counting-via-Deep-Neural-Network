import unittest
from main2 import *
from fastapi.testclient import TestClient
#import asyncio
#import aiounittest
#from httpx import AsyncClient
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

client = TestClient(app)
#https://fastapi.tiangolo.com/tutorial/testing/
sample_image = "test.jpg"

class MyTestCase(unittest.TestCase):
    def test_main(self):
        response = client.get("/api/home")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "Welcome to Maize Tassel Counting Default"})

    def test_hello(self):
        response = client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "Welcome to Maize Tassel Counting Default"})

    def test_predict(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
            response = client.post(
                "/api/predict",
                files={"file": ("test.jpg", byte_im)}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["file_name"], "test.jpg")
        # 'file_name': file.filename,
        # 'image': data,
        # 'density_img': density_img,
        # 'count': pdcount,
        # 'yolov5_count': yolov5_count,
        # 'yolov5_img': yolov5_img,
        # 'rcnn_img': rcnn_img,
        # 'rcnn_count': rcnn_count

    # Utility Function testing
    def test_read_image(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        self.assertEqual(str(type(img)), "<class 'numpy.ndarray'>")
        self.assertEqual(len(img.shape), 3)

    def test_resize_image(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        img1 = resize_image(img)
        self.assertEqual(str(type(img)), "<class 'numpy.ndarray'>")
        self.assertEqual(len(img.shape), 3)
        self.assertTrue(img.shape[0] > img1.shape[0])
        self.assertTrue(img.shape[1] > img1.shape[1])

    def test_normalize_image(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        img = resize_image(img)
        img1 = normalize_image(img)
        self.assertEqual(str(type(img)), "<class 'numpy.ndarray'>")
        self.assertEqual(len(img.shape), 3)
        self.assertEqual(str(type(img1[0][0][0])), "<class 'numpy.float32'>")

    def test_tensor_image(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        img = resize_image(img)
        img = normalize_image(img)
        img1 = tensor_image(img)
        self.assertEqual(str(type(img1)), "<class 'torch.Tensor'>")

    def test_zero_padding_image(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        img = resize_image(img)
        img = normalize_image(img)
        img = tensor_image(img)
        img1 = zero_padding_image(img)
        self.assertEqual(str(type(img1)), "<class 'torch.Tensor'>")
        self.assertEqual(len(img1.size()), 4)

    def test_density_map(self):
        with open('test.jpg', 'rb') as f:
            byte_im = f.read()
        img = read_image(byte_im)
        img1 = read_image(byte_im)
        img = resize_image(img)
        img = normalize_image(img)
        img = tensor_image(img)
        img = zero_padding_image(img)
        model = CountingModels(arc='tasselnetv2', input_size=64, output_stride=8)
        model = nn.DataParallel(model)
        model.load_state_dict(torch.load('density_model.pt'))
        model = model.eval()
        with torch.no_grad():
            output = model(img, is_normalize=False)
            density_img = density_map(output, img, img1)
        self.assertEqual(str(type(density_img)), "<class 'bytes'>")


    # # Connection Testing
    # def test_server_connection(self):
    #
    #
    # def test_client_connection(self):
    #
    #
    # # Main Functions Testing
    # def test_predict(self):
    #
    #
    # # Model testing
    # def test_density_model(self):
    #
    #
    # def test_yolo_model(self):
    #     sample_image = "test.jpg"
    #     yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
    #     yolo_output = yolo_model(sample_image)
    #
    #
    # def test_fasterrcnn_model(self):


if __name__ == '__main__':
    unittest.main()
