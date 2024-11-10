import React, { useState } from 'react'
import './FileList.css'
import logo from '../../assets/test.jpg'
import logoDownload from '../../assets/download.svg'
import logoCopy from '../../assets/copy.svg'
import logoDownloadWhite from '../../assets/downloadWhite.svg'
import logoCopyWhite from '../../assets/copyWhite.svg'

interface FileWithProgress {
  file: File
  progress: number
  name: string
  word: string
  frl: string
  frr: string
  ocr: string
}

interface FileListProps {
  files: FileWithProgress[]
}

const FileList: React.FC<FileListProps> = ({ files }) => {
  const [showMore, setShowMore] = useState<boolean>(true)
  const [selectedFile, setSelectedFile] = useState<FileWithProgress | null>(null)

  const showMoreInfo = (file: FileWithProgress): void => {
    setSelectedFile(file)
    console.log(file.word)

    setShowMore(false)
  }

  const handleBack = (): void => {
    setShowMore(true)
    setSelectedFile(null)
  }

  return (
    <>
      {showMore ? (
        <div className="fileListWrap">
          <ul className="file-preview-loading-ul-list">
            {files.map((file, index) => (
              <li key={index} className="file-item-li">
                <div className="leftPart">
                  <img className="imgFile" src={logo} alt="file" />
                  <button className="buttonOpen" onClick={() => showMoreInfo(file)}>
                    Открыть
                  </button>
                </div>
                <div className="rightPart">
                  {file.name}
                  <div className="filesDownload">
                    <div className="subFiles">
                      <h4>График</h4>
                      <div className="buttonsFiles">
                        <div className="icons">
                          <img className="imgIcon" src={logoDownload} alt="" />
                          <button className="buttonDown">Скачать файл</button>
                        </div>
                        <div className="icons">
                          <img className="imgIcon" src={logoCopy} alt="" />
                          <button className="buttonCopy">Скопировать</button>
                        </div>
                      </div>
                    </div>
                    <div className="subFiles">
                      <h4>Отчёт</h4>
                      <div className="buttonsFiles">
                        <div className="icons">
                          <img className="imgIcon" src={logoDownload} alt="" />
                          <button className="buttonDown">Скачать файл</button>
                        </div>
                        <div className="icons">
                          <img className="imgIcon" src={logoCopy} alt="" />
                          <button className="buttonCopy">Скопировать</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div>
          <div className="topPartWrapper">
            <h2>{selectedFile?.name}</h2>
            <div className="topPart">
              <h4>Отчет</h4>
              <div className="icons">
                <img className="imgIcon" src={logoDownload} alt="" />
                <a href={selectedFile?.word} download={`Отчёт_по_${selectedFile?.name}.docx`}>
                  <button className="buttonDown">Скачать файл</button>
                </a>
              </div>
              <div className="icons">
                <img className="imgIcon" src={logoCopy} alt="" />
                <button className="buttonCopy">Скопировать</button>
              </div>
            </div>
          </div>
          <div>
            <img className="imgFileMore" src={logo} alt="file" />
          </div>
          <div className="bottomPart">
            <button className="buttonBack" onClick={handleBack}>
              Назад
            </button>
            <div className="buttomWrapper">
              <div className="icons-wrap">
                <img className="imgIconMore" src={logoDownloadWhite} alt="" />
                <a
                  href={`http://vpn.v0d14ka.ru:8005/${selectedFile?.word}`}
                  download={`Отчёт_по_${selectedFile?.name}.docx`}
                >
                  <button className="buttonDownMore">Скачать файл</button>
                </a>
              </div>
              <div className="icons-wrap">
                <img className="imgIconMore" src={logoCopyWhite} alt="" />
                <button className="buttonCopyMore">Скопировать</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default FileList
