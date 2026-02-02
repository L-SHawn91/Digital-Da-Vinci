# Dockerfile - SHawn-Brain Backend

FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드
COPY ddc ./ddc

# 포트
EXPOSE 8000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 시작
CMD ["uvicorn", "ddc.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
