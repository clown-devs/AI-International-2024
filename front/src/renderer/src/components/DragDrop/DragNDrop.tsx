import React, { useState } from 'react'
import './DragNDrop.css'
import logo from '../../assets/upload.svg'

interface DragNDropProps {
  onFilesSelected: (files: File[]) => void
}

const DragNDrop: React.FC<DragNDropProps> = ({ onFilesSelected }) => {
  const [fileNames, setFileNames] = useState<string[]>([])
  const [isDragging, setIsDragging] = useState<boolean>(false)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const files = event.target.files
    if (files) {
      const fileArrayName = Array.from(files).map((file) => file.name)
      const fileArray = Array.from(files)

      setFileNames(fileArrayName)
      console.log('Выбраны файлы:', fileArrayName)
      onFilesSelected(fileArray)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>): void => {
    event.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (): void => {
    setIsDragging(false)
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>): void => {
    event.preventDefault()
    setIsDragging(false)
    const files = event.dataTransfer.files
    if (files) {
      const fileArrayName = Array.from(files).map((file) => file.name)
      const fileArray = Array.from(files)
      setFileNames(fileArrayName)
      console.log('Перетащены файлы:', fileArrayName)
      onFilesSelected(fileArray)
    }
  }

  const removeFile = (index: number): void => {
    const newFileNames = [...fileNames]
    newFileNames.splice(index, 1)
    setFileNames(newFileNames)
  }

  const fileCountText = fileNames.length === 1 ? 'файл' : 'файлы'

  return (
    <div
      className={`file-upload ${isDragging ? 'dragging' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <img className="upload-icon" src={logo} alt="upload icon" />
      <h1>Загрузить edf {fileCountText}</h1>
      <h4 className="textFile">Перетащите или выберите {fileCountText}</h4>
      <label className="file-select-button">
        <input type="file" multiple onChange={handleFileSelect} />
        Выберите {fileCountText}
      </label>

      {fileNames.length > 0 && (
        <div className="file-preview">
          {fileNames.map((name, index) => {
            const shortenedName = name.length > 11 ? name.substring(0, 11) + '...' : name

            return (
              <div key={index} className="file-item">
                {shortenedName}
                <button className="remove-file-button" onClick={() => removeFile(index)}>
                  &times;
                </button>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default DragNDrop
