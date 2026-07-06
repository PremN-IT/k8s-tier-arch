FROM python:3.11-slim

# Run as a non-root user for security


WORKDIR /app

# Upgrade packaging tools (clears the wheel / setuptools CVEs Trivy flagged)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .



CMD ["python", "app.py"]
