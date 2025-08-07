@echo off

python\python.exe -m pip install --upgrade pip setuptools

python\python.exe -m pip install virtualenv
python\python.exe -m virtualenv .venv

.venv\Scripts\python.exe -m pip install --upgrade pip setuptools

.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m unidic download 2>&1

@pause