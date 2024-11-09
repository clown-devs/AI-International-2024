from fastapi import FastAPI, UploadFile
import hashlib
from .ai import get_marked_edf
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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
    hash = hashlib.md5(file.filename.encode()).hexdigest()
    tmp_filename = f"server/static/{hash}.edf"
    with open(tmp_filename, "wb") as f:
        f.write(edfInput.read())

    marked_edf_filename, data = get_marked_edf(tmp_filename)

    # т.к json очень большой то лучше отдавать его в виде ссылки на файл
    json_filename = f"static/{hash}.json"
    # data = {
    #     "FrL": data[:, 0].tolist(),
    #     "FrR": data[:, 1].tolist(),
    #     "OcR": data[:, 2].tolist(),
    #     "classes": data[:, 3].tolist()
    # }
    
    # постарался сжать данные
    # import numpy as np
    # data = {
    #     "FrL": np.round(data[:, 0], 6).tolist(),
    #     "FrR": np.round(data[:, 1], 6).tolist(),
    #     "OcR": np.round(data[:, 2], 6).tolist(),
    #     "classes": data[:, 3].tolist()
    # }

    data = {
         "FrL": data[:, 0].tolist(),
         "FrR": data[:, 1].tolist(),
         "OcR": data[:, 2].tolist(),
         "classes": list(map(int, data[:, 3]))
    }

    # import msgpack
    # packed = msgpack.packb(data)
    # pack_filename = f"static/{hash}.msgpack"
    # import gzip
    # with gzip.open("server/" + pack_filename + ".gz", "wb") as f:
    #     f.write(packed)

    # import json
    # with open("server/"+json_filename, "w") as f:
    #     f.write(json.dumps(data))

    import gzip

    graph_json = create_plot(data)
    with gzip.open("server/" + json_filename + ".gz", "wb") as f:
        f.write(graph_json.encode())
    
    resp = {
        "file": marked_edf_filename,
        "graph": json_filename
        #"json": json_filename,
        #"msgpack": pack_filename + ".gz"
    }

    return resp

import plotly.graph_objects as go
import plotly.express as px

def create_plot(data):
    # Преобразуем данные
    FrL = data["FrL"]
    FrR = data["FrR"]
    OcR = data["OcR"]
    classes = data["classes"]

    # Создаем фигуру
    fig = go.Figure()

    # Для каждого класса (0, 1, 2, 3) добавляем scatter trace
    colors = {0: "blue", 1: "green", 2: "red", 3: "orange"}
    for class_label in [0, 1, 2, 3]:
        class_indices = [i for i, c in enumerate(classes) if c == class_label]
        fig.add_trace(go.Scatter(x=[FrL[i] for i in class_indices],
                                 y=[FrR[i] for i in class_indices],
                                 mode='markers',
                                 name=f'Class {class_label}',
                                 marker=dict(color=colors[class_label])))

    # Настроим макет графика
    fig.update_layout(
        title="Signal Channels with Class Colors",
        xaxis_title="FrL",
        yaxis_title="FrR",
        legend_title="Classes",
        showlegend=True,
    )
    
    # Возвращаем график в формате JSON
    return fig.to_json()