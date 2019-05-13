cd $PSScriptRoot/..
python -m venv --system-site-packages venv
& venv/Scripts/Activate.ps1
python -m pip install -U pip setuptools
pip install -U -r requirements.txt
