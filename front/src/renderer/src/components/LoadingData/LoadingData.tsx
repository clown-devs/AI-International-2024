import React, { useState } from 'react'
import './LoadingData.css'
import logo from '../../assets/upload.svg'

import logoFile from '../../assets/file.svg'

interface FileWithProgress {
  file: File
  progress: number
  name: string
}

interface LoadingDataProps {
  files: FileWithProgress[]
}

const LoadingData: React.FC<LoadingDataProps> = ({ files }) => {
  const [fileNames, setFileNames] = useState<string[]>([])
  const [isDragging, setIsDragging] = useState<boolean>(false)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const files = event.target.files
    if (files) {
      const fileArrayName = Array.from(files).map((file) => file.name)

      setFileNames(fileArrayName)
      console.log('Выбраны файлы:', fileArrayName)
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

      setFileNames(fileArrayName)
      console.log('Перетащены файлы:', fileArrayName)
    }
  }

  const removeFile = (index: number): void => {
    const newFileNames = [...fileNames]
    newFileNames.splice(index, 1)
    setFileNames(newFileNames)
  }

  const fileCountText = fileNames.length === 1 ? 'файл' : 'файлы'

  return (
    <>
      <div
        className={`file-upload-loading ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <img className="upload-icon" src={logo} alt="upload icon" />
        <div>
          <h2>Загрузить edf {fileCountText}</h2>
          <h4 className="textFile">Перетащите или выберите {fileCountText}</h4>
        </div>
        <label className="file-select-button">
          <input type="file" multiple onChange={handleFileSelect} />
          Выберите {fileCountText}
        </label>

        {fileNames.length > 0 && (
          <div className="file-preview-loading">
            {fileNames.map((name, index) => (
              <div key={index} className="file-item">
                {name}
                <button className="remove-file-button" onClick={() => removeFile(index)}>
                  &times;
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="file-preview-loading-ul">
        {files.map((file, index) => (
          <div key={index} className="file-item-ul">
            <img className="upload-icon-ul" src={logoFile} alt="upload icon" />
            <div className="wrapper">
              <div className="file-name-ul">{file.name}</div>
              <div className="progress-bar-ul-wrap">
                <div className="progress-bar-ul">
                  <div className="progress-ul" style={{ width: `${file.progress}%` }}></div>
                </div>
                <span>{file.progress}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

export default LoadingData
