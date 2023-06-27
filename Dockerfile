FROM python:3.9

# Встановлюємо залежності проекту
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо файли проекту у контейнер
COPY . /app
WORKDIR /app

# Встановлюємо Flask змінні середовища
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Запускаємо додаток
CMD ["python", "main.py"]
