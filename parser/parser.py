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
    
    data_with_classes = np.column_stack((data, classes))
    

    return data_with_classes, swd_annotation, is_annotation, ds_annotation


class Analytics:
    def __init__(self, sampling_frequency: int):
        self.sampling_frequency = sampling_frequency
        self.anomaly_count = 0
        self.total_duration = 0.0
        self.total_time = 0.0
        self.average_duration = 0.0
        self.average_interval = 0.0
        self.time_with_anomalies = 0.0
        self.durations = []
        self.intervals = []
        self.anomalies_by_type = {
            1: [],  # SWD
            2: [],  # IS
            3: []   # DS
        }
        # пиковая амплитуда сигнала в рамках аномалии
        self.peak_amplitudes = {
            1: [],  
            2: [], 
            3: []
        }

    def calculate_average_duration(self):
        if self.anomaly_count > 0:
            self.average_duration = self.total_duration / self.anomaly_count
    
    def calculate_percentage_with_anomalies(self):
        if self.total_time > 0:
            self.time_with_anomalies = (self.total_duration / self.total_time) * 100
    
    def calculate_average_interval(self):
        if len(self.intervals) > 0:
            self.average_interval = sum(self.intervals) / len(self.intervals)


# save_to_edf принимает на вход матрицу сигналов и классов и путь к файлу, в который нужно сохранить данные
def save_to_edf(data_with_classes: np.ndarray, output_file: str) -> Analytics:
    signals = data_with_classes[:, :3].T  
    classes = data_with_classes[:, 3] 

    sampling_frequency = 400  
    ch_names = ['FrL', 'FrR', 'OcR']
    info = mne.create_info(ch_names, sfreq=sampling_frequency, ch_types=['eeg'] * 3)

    raw = mne.io.RawArray(signals, info)
    annotations = mne.Annotations(onset=[], duration=[], description=[])
    
    analytics = Analytics(sampling_frequency) 
    analytics.total_time = len(classes) / sampling_frequency # Время записи в секундах

    i = 0
    last_end = 0  # Для вычисления интервалов между аномалиями
    while i < len(classes):
        class_label = classes[i]
        if class_label != 0:
            start = i
            while i < len(classes) and classes[i] == class_label:
                i += 1
            end = i

            onset_start = start / sampling_frequency
            onset_end = end / sampling_frequency
            duration = onset_end - onset_start

            analytics.anomaly_count += 1
            analytics.total_duration += duration
            analytics.durations.append(duration)
            analytics.anomalies_by_type[class_label].append((onset_start, onset_end))

            if last_end > 0:
                interval = onset_start - last_end
                analytics.intervals.append(interval)
            last_end = onset_end

            peak_amplitude = np.abs(np.max(signals[:, start:end]))
            peak_amplitude = np.exp(peak_amplitude)
            analytics.peak_amplitudes[class_label].append(peak_amplitude)

            if class_label == 1:
                description_start, description_end = 'swd1', 'swd2'
            elif class_label == 2:
                description_start, description_end = 'is1', 'is2'
            elif class_label == 3:
                description_start, description_end = 'ds1', 'ds2'

            annotations.append(onset_start, 0, description_start)
            annotations.append(onset_end, 0, description_end)
        else:
            i += 1

    raw.set_annotations(annotations)
    raw.export(output_file, fmt='edf')

    analytics.calculate_average_duration()
    analytics.calculate_percentage_with_anomalies()
    analytics.calculate_average_interval()
    
    return analytics 


# save_to_csv сохраняет 3 сигнала (FrL, FrR, OcR) вместе с классами в csv файл
def save_to_csv(data: np.ndarray, filename: str) -> None:

    header = 'FrL,FrR,OcR,Class'
    np.savetxt(filename, data, delimiter=',', header=header, comments='')



