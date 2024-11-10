from fastapi import FastAPI, UploadFile
import hashlib
from .ai import get_marked_edf
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import random
from visual.visual import plot_channel

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./server/static"), name="static")

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    edfInput = file.file
    hash = hashlib.md5(file.filename.encode()+ str(random.randint(0, 100000)).encode()).hexdigest()
    tmp_filename = f"server/static/{hash}.edf"
    with open(tmp_filename, "wb") as f:
        f.write(edfInput.read())

    marked_edf_filename, data = get_marked_edf(tmp_filename, hash)


    frl_json = plot_channel(data, "FrL", 0)
    with open(f"server/static/{hash}_frl.json", "w") as f:
        f.write(frl_json)

    frr_json = plot_channel(data, "FrR", 1)
    with open(f"server/static/{hash}_frr.json", "w") as f:
        f.write(frr_json)
    
    ocr_json = plot_channel(data, "OcR", 2)
    with open(f"server/static/{hash}_ocr.json", "w") as f:
        f.write(ocr_json)

    resp = {
        "file": marked_edf_filename,
        "word": f"static/{hash}.docx",
        "frl": f"static/{hash}_frl.json",
        "frr": f"static/{hash}_frr.json",
        "ocr": f"static/{hash}_ocr.json"
    }

    return resp
