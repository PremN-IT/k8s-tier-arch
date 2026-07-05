FROM python:3.11-slim
WORKDIR /app
COPY src/requirementx.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python", "app.py"]

