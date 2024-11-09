from fastapi import FastAPI, UploadFile
import hashlib
from .ai import get_marked_edf
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="./server/static"), name="static")

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    edfInput = file.file
    hash = hashlib.md5(file.filename.encode()).hexdigest()
    tmp_filename = f"server/static/{hash}.edf"
    with open(tmp_filename, "wb") as f:
        f.write(edfInput.read())

    marked_edf_filename, data = get_marked_edf(tmp_filename)
    resp = {
        "file": marked_edf_filename,
        "data": {
            "FrL": data[:, 0].tolist(),
            "FrR": data[:, 1].tolist(),
            "OcR": data[:, 2].tolist(),
            "classes": data[:, 3].tolist()
        }
    }

    return resp
