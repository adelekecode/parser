# gunicorn_config.py

bind = "0.0.0.0:8000"  # Specify the host and port
workers = 4  # Number of worker processes
timeout = 60 # Time in seconds before a worker is killed and restarted
