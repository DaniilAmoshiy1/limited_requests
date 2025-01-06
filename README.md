# limited_requests

Code that displays a json page and limits the number of requests per minute via IP

### Working with the environment on Windows:
create venv:
```bash
python -m venv venv
```

activate venv:
```bash
venv/Scripts/activate
```

### For start use code:
download requirements:
```bash
pip install -r requirements.txt
```

start_server(local):
```bash
uvicorn main:app --reload
```

go to web page if was local start:
http://127.0.0.1:8000

for stop local server, point to cmd(in IDE) and press Ctrl + C
