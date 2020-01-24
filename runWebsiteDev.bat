@ECHO OFF
CALL activate clipd
cmd.exe /K "cd C:\Users\zaroh\Documents\GitHub\clipd&&C:&&set FLASK_APP=app&&set ^FLASK_ENV=development&&flask run -p 8000"