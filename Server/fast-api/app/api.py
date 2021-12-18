from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

tests = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
]

@app.get("/test", tags=["tests"])
async def get_tests() -> dict:
    return { "data": tests }


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Testing"}

@app.post("/test", tags=["tests"])
async def add_test(test: dict) -> dict:
    tests.append(test)
    return {
        "data": {"Todo added."}
    }
