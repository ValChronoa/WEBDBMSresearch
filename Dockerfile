FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Install libGL for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=run.py
EXPOSE 5000
CMD ["gunicorn", "run:app", "-c", "gunicorn_config.py"]