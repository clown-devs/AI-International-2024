import { app, BrowserWindow } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

// Определение __dirname в ES-модуле
const __dirname = path.dirname(fileURLToPath(import.meta.url));

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      enableRemoteModule: false,
    },
  });

  const filePath = path.join(__dirname, 'index.html');
  console.log('Loading file:', filePath);
  mainWindow.loadFile(filePath);
}

app.whenReady().then(createWindow);
