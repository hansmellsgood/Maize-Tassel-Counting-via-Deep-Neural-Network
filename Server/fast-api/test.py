import unittest
from main2 import *
from fastapi.testclient import TestClient
import os
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
sample_image1 = "test1.jpg"


class MyTestCase(unittest.TestCase):
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


    # Connection Testing
    def test_server_connection_pass(self):
        response = client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "Welcome to Maize Tassel Counting Default"})


    def test_server_connection_fail(self):
        response = client.get("/api/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"result": "Welcome to Maize Tassel Counting Default"})


    # Main Functions Testing
    def test_predict(self):
        with open(sample_image, 'rb') as f:
            byte_im = f.read()
            response = client.post(
                "/api/predict",
                files={"file": ("test.jpg", byte_im)}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["file_name"], sample_image)
        self.assertEqual(str(type(response.json()["image"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["density_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["yolov5_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["yolov5_count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["rcnn_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["rcnn_count"])), "<class 'int'>")

    def test_predict_multiple(self):
        files = [
            ('files', ('test.jpg', open(sample_image, 'rb'), 'image/jpeg')),
            ('files', ('test1.jpg', open(sample_image1, 'rb'), 'image/jpeg'))
        ]
        response = client.post(
            "/api/testArray",
            files=files
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0]["file_name"], "test.jpg")
        self.assertEqual(response.json()['data'][1]["file_name"], "test1.jpg")
        self.assertEqual(str(type(response.json()['data'][0]["image"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][1]["image"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][0]["density_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][1]["density_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][0]["count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()['data'][1]["count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()['data'][0]["yolov5_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][1]["yolov5_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][0]["yolov5_count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()['data'][1]["yolov5_count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()['data'][0]["rcnn_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][1]["rcnn_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()['data'][0]["rcnn_count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()['data'][1]["rcnn_count"])), "<class 'int'>")

    def test_Mobile(self):
        with open(sample_image, 'rb') as f:
            pp_uri = "test.jpg"
            pp_base64 = f.read()
            img = read_image(pp_base64)
            encoded_b64 = base64.b64encode(pp_base64)
            pp_filename = "test.jpg"
            pp_width = img.shape[0]
            pp_height = img.shape[1]
            pp_filesize = os.path.getsize('test.jpg')
            pp_type = sample_image[-4]
            item = Item(uri=pp_uri,type=pp_type,fileName=pp_filename,height=pp_height,
                 width=pp_width,fileSize=pp_filesize,base64=encoded_b64)
            response = client.post(
                "/api/pp",
                data=item.json()
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["file_name"], sample_image)
        self.assertEqual(str(type(response.json()["file_name"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["height"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["width"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["density_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["yolov5_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["yolov5_count"])), "<class 'int'>")
        self.assertEqual(str(type(response.json()["rcnn_img"])), "<class 'str'>")
        self.assertEqual(str(type(response.json()["rcnn_count"])), "<class 'int'>")


    # Model testing
    def test_density_model(self):
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
            output_save = output
            output = Normalizer.gpu_normalizer(output, img.size()[2], img.size()[3], INPUT_SIZE, OUTPUT_STRIDE)
            # postprocessing
            output = np.clip(output, 0, None)
            pd_count = output.sum()
            pd_count = math.floor(pd_count)
            density_img = density_map(output_save, img, img1)
        self.assertEqual(str(type(model)), "<class 'torch.nn.parallel.data_parallel.DataParallel'>")
        self.assertEqual(str(type(density_img)), "<class 'bytes'>")
        self.assertEqual(str(type(pd_count )), "<class 'int'>")

    def test_yolo_model(self):
        img = Image.open(sample_image)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
        model.conf = 0.3
        model.iou = 0.1
        output = model(img)
        pd_count = len(output.pred[0].numpy())
        output = output.render()
        buffered = BytesIO()
        img_base64 = Image.fromarray(output[0])
        img_base64.save(buffered, format="JPEG")
        yolov5_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        self.assertEqual(str(type(yolov5_img)), "<class 'str'>")
        self.assertEqual(str(type(pd_count)), "<class 'int'>")

    def test_fasterrcnn_model(self):
        img = cv2.imread(sample_image, cv2.IMREAD_COLOR)
        img2 = cv2.imread(sample_image, cv2.IMREAD_COLOR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB).astype(np.float32)
        img2 /= 255.
        img2 = img2.transpose((2, 0, 1))
        img2 = torch.from_numpy(img2)
        img2 = img2.unsqueeze(0)
        model = torch.load('faster_rcnn2.pt')
        model.eval()
        output = model(img2)
        nms_out = (torchvision.ops.nms(boxes=output[0]['boxes'],
                                       scores=output[0]['scores'], iou_threshold=0.1)).cpu().numpy()
        threshold = 0.3
        boxes = []
        scores = []
        for n in nms_out:
            if output[0]['scores'][n].cpu().detach().numpy() <= threshold:
                continue
            boxes.append(output[0]['boxes'][n].cpu().detach().numpy().astype(np.int32))
            scores.append(output[0]['scores'][n].cpu().detach().numpy())
        for box in boxes:
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 10)
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.imshow(img.astype(np.uint8))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes, format='jpg', bbox_inches="tight", pad_inches=0, dpi=300)
        my_stringIObytes.seek(0)
        rcnn_img = base64.b64encode(my_stringIObytes.read())
        pd_count = len(boxes)
        self.assertEqual(str(type(rcnn_img)), "<class 'bytes'>")
        self.assertEqual(str(type(pd_count)), "<class 'int'>")

if __name__ == '__main__':
    unittest.main()
