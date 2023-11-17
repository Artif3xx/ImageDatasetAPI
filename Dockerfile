# Use an official lightweight Python image.
FROM python:3.10-slim

LABEL authors="castox"

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-opencv python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY api/ api/

RUN pip install --no-cache-dir -r api/requirements.txt

RUN apt-get purge -y python3-pip \
    && apt-get autoremove -y \
    && apt-get clean

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
