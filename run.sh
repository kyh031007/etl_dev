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
echo "PostgreSQL 데이터베이스 상태 확인 중..."
if ! docker-compose -f docker-compose-db.yml ps | grep -q "Up"; then
    echo "PostgreSQL 데이터베이스 시작 중..."
    docker-compose -f docker-compose-db.yml up -d
    echo "데이터베이스 준비 대기 중..."
    sleep 10
else
    echo "PostgreSQL 데이터베이스가 이미 실행 중입니다."
fi

# Airflow 이미지 재빌드 및 실행
echo "Airflow 재빌드 및 실행 중..."
docker-compose up --build -d

# 실행 상태 확인
echo "애플리케이션 실행 상태 확인..."
sleep 5
echo "=== PostgreSQL 상태 ==="
docker-compose -f docker-compose-db.yml ps
echo "=== Airflow 상태 ==="
docker-compose ps

echo ""
echo "=== 실행 완료 ==="
echo "Airflow Web UI: http://localhost:9090"
echo "로그인: admin / admin"
echo "PostgreSQL: localhost:5434"
echo "DAG ID: air_quality_etl_pipeline"
echo ""
echo "유용한 명령어:"
echo "   로그 확인: docker-compose logs -f"
echo "   DB 로그 확인: docker-compose -f docker-compose-db.yml logs -f"
echo "   전체 중지: docker-compose down && docker-compose -f docker-compose-db.yml down" 