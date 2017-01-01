import multiprocessing

bind = "0.0.0.0:8000"
backlog = 2048
threads = 1

proc_name = "govern"

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000

timeout = 30
keepalive = 2
graceful_timeout = 30

max_requests = 0
max_requests_jitter = 0

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

reload = False
spew = False
check_config = False

daemon = False
sendfile = True
preload_app = False

loglevel = "info"
logger_class = "gunicorn.glogging.Logger"
