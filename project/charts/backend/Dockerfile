FROM python:3.11-slim

WORKDIR /app

# --- everything below runs as root (build-time) ---

# Upgrade packaging tools (clears the wheel / setuptools CVEs Trivy flagged)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Create a non-root user and hand it the app directory, THEN drop to it.
# Only the running gunicorn process needs to be unprivileged.
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]