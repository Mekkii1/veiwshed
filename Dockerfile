FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install numpy rasterio fastapi uvicorn

CMD ["uvicorn", "veiwshedd:app", "--host", "127.0.0.1", "--port", "8000"]
