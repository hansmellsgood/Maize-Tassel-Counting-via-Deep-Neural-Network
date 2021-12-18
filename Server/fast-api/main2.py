from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image

# import tensorflow as tf
import torch
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

# MODEL = tf.keras.models.load_model("../saved_models/1")

# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

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

@app.get("/ping")
async def ping() -> dict:
    return {'data': tests}

@app.post("/ping")
async def add_tests(test: dict) -> dict:
    tests.append(test)
    return {
        "data": {"Tests added."}
    }

def read_file_as_image(data):
    image = Image.open(BytesIO(data))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    transform = transforms.Compose([
       transforms.Resize((32, 32)),
       transforms.ToTensor()
    ])
    img1 = transform(image).unsqueeze(0)

    # img_batch = np.expand_dims(image, 0)
    # predictions = MODEL.predict(img_batch)
    # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    # confidence = np.max(predictions[0])

    return {
        'image_size': image.size,
        "transform_size": img1.size()
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
