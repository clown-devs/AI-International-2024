import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import parse_file, save_to_edf
from .word import save_analytics_to_word
def get_marked_edf(unmarked_filename, hash):
    #data, swd, is_, ds = parse_file(unmarked_filename) 

    model = load_model("clown-net-new-finak-one.keras")    
    data, x_data = prepare_data(unmarked_filename, k=1)
    data = data[0]
    data = data[:8640000]
    classes = predict_model(model, x_data)
    data[:, -1] = classes

    marked_filename = f"static/{hash}_marked.edf"
    analytics = save_to_edf(data, "server/"+marked_filename)
    save_analytics_to_word(analytics, f"server/static/{hash}.docx")

    return marked_filename, data
    

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_model(path_for_model):
    from tensorflow.keras.models import load_model
    return load_model(path_for_model)

def prepare_data(path_for_edf, k=3):
    data_test = parse_file(path_for_edf)
    data_df = pd.DataFrame(data_test[0])[[0, 1, 2]]
    data_df.columns = ['1', '2', '3']
    standard_scaler = StandardScaler()
    if k == 3:
        X_data = standard_scaler.fit_transform(np.array(data_df[['1', '2', '3']]))
    else:
        X_data = standard_scaler.fit_transform(np.array(data_df['1']).reshape(-1, 1))
    X_data_total = X_data  
    segment_size = 12000
    num_segments = len(X_data_total) // segment_size
    X_data_total = X_data_total[:num_segments * segment_size].reshape(-1, segment_size, k)
    return data_test, X_data_total

def predict_model(model, X_data):
    pred = model.predict(X_data)
    return np.argmax(pred, axis=2).flatten()