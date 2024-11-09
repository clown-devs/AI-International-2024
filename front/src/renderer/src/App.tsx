import axios from 'axios'
import DragNDrop from './components/DragDrop/DragNDrop'
import { useState } from 'react'
import Plot from 'react-plotly.js'
import LoadingData from './components/LoadingData/LoadingData'

interface FileWithProgress {
  file: File
  progress: number
  name: string
}

function App(): JSX.Element {
  const [files, setFiles] = useState<FileWithProgress[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<{
    FrL: number[]
    FrR: number[]
    OcR: number[]
    classes: number[]
  } | null>(null)

  const handleFileSelected = (files: File[]): void => {
    const newFiles = files.map((file) => ({
      file,
      progress: 0,
      name: file.name
    }))

    setFiles((prevFiles) => [...prevFiles, ...newFiles]) // Добавляем новые файлы в состояние
  }

  const uploadFiles = async (): Promise<void> => {
    if (files.length === 0) {
      console.log('Нет выбранных файлов для загрузки')
      return
    }
    console.log('qwqqwqww', files)

    setLoading(true)
    setError(null)

    const uploadPromises = files.map(async (fileWithProgress) => {
      const formData = new FormData()
      formData.append('file', fileWithProgress.file)

      try {
        await axios.post('http://vpn.v0d14ka.ru:8005/upload', formData, {
          onUploadProgress: (progressEvent) => {
            const total = progressEvent.total ?? 1
            const progress = Math.round((progressEvent.loaded * 100) / total)
            setFiles((prevFiles) =>
              prevFiles.map((f) => (f.name === fileWithProgress.name ? { ...f, progress } : f))
            )
          }
        })
      } catch (error) {
        console.error(`Ошибка загрузки файла ${fileWithProgress.name}:`, error)
        setError(`Не удалось загрузить файл ${fileWithProgress.name}`)
      }
    })
    await Promise.all(uploadPromises)
  }

  if (error) return <p>{error}</p>

  return (
    <>
      {loading && <LoadingData files={files} />}

      {!loading && <DragNDrop onFilesSelected={handleFileSelected} />}

      <div className="tabButton">
        <button className="activeButton cancel">Отменить</button>
        <button className="activeButton" onClick={uploadFiles}>
          Загрузить
        </button>
      </div>
      {/* {data && (
        <Plot
          data={[
            {
              x: [data.FrL],
              y: data.FrR,
              type: 'scatter', // Измените на нужный тип графика, например 'bar' для гистограммы
              mode: 'lines+markers',
              marker: { color: 'blue' }
            }
          ]}
          layout={{ title: 'Ваш график', xaxis: { title: 'X' }, yaxis: { title: 'Y' } }}
        />
      )} */}
    </>
  )
}

export default App
