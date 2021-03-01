require('dotenv').config();

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
            contextIsolation: true,
        },
    });

    // loads the index.html of the app
    if (process.env.ENV === 'DEV') {
        //mainWindow.loadURL('https://dev.cis4250-03.socs.uoguelph.ca'); //This doesn't work for local dev but we want it to.
        mainWindow.loadURL('http://localhost:3000');
    } else {
        mainWindow.loadURL(`file://${path.join(__dirname, '../build/index.html')}`);
    }

    // Opens the dev tools. Comment out to get rid of them.
    //mainWindow.webContents.openDevTools();

    // Dereference window object on closure
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

// Create browser window after initialization
app.whenReady().then(createWindow);

// Quit app when all windows are closed except on macOS
// (It is common that apps stay open until user explitly quits)
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Recreates the window on macOS when user clicks on dock icon
app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});
