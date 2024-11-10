import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

// Интерфейсы для типов данных
interface GraphData {
  mode: string;
  name: string;
  x: number[];
  y: number[];
  type?: string;  // Тип графика (например, 'scatter', 'line' и т.д.)
  line?: { color: string, dash?: string };  // Цвет линии и тип (пунктир или сплошная)
}

interface JsonData {
  data: GraphData[];
}

// Добавляем пропсы для URL-адресов
interface PlotlyWidgetProps {
  url1: string;  // URL для первого JSON
  url2: string;  // URL для второго JSON
  url3: string;  // URL для третьего JSON
}

const PlotlyWidget: React.FC<PlotlyWidgetProps> = ({ url1, url2, url3 }) => {
  const [graphData1, setGraphData1] = useState<GraphData[] | null>(null);
  const [graphData2, setGraphData2] = useState<GraphData[] | null>(null);
  const [graphData3, setGraphData3] = useState<GraphData[] | null>(null);

  useEffect(() => {
    // Функция для загрузки JSON данных с сервера
    const fetchData = async () => {
      try {
        // Выполняем три GET-запроса с использованием axios
        const response1 = await axios.get(url1);
        const response2 = await axios.get(url2);
        const response3 = await axios.get(url3);

        // Преобразуем ответы в данные
        const jsonData1: JsonData = response1.data;
        const jsonData2: JsonData = response2.data;
        const jsonData3: JsonData = response3.data;

        // Устанавливаем данные в стейт для каждого графика
        setGraphData1(jsonData1.data);
        setGraphData2(jsonData2.data);
        setGraphData3(jsonData3.data);
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      }
    };

    fetchData();
  }, [url1, url2, url3]);  // Следим за изменениями URL

  // Если данные ещё не загружены, показываем индикатор загрузки
  if (!graphData1 || !graphData2 || !graphData3) {
    return <p>Загружаем данные...</p>;
  }

  // Определяем общие настройки для всех субграфиков
  const layout = {
    grid: { rows: 3, columns: 1, pattern: 'independent' },
    height: 900,  // Общая высота для всех графиков
    showlegend: true,
    xaxis: { title: 'time' },  // Для первого графика
    yaxis: { title: 'mu' },  // Для первого графика
    xaxis2: { title: 'time' }, // Для второго графика
    yaxis2: { title: 'mu' }, // Для второго графика
    xaxis3: { title: 'time' }, // Для третьего графика
    yaxis3: { title: 'mu' }, // Для третьего графика
  };

  // Формируем данные для графиков с условием для отображения легенды
  const plotData = [
    ...graphData1.map((item) => {
      const showLegend = !(item.line?.dash === 'dot' || item.mode === 'markers');
      return {
        x: item.x,
        y: item.y,
        mode: item.mode,
        name: item.name,  // Устанавливаем название графика вручную для первого графика
        type: item.type || 'scatter',
        xaxis: 'x1',  // Для первого графика
        yaxis: 'y1',
        line: item.line,  // Используем цвет линии из данных
        showlegend: showLegend, // Устанавливаем условие для отображения легенды
      };
    }),
    ...graphData2.map((item) => {
      const showLegend = !(item.line?.dash === 'dot' || item.mode === 'markers');
      return {
        x: item.x,
        y: item.y,
        mode: item.mode,
        name: item.name,  // Устанавливаем название графика вручную для второго графика
        type: item.type || 'scatter',
        xaxis: 'x2',  // Для второго графика
        yaxis: 'y2',
        line: item.line,  // Используем цвет линии из данных
        showlegend: showLegend, // Устанавливаем условие для отображения легенды
      };
    }),
    ...graphData3.map((item) => {
      const showLegend = !(item.line?.dash === 'dot' || item.mode === 'markers');
      return {
        x: item.x,
        y: item.y,
        mode: item.mode,
        name: item.name,  // Устанавливаем название графика вручную для третьего графика
        type: item.type || 'scatter',
        xaxis: 'x3',  // Для третьего графика
        yaxis: 'y3',
        line: item.line,  // Используем цвет линии из данных
        showlegend: showLegend === true, // Устанавливаем условие для отображения легенды
      };
    }),
  ];

  return (
    <div className="plotly-widget">
      <Plot
        data={plotData}
        layout={layout}
      />
    </div>
  );
};

export default PlotlyWidget;
