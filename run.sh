#!/bin/bash

# ETL Airflow 시스템 Docker 실행 스크립트

echo "ETL Airflow 시스템 배포를 시작합니다..."

# 환경 변수 설정 (필요에 따라 수정)
source .env

# 필요한 디렉토리 생성 및 권한 설정
echo "디렉토리 권한 설정 중..."
mkdir -p etl/logs etl/output
chmod -R 777 etl/logs etl/output

# Airflow 컨테이너만 중지
echo "Airflow 컨테이너 중지 중..."
docker-compose down

# PostgreSQL 상태 확인 및 시작
# echo "PostgreSQL 데이터베이스 상태 확인 중..."
# if ! docker-compose -f docker-compose-db.yml ps | grep -q "Up"; then
#     echo "PostgreSQL 데이터베이스 시작 중..."
#     docker-compose -f docker-compose-db.yml up -d
#     echo "데이터베이스 준비 대기 중..."
#     sleep 10
# else
#     echo "PostgreSQL 데이터베이스가 이미 실행 중입니다."
# fi

# ETL 시스템 재빌드 및 실행
echo "ETL 시스템 재빌드 및 실행 중..."
docker-compose up --build -d

# 데이터베이스 준비 대기
echo "PostgreSQL 시작 대기 중..."
sleep 15

# Airflow 데이터베이스 초기화 (처음 실행시에만)
echo "Airflow 데이터베이스 초기화 중..."
docker-compose exec -T airflow-webserver airflow db init || echo "DB 이미 초기화됨"

# 관리자 계정 생성 (처음 실행시에만)
echo "Airflow 관리자 계정 생성 중..."
docker-compose exec -T airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || echo "관리자 계정 이미 존재"

# 실행 상태 확인
echo "시스템 상태 확인..."
sleep 5
echo "=== ETL 시스템 전체 상태 ==="
docker-compose ps

echo ""
echo "=== 실행 완료 ==="
echo "Airflow Web UI: http://localhost:9090"
echo "로그인: admin / admin"
echo "PostgreSQL: localhost:5434"
echo "DAG ID: air_quality_etl_pipeline"
echo ""
echo "유용한 명령어:"
echo "   전체 로그 확인: docker-compose logs -f"
echo "   특정 서비스 로그: docker-compose logs -f [postgres|airflow-webserver|airflow-scheduler]"
echo "   전체 중지: docker-compose down"
echo "   데이터베이스 재초기화: docker-compose exec airflow-webserver airflow db reset" 