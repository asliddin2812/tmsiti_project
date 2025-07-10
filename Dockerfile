# Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_BUILD_ISOLATION=1 \
    PIP_ONLY_BINARY=:all:

# Tizim uchun kerakli kutubxonalarni o‘rnatish
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# ⚠️ Avval pydantic & settings'ni `.whl` bilan o‘rnatamiz
RUN pip install --only-binary pydantic,pydantic-core \
    "pydantic==2.5.0" \
    "pydantic-settings==2.1.0"

# Endi qolgan barcha kutubxonalarni o‘rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani nusxalash
COPY . .

# Static media papkalar
RUN mkdir -p static/uploads static/default

# Non-root user
RUN useradd --create-home --shell /bin/bash tmsiti \
    && chown -R tmsiti:tmsiti /app

USER tmsiti

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
