FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY extractor.py .

RUN pip install --no-cache-dir pymupdf

CMD ["python", "extractor.py"]
