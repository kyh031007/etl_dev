FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Python dependencies 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일들 복사
COPY etl/main.py /opt/airflow/main.py
COPY etl/src/ /opt/airflow/src/
COPY etl/dags/ /opt/airflow/dags/
COPY etl/model/ /opt/airflow/model/
COPY etl/config.py /opt/airflow/config.py
COPY etl/.env /opt/airflow/.env

# 작업 디렉토리 설정
WORKDIR /opt/airflow

# 환경 변수 설정
ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"

# 로그 및 출력 디렉토리 생성
RUN mkdir -p /opt/airflow/logs /opt/airflow/output 