FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Install libGL and libgthread for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=run.py
EXPOSE 5000
CMD ["gunicorn", "run:app", "-c", "gunicorn_config.py"]