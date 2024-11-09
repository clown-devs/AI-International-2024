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


    graph_json = create_plot(data)
      # Сжимаем график в gzip
    with open("server/" + json_filename, "w") as f:
        f.write(graph_json)
    
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

    # Уменьшим размер данных для ускорения отрисовки
    FrL = FrL[:100000]
    FrR = FrR[:100000]
    OcR = OcR[:100000]
    classes = classes[:100000]

    # Частота дискретизации
    sampling_frequency = 400  # Гц

    # Время на оси X (по индексу данных)
    time = [i / sampling_frequency for i in range(len(FrL))]

    # Создаем фигуру
    fig = go.Figure()

    # Для каждого класса (0, 1, 2, 3) добавляем scatter trace для каждого канала
    colors = {0: "gray", 1: "green", 2: "red", 3: "orange"}
    for class_label in [0, 1, 2, 3]:
        # Для каждого канала
        class_indices = [i for i, c in enumerate(classes) if c == class_label]
        
        # FrL график
        fig.add_trace(go.Scatter(
            x=[time[i] for i in class_indices], 
            y=[FrL[i] for i in class_indices], 
            mode='markers', 
            name=f'FrL - Class {class_label}', 
            marker=dict(color=colors[class_label])
        ))

        # FrR график
        fig.add_trace(go.Scatter(
            x=[time[i] for i in class_indices], 
            y=[FrR[i] for i in class_indices], 
            mode='markers', 
            name=f'FrR - Class {class_label}', 
            marker=dict(color=colors[class_label])
        ))

        # OcR график
        fig.add_trace(go.Scatter(
            x=[time[i] for i in class_indices], 
            y=[OcR[i] for i in class_indices], 
            mode='markers', 
            name=f'OcR - Class {class_label}', 
            marker=dict(color=colors[class_label])
        ))

    # Настроим макет графика
    fig.update_layout(
        title="Signal Channels with Class Colors",
        xaxis_title="Time (s)",
        yaxis_title="Signal Amplitude",
        legend_title="Classes",
        showlegend=True,
    )
    
    # Возвращаем график в формате JSON
    return fig.to_json()