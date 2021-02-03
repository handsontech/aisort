ECHO ON
cd aiweb

TASKKILL /IM chrome.exe

start  npm start

timeout /t 3

start chrome http://127.0.0.1 
