# Use an official lightweight Python image.
FROM python:3.12-alpine

LABEL authors="castox"

WORKDIR /app
COPY api/ api/

RUN pip install --no-cache-dir -r api/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
