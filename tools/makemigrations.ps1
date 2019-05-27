Set-Location $PSScriptRoot/..
& venv/Scripts/Activate.ps1
python web/manage.py makemigrations
python web/manage.py migrate
