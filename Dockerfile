FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libpangocairo-1.0-0 \
    libatspi2.0-0 \
    libdrm2 \
    ca-certificates \
    fonts-liberation \
    wget \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Playwright ve bağımlılıklarını kur
RUN pip install --no-cache-dir fastapi uvicorn playwright

# Playwright tarayıcılarını indir
RUN playwright install --with-deps

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
