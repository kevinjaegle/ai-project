# ========== Build-Stage ==========
FROM python:3.11-slim AS builder
WORKDIR /app

# System-Tools für manche Wheels (falls nötig, sonst auskommentieren)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ========== Runtime-Stage ==========
FROM python:3.11-slim
WORKDIR /app

# Sicherheits-Upgrade (klein halten)
RUN useradd -m -u 1000 appuser

# Wheels + App rein
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

# Besitz anpassen und als Nicht-Root laufen
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck (optional; viele Hoster haben eigenen)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import requests; import sys; \
  sys.exit(0) if requests.get('http://127.0.0.1:8000/health', timeout=2).status_code==200 else sys.exit(1)" || exit 1

CMD ["sh", "-c", "uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
