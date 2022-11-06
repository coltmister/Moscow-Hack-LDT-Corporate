import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "settings.wsgi"
# preload_app = True
reload = True
max_requests = 1000


