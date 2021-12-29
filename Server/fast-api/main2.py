# FastAPI Modules
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Stats Modules
import numpy as np
import math

# Images Modules
from io import BytesIO
from PIL import Image
import cv2
import base64

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


def read_image(x):
    img_arr = np.array(Image.open(BytesIO(x)))
    if len(img_arr.shape) == 2:  # grayscale
        img_arr = np.tile(img_arr, [3, 1, 1]).transpose(1, 2, 0)
    return img_arr


@app.get("/predict")
async def get_image() -> dict:
    return {'data1': single}


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = await file.read()
    data = base64.b64encode(image)

    # resize image
    image = read_image(image)
    h, w = image.shape[:2]
    nh = int(np.ceil(h * 0.125))
    nw = int(np.ceil(w * 0.125))
    image = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_CUBIC)

    # Normalize
    image = image.astype('float32')
    # pixel normalization
    image = (IMG_SCALE * image - IMG_MEAN) / IMG_STD
    image = image.astype('float32')

    # To Tensor
    image = image.transpose((2, 0, 1))
    image = torch.from_numpy(image)

    # Zero Padding
    psize = 32
    h, w = image.size()[-2:]
    ph, pw = (psize - h % psize), (psize - w % psize)
    print(ph, pw)

    (pl, pr) = (pw // 2, pw - pw // 2) if pw != psize else (0, 0)
    (pt, pb) = (ph // 2, ph - ph // 2) if ph != psize else (0, 0)
    if (ph != psize) or (pw != psize):
        tmp_pad = [pl, pr, pt, pb]
        print(tmp_pad)
        image = F.pad(image, tmp_pad)
    image = image.unsqueeze(0)

    # load model
    model = torch.load('whole_model.pt')
    model.eval()
    output = model(image, is_normalize=False)
    output = Normalizer.gpu_normalizer(output, image.size()[2], image.size()[3], INPUT_SIZE, OUTPUT_STRIDE)
    # postprocessing
    output = np.clip(output, 0, None)
    pdcount = output.sum()
    pdcount = math.floor(pdcount)

    return {
        'file_name': file.filename,
        'encode': data,
        'encode1': '',
        'encode2': '',
        'count': pdcount
    }


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
