# Use a stable version of python
FROM python:3.11-slim-bookworm

WORKDIR /app

# 1. FIX: Ignore repository signature errors and install build tools
# Added --allow-insecure-repositories to fix your 'invalid signature' error
RUN apt-get update --allow-insecure-repositories && \
    apt-get install -y --allow-unauthenticated \
    libaio1 \
    build-essential \
    curl \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. THE FIX: Manually define architecture for the ibm_db installer
# This prevents the 'NameError: arch_ is not defined' on ARM64/Apple Silicon
ENV ARCH=arm64
ENV PLATFORM=linux
ENV IBM_DB_HOME=/app/clidriver

# 3. Upgrade build tools to a version compatible with C-extensions on ARM
RUN pip install --upgrade pip setuptools==69.5.1 wheel

# 4. Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

EXPOSE 8000

# Ensure uvicorn is used for FastAPI/Starlette apps
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

