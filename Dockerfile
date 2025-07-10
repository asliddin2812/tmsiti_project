# Python 3.11 asosida eng minimal image
FROM python:3.11-slim

# Rust build muhit sozlamalari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_BUILD_ISOLATION=1 \
    PIP_ONLY_BINARY=:all: \
    CARGO_HOME=/tmp/cargo \
    RUSTUP_HOME=/tmp/rustup \
    PATH="/root/.cargo/bin:$PATH"

# Ishchi katalog
WORKDIR /app

# Zarur tizim kutubxonalarini o‘rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    curl \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Rust toolchainni o‘rnatish
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Pydantic va pydantic-settings uchun .whl bilan o‘rnatish (Rust kutubxona bo‘lishiga qaramay)
RUN pip install --only-binary pydantic,pydantic-core \
    "pydantic==2.5.0" \
    "pydantic-settings==2.1.0"

# requirements.txt fayl orqali qolgan kutubxonalarni o‘rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani konteynerga nusxalash
COPY . .

# Static fayllar uchun papkalar
RUN mkdir -p static/uploads static/default

# Oddiy user bilan ishlash (root bo‘lmaslik uchun)
RUN useradd --create-home --shell /bin/bash tmsiti && chown -R tmsiti:tmsiti /app
USER tmsiti

# Uvicorn port
EXPOSE 8000

# Health check (agar health endpoint bo‘lsa)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Loyihani ishga tushirish
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
