FROM python:3.11-slim

WORKDIR /app

# Copy requirements from project root
COPY ../requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy all worker service files (flat structure)
COPY . /app

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
