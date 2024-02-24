### demucs binary

First time creating the .spec file
```bash
cd /app/app 
pyinstaller --add-data="/usr/local/lib/python3.11/site-packages/demucs:demucs/" separator.py
```

Running using .spec file
```bash
pyinstaller separator.spec
```
