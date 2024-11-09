import numpy as np
import mne
from typing import Tuple

# parse_file принимает на вход путь к edf файлу и возвращает:
# - data_with_classes: матрица(np.ndarray) в которой хранятся 3 сигнала (FrL, FrR, OcR) + класс.
# - swd_annotation   : массив кортежей (начало, конец) эпи-разрядов (swd)
# - is_annotation    : массив кортежей (начало, конец) промежуточной фазы сна (is)
# - ds_annotation    : массив кортежей (начало, конец) глубокой фазы сна (ds)
def parse_file(file_path: str) -> Tuple[np.ndarray, list, list, list]:
    edf = mne.io.read_raw_edf(file_path)

    # Предполагаем, что все сигналы хахатона записаны с частотой 400Гц
    sampling_frequency = edf.info['sfreq']
    if sampling_frequency != 400:
        raise ValueError('Sampling frequency is not 400Hz')
    
    data = edf.get_data().T

    # Для каждого сигнала добавляем класс
    # Класс 0 - нет класса
    # Класс 1 - swd
    # Класс 2 - is
    # Класс 3 - ds
    classes = np.zeros((data.shape[0],), dtype=int)

    # Аннотации - это метки, которые ставятся на временные отрезки сигнала
    # У нас есть: 
    # - swd1, swd2 - начало и конец эпи-разрядов
    # - is1, is2 - начало и конец промежуточной фазы сна
    # - ds1, ds2 - начало и конец глубокой фазы сна
    # Они идут по порядку, то есть swd1 - начало значит сразу после него будет swd2 - конец

    annotations = edf.annotations
    swd_annotation, is_annotation, ds_annotation = [], [], []
    
    # Обрабатываем аннотации и устанавливаем классы точкам
    # Не уверен что классы у точек определяются правильно но пока так
    i = 0
    while i < len(annotations):
        onset = int(annotations[i]['onset'] * sampling_frequency)
        description = annotations[i]['description']

        if description == 'swd1':
            offset = int(annotations[i + 1]['onset'] * sampling_frequency)
            swd_annotation.append((onset, offset))
            classes[onset:offset] = 1
            i += 2 
        elif description == 'is1':
            offset = int(annotations[i + 1]['onset'] * sampling_frequency)
            is_annotation.append((onset, offset))
            classes[onset:offset] = 2
            i += 2
        elif description == 'ds1':
            offset = int(annotations[i + 1]['onset'] * sampling_frequency)
            ds_annotation.append((onset, offset))
            classes[onset:offset] = 3
            i += 2
        else:
            i += 1  
    # надо чтобы классы были int
    classes = classes.astype(int)
    data_with_classes = np.column_stack((data, classes))
    

    return data_with_classes, swd_annotation, is_annotation, ds_annotation


# Сохраняем 3 сигнала (FrL, FrR, OcR) вместе с классами в csv файл
def save_to_csv(data: np.ndarray, filename: str) -> None:
    header = 'FrL,FrR,OcR,Class'
    np.savetxt(filename, data, delimiter=',', header=header, comments='')



