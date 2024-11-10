import numpy as np
import plotly.graph_objects as go
import json
import plotly

def plot_channel(data_with_classes: np.ndarray, channel_name: str, channel_index: int, resample_factor: int = 100) -> str:
    channel_data = data_with_classes[:, channel_index]
    classes = data_with_classes[:, -1]
    time_axis = np.arange(len(channel_data)) / 400  
    
    if resample_factor > 1:
        channel_data = channel_data[:len(channel_data) // resample_factor * resample_factor]
        time_axis = time_axis[:len(time_axis) // resample_factor * resample_factor]
        classes = classes[:len(classes) // resample_factor * resample_factor]
        
        channel_data = channel_data.reshape(-1, resample_factor).mean(axis=1)
        time_axis = time_axis.reshape(-1, resample_factor).mean(axis=1)
        classes = classes.reshape(-1, resample_factor).max(axis=1) 

    fig = go.Figure()


    class_colors = {
        0: 'rgba(169, 169, 169, 1)',  # Нет класса
        1: 'rgba(255, 0, 0, 0.8)',  # SWD (красный)
        2: 'rgba(0, 255, 0, 0.8)',  # IS (зеленый)
        3: 'rgba(0, 0, 255, 0.8)'   # DS (синий)
    }

    
    fig.add_trace(go.Scatter(
        x=time_axis,
        y=channel_data,
        mode='lines',
        name=channel_name,
        line=dict(color=class_colors[0])
    ))

    

    class_labels = {
        0: 'Аномалия отсутствует',
        1: 'SWD',
        2: 'IS',
        3: 'DS'
    }

    class_exists = {
        0: False,
        1: False,
        2: False,
        3: False
    }

    for i in range(1, len(classes)):
        if classes[i] != classes[i-1]: 
            if classes[i-1] != 0:
                class_exists[classes[i]] = True
                fig.add_trace(go.Scatter(
                    x=[time_axis[i], time_axis[i]],
                    y=[min(channel_data), max(channel_data)],
                    mode='lines',
                    line=dict(color=class_colors[classes[i-1]], dash='dot'),
                    showlegend=True,
                    legendgroup=class_labels[classes[i-1]],
                    name=class_labels[classes[i-1] ]
                )
                )

            if classes[i] != 0:
                class_exists[classes[i]] = True
                fig.add_trace(go.Scatter(
                    x=[time_axis[i], time_axis[i]],
                    y=[min(channel_data), max(channel_data)],
                    mode='lines',
                    line=dict(color=class_colors[classes[i]], dash='dot'),
                    showlegend=True,
                    name=class_labels[classes[i]],
                    legendgroup=class_labels[classes[i]]
                ))
                


    for class_type in class_labels:
        if class_exists[class_type]:
            fig.add_trace(go.Scatter(
                x=[None], y=[None], 
                mode='markers',
                marker=dict(color=class_colors[class_type], size=10),
                name=class_labels[class_type],
                showlegend=True,
                legendgroup=class_labels[classes[i]]
            ))

    # Настройки осей и заголовок
    fig.update_layout(
        title=f"График канала: {channel_name}",
        xaxis_title="Время (секунды)",
        yaxis_title="Амплитуда",
        legend_title="Тип аномалии"
    )

    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json


def simple_plot_channel(data_with_classes: np.ndarray, channel_name: str, channel_index: int, resample_factor: int = 4) -> str:
    channel_data = data_with_classes[:, channel_index]
    classes = data_with_classes[:, -1]
    time_axis = np.arange(len(channel_data)) / 400  
    

    if resample_factor > 1:
        channel_data = channel_data[:len(channel_data) // resample_factor * resample_factor] 
        time_axis = time_axis[:len(time_axis) // resample_factor * resample_factor]
        classes = classes[:len(classes) // resample_factor * resample_factor]
        
        channel_data = channel_data.reshape(-1, resample_factor).mean(axis=1)
        time_axis = time_axis.reshape(-1, resample_factor).mean(axis=1)
        classes = classes.reshape(-1, resample_factor).max(axis=1)
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_axis,
        y=channel_data,
        mode='lines',
        name=channel_name
    ))


    anomaly_color = 'rgba(255, 0, 0, 0.2)'  
    anomaly_indices = np.where(classes != 0)[0]
    
    if len(anomaly_indices) > 0:
        fig.add_trace(go.Scatter(
            x=time_axis[anomaly_indices],
            y=channel_data[anomaly_indices],
            mode='lines',
            line=dict(color=anomaly_color),
            name='Anomalies',
            showlegend=True
        ))

    
    fig.update_layout(
        title=f"График канала: {channel_name}",
        xaxis_title="Время (секунды)",
        yaxis_title="Амплитуда",
        legend_title="Тип аномалии"
    )

    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json