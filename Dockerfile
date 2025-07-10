# Python 3.12 slim tasviridan foydalanamiz
FROM python:3.12-slim

# Ishchi direktoriyani sozlash
WORKDIR /app

# Tizim kutubxonalarni o'rnatish
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# pip-ni yangilash
RUN pip install --upgrade pip

# Rust o'rnatish (cryptography uchun)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Python paketlarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . .

# Portni ochish
EXPOSE 8000

# Ilovani ishga tushirish
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]