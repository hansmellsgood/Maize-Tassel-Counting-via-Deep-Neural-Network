# FastAPI Modules
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from typing import List

# Stats Modules
import numpy as np
import math

# Images Modules
import io
from io import BytesIO
from PIL import Image
import cv2
import base64
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Torch Modules
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tests = [
    {
        "id": "1",
        "citem": "Read a book."
    },
    {
        "id": "2",
        "citem": "Cycle around town."
    }
]

single = [
    {
        "id": 1,
        "file": "test.jpeg",
        "file_name": "test.jpeg",
        "count": 1,
        # "density_img":"test.jpeg"
    }]

multiple = [
    {
        "id": "1",
        "file": "1",
        "file_name": "test.jpeg",
        "count": "3",
        # "density_img":"test.jpeg"
    },
    {
        "id": "2",
        "file": "1",
        "file_name": "test.jpeg",
        "count": "3",
        # "density_img": "test.jpeg"
    }
]

# Constants
IMG_SCALE = 1. / 255
IMG_MEAN = [.3405, .4747, .2418]
IMG_STD = [1, 1, 1]
INPUT_SIZE = 64
OUTPUT_STRIDE = 8





@app.get("/ping")
async def ping() -> dict:
    return {'data1': tests}


@app.post("/ping")
async def add_tests(test: dict) -> dict:
    tests.append(test)
    return {
        "data1": {"Tests added."}
    }


@app.get("/predict")
async def get_image() -> dict:
    return {'data1': single}


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = await file.read()
    data = base64.b64encode(image)

    # preprocessing
    test_image = read_image(image)
    image = read_image(image)
    image = resize_image(image)
    image = normalize_image(image)
    image = tensor_image(image)
    image = zero_padding_image(image)

    # load model
    model = torch.load('whole_model.pt')
    model.eval()
    with torch.no_grad():
        output = model(image, is_normalize=False)
        output_save = output
        output = Normalizer.gpu_normalizer(output, image.size()[2], image.size()[3], INPUT_SIZE, OUTPUT_STRIDE)
        # postprocessing
        output = np.clip(output, 0, None)
        pdcount = output.sum()
        pdcount = math.floor(pdcount)
        density_image = density_map(output_save, image, test_image)

    
    return {
        'file_name': file.filename,
        'encode': data,
        'encode1': density_image,
        'encode2': '',
        'count': pdcount
    }


@app.post("/testArray")
async def predict(
        files: List[UploadFile] = File(...)
):
    multipleTest = [{
        "file_name": None,
        "image": None,
        "count": 0,
        "density_image":None
    }]
    for i, file in enumerate(files):
        info = {}
        image = await file.read()
        data = base64.b64encode(image)
        # preprocessing
        test_image = read_image(image)
        image = read_image(image)
        image = resize_image(image)
        image = normalize_image(image)
        image = tensor_image(image)
        image = zero_padding_image(image)

        # load model
        model = torch.load('whole_model.pt')
        model.eval()
        with torch.no_grad():
            output = model(image, is_normalize=False)
            output_save = output
            output = Normalizer.gpu_normalizer(output, image.size()[2], image.size()[3], INPUT_SIZE, OUTPUT_STRIDE)
            # postprocessing
            output = np.clip(output, 0, None)
            pdcount = output.sum()
            pdcount = math.floor(pdcount)
            density_image = density_map(output_save, image, test_image)
            if i == 0:
                multipleTest[0]['file_name'] = file.filename
                multipleTest[0]['image'] = data
                multipleTest[0]['count'] = pdcount
                multipleTest[0]['density_image'] = density_image
            else:
                info['file_name'] = file.filename
                info['image'] = data
                info['count'] = pdcount
                info['density_image'] = density_image
                multipleTest.append(info)

    return {
        'data': multipleTest
    }


def read_image(image):
    img_arr = np.array(Image.open(BytesIO(image)))
    if len(img_arr.shape) == 2:  # grayscale
        img_arr = np.tile(img_arr, [3, 1, 1]).transpose(1, 2, 0)
    return img_arr


def resize_image(image):
    h, w = image.shape[:2]
    nh = int(np.ceil(h * 0.125))
    nw = int(np.ceil(w * 0.125))
    image = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_CUBIC)
    return image


def normalize_image(image):
    # Normalize
    image = image.astype('float32')
    # pixel normalization
    image = (IMG_SCALE * image - IMG_MEAN) / IMG_STD
    image = image.astype('float32')
    return image


def tensor_image(image):
    # To Tensor
    image = image.transpose((2, 0, 1))
    image = torch.from_numpy(image)
    return image


def zero_padding_image(image):
    psize = 32
    h, w = image.size()[-2:]
    ph, pw = (psize - h % psize), (psize - w % psize)

    (pl, pr) = (pw // 2, pw - pw // 2) if pw != psize else (0, 0)
    (pt, pb) = (ph // 2, ph - ph // 2) if ph != psize else (0, 0)
    if (ph != psize) or (pw != psize):
        tmp_pad = [pl, pr, pt, pb]
        image = F.pad(image, tmp_pad)
    image = image.unsqueeze(0)
    return image


def recover_countmap(pred, image, patch_sz, stride):
    pred = pred.reshape(-1)
    imH, imW = image.shape[2:4]
    cntMap = np.zeros((imH, imW), dtype=float)
    norMap = np.zeros((imH, imW), dtype=float)

    H = np.arange(0, imH - patch_sz + 1, stride)
    W = np.arange(0, imW - patch_sz + 1, stride)
    cnt = 0
    for h in H:
        for w in W:
            pixel_cnt = pred[cnt] / patch_sz / patch_sz
            cntMap[h:h + patch_sz, w:w + patch_sz] += pixel_cnt
            norMap[h:h + patch_sz, w:w + patch_sz] += np.ones((patch_sz, patch_sz))
            cnt += 1
    return cntMap / (norMap + 1e-12)


def density_map(output_save, image, test_image):
    # density map
    cmap = plt.cm.get_cmap('jet')
    output_save = np.clip(output_save.squeeze().cpu().numpy(), 0, None)
    output_save = recover_countmap(output_save, image, INPUT_SIZE, OUTPUT_STRIDE)
    output_save = output_save / (output_save.max() + 1e-12)
    output_save = cmap(output_save) * 255.
    # image composition
    nh, nw = output_save.shape[:2]
    test_image = cv2.resize(test_image, (nw, nh), interpolation=cv2.INTER_CUBIC)
    output_save = 0.5 * test_image + 0.5 * output_save[:, :, 0:3]

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.imshow(output_save.astype(np.uint8))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg', bbox_inches='tight', dpi=300)
    my_stringIObytes.seek(0)
    density_map = base64.b64encode(my_stringIObytes.read())
    return density_map

class Normalizer:
    @staticmethod
    def gpu_normalizer(x, imh, imw, insz, os):
        _, _, h, w = x.size()
        # accm = torch.cuda.FloatTensor(1, insz*insz, h*w).fill_(1)
        accm = torch.FloatTensor(1, insz * insz, h * w).fill_(1)
        accm = F.fold(accm, (imh, imw), kernel_size=insz, stride=os)
        accm = 1 / accm
        accm /= insz ** 2
        accm = F.unfold(accm, kernel_size=insz, stride=os).sum(1).view(1, 1, h, w)
        x *= accm
        return x.squeeze().cpu().detach().numpy()


class Encoder(nn.Module):
    def __init__(self, arc='tasselnetv2'):
        super(Encoder, self).__init__()
        if arc == 'tasselnetv2':
            self.encoder = nn.Sequential(
                nn.Conv2d(3, 16, 3, padding=1, bias=False),
                nn.BatchNorm2d(16),
                nn.ReLU(inplace=True),
                nn.MaxPool2d((2, 2), stride=2),
                nn.Conv2d(16, 32, 3, padding=1, bias=False),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
                nn.MaxPool2d((2, 2), stride=2),
                nn.Conv2d(32, 64, 3, padding=1, bias=False),
                nn.BatchNorm2d(64),
                nn.ReLU(inplace=True),
                nn.MaxPool2d((2, 2), stride=2),
                nn.Conv2d(64, 128, 3, padding=1, bias=False),
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
                nn.Conv2d(128, 128, 3, padding=1, bias=False),
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
            )
        else:
            raise NotImplementedError

    def forward(self, x):
        x = self.encoder(x)
        return x


class Counter(nn.Module):
    def __init__(self, arc='tasselnetv2', input_size=64, output_stride=8):
        super(Counter, self).__init__()
        k = int(input_size / 8)
        avg_pool_stride = int(output_stride / 8)

        if arc == 'tasselnetv2':
            self.counter = nn.Sequential(
                nn.Conv2d(128, 128, (k, k), bias=False),
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
                nn.Conv2d(128, 128, 1, bias=False),
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
                nn.Conv2d(128, 1, 1)
            )
        else:
            raise NotImplementedError

    def forward(self, x):
        x = self.counter(x)
        return x


class CountingModels(nn.Module):
    def __init__(self, arc='tasselnetv2', input_size=64, output_stride=8):
        super(CountingModels, self).__init__()
        self.input_size = input_size
        self.output_stride = output_stride

        self.encoder = Encoder(arc)
        self.counter = Counter(arc, input_size, output_stride)
        if arc == 'tasselnetv2':
            # changed
            self.normalizer = Normalizer.gpu_normalizer

        self.weight_init()

    def forward(self, x, is_normalize=True):
        imh, imw = x.size()[2:]
        x = self.encoder(x)
        x = self.counter(x)
        if is_normalize:
            x = self.normalizer(x, imh, imw, self.input_size, self.output_stride)
        return x

    def weight_init(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=0.01)
                # nn.init.kaiming_uniform_(
                #         m.weight,
                #         mode='fan_in',
                #         nonlinearity='relu'
                #         )
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
