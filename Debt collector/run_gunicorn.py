import os
os.system("gunicorn --bind 0.0.0.0:8000 --workers 4 app:app")
if __name__ == "__main__":
    os.system("gunicorn --bind 127.0.0.1:8000 wsgi:app")
