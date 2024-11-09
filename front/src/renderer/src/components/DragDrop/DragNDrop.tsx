import React, { useState } from 'react'
import './DragNDrop.css'
import logo from '../../assets/upload.svg'

const DragNDrop: React.FC = () => {
  const [fileNames, setFileNames] = useState<string[]>([])
  const [isDragging, setIsDragging] = useState<boolean>(false)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const files = event.target.files
    if (files) {
      const fileArray = Array.from(files).map((file) => file.name)
      setFileNames(fileArray)
      console.log('Выбраны файлы:', fileArray)
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
      const fileArray = Array.from(files).map((file) => file.name)
      setFileNames(fileArray)
      console.log('Перетащены файлы:', fileArray)
    }
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
        <div className="file-names">
          <p>Выбранные {fileCountText}:</p>
          <ul>
            {fileNames.map((name, index) => (
              <li key={index}>{name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default DragNDrop
