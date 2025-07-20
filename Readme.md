python.exe -m pip install --upgrade pip

python -Xutf8 manage.py dumpdata product --indent 2 --output data.json

python -Xutf8 manage.py loaddata data.json