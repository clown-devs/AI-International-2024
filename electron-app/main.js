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
      preload: path.join(__dirname, 'preload.js'), // используем __dirname как в CommonJS
    },
  });

  mainWindow.loadURL('http://localhost:5173'); // Подключение к серверу Vite
}

app.whenReady().then(createWindow);
