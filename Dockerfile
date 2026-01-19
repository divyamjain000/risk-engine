FROM python:3.11-slim AS test
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY . .
RUN pytest -q

FROM python:3.11-slim
WORKDIR /app
COPY --from=test /app /.test_artifacts
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
