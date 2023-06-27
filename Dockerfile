FROM python:3.9


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app
WORKDIR /app


ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0


CMD ["python", "main.py"]
