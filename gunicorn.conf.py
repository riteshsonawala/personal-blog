import os

# Server socket
bind = "0.0.0.0:{}".format(os.environ.get('PORT', 2112))
backlog = 2048

# Worker processes
workers = int(os.environ.get('WEB_CONCURRENCY', 4))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
loglevel = os.environ.get('LOG_LEVEL', 'info')
accesslog = '-'
errorlog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'personal-blog'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Enable stats
statsd_host = None