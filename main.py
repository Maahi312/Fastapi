from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Endpoint accessed successfully. Your Docker, Jenkins, and Azure repo setup is working fine"}