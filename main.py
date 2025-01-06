from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import time

from config import NUMBER_ALLOWED_REQUESTS, TIME_LIMIT


app = FastAPI()
templates = Jinja2Templates(directory='templates')


class ConnectionCounter:
    def __init__(self, requests_per_period: int, time_limit: int):
        self.requests_per_period = requests_per_period
        self.time_limit = time_limit
        self.request_count = 0
        self.last_reset_time = time.time()

    def plus_counter(self):
        current_time = time.time()
        if current_time - self.last_reset_time > self.time_limit:
            self.request_count = 0
            self.last_reset_time = current_time

        if self.request_count < self.requests_per_period:
            self.request_count += 1
            return True
        return False


counter = ConnectionCounter(NUMBER_ALLOWED_REQUESTS, TIME_LIMIT)


ip_counters = {}


@app.get('/')
async def get_main_page():
    return {'Frog': 'Kvaaa'}


@app.middleware('http')
async def request_limit(request: Request, call_next):
    user_ip = request.client.host

    if user_ip not in ip_counters:
        ip_counters[user_ip] = ConnectionCounter(NUMBER_ALLOWED_REQUESTS, TIME_LIMIT)

    ip_counter = ip_counters[user_ip]

    if not ip_counter.plus_counter():
        return templates.TemplateResponse('error_429.html', {'request': request})

    response = await call_next(request)
    return response
