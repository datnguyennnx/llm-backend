# Use an official Python runtime (Python 3.13 is fine, if asyncpg>=0.27.0 supports it)
FROM python:3.13-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies including Python dev headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libc6-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies (ensure asyncpg>=0.27.0 is specified)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]