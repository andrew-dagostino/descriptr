// Code modified from https://www.freecodecamp.org/news/building-an-electron-application-with-create-react-app-97945861647c/

const electron = require('electron');
// Modules to control application life and native browser window
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

const path = require('path');
const url = require('url');

// Global reference of the window object. 
let mainWindow;

function createWindow() {
  // Create browser window
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true
    }
  });

  // loads the index.html of the app
  mainWindow.loadURL('http://localhost:3000');

  // Opens the dev tools. Comment out to get rid of them.
  mainWindow.webContents.openDevTools();

  // Dereference window object on closure
  mainWindow.on('closed', function () {
    mainWindow = null
  })
}

// Create browser window after initialization
app.whenReady().then(createWindow)

// Quit app when all windows are closed except on macOS
// (It is common that apps stay open until user explitly quits)
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit()
  }
});

// Recreates the window on macOS when user clicks on dock icon
app.on('activate', function () {
  if (mainWindow === null) {
    createWindow()
  }
});