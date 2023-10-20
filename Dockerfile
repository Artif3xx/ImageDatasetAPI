FROM python:3.10-slim

WORKDIR /app

COPY api/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY api api
COPY package.json package.json

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
