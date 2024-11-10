import axios from 'axios'
import DragNDrop from './components/DragDrop/DragNDrop'
import FileList from './components/FileList/FileList'
import { useState } from 'react'
import LoadingData from './components/LoadingData/LoadingData'

interface FileWithProgress {
  file: File
  progress: number
  name: string
  word: string
  frl: string
  frr: string
  ocr: string
}

function App(): JSX.Element {
  const [files, setFiles] = useState<FileWithProgress[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [showList, setShowList] = useState<boolean>(true)
  const [showData, setShowData] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelected = (files: File[]): void => {
    const newFiles = files.map((file) => ({
      file,
      progress: 0,
      name: file.name,
      word: '',
      frl: '',
      frr: '',
      ocr: ''
    }))

    setFiles((prevFiles) => [...prevFiles, ...newFiles]) // Добавляем новые файлы в состояние
  }

  const uploadFiles = async (): Promise<void> => {
    if (files.length === 0) {
      console.log('Нет выбранных файлов для загрузки')
      return
    }

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
    setShowData(true)
  }

  const showFileList = (): void => {
    setShowList(false)
  }

  if (error) return <p>{error}</p>

  return (
    <>
      {loading && showList && <LoadingData files={files} />}

      {!loading && showList && <DragNDrop onFilesSelected={handleFileSelected} />}

      {!showList && <FileList files={files} />}

      {showList && (
        <div className="tabButton">
          <button className="activeButton cancel">Отменить</button>
          {loading ? (
            <button className={`activeButton ${!showData ? 'loading' : ''}`} onClick={showFileList}>
              {!showData ? 'Загрузка данных' : 'Показать данные'}
            </button>
          ) : (
            <button className="activeButton" onClick={uploadFiles}>
              Загрузить
            </button>
          )}
        </div>
      )}
    </>
  )
}

export default App
