from collections import defaultdict
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from scripts.config import NUMBER_ALLOWED_REQUESTS, SECOND_LIMIT


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


ip_counters = defaultdict(list)


@app.get('/')
async def get_main_page():
    return {'Frog': 'Kvaaa'}


@app.middleware('http')
async def request_limit(request: Request, call_next):
    user_ip = request.client.host
    current_time = time.time()

    ip_counters[user_ip] = list(
        filter(
            lambda timestamp: current_time - timestamp <= SECOND_LIMIT, ip_counters[user_ip]
        )
    )

    if len(ip_counters[user_ip]) >= NUMBER_ALLOWED_REQUESTS:
        return templates.TemplateResponse('error_429.html', {'request': request})

    ip_counters[user_ip].append(current_time)
    response = await call_next(request)

    return response
