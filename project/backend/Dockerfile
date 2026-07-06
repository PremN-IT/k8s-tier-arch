FROM python:3.11-alpine

# Run as a non-root user for security
RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

# Upgrade packaging tools (clears the wheel / setuptools CVEs Trivy flagged)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app src/ .

USER app

CMD ["python", "app.py"]
