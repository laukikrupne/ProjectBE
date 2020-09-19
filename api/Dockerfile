FROM python:3.6.9
WORKDIR /usr/src/api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn","--bind","0.0.0.0:8000","app:app"]
