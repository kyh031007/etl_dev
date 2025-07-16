# 대기오염 중금속 데이터 ETL 시스템

Apache Airflow를 사용하여 대기오염 중금속 데이터를 자동으로 수집, 가공하고 AWS S3에 저장하는 ETL 파이프라인입니다.

## 기술 스택

- **Python 3.10+**: 메인 개발 언어
- **Apache Airflow 2.8.1**: 워크플로우 관리 및 스케줄링
- **PostgreSQL 13**: 수집정보 및 설정 저장
- **Docker**: 컨테이너화 환경
- **AWS S3**: 데이터 저장소
- **polars**: 데이터 처리

## 프로젝트 구조

```
etl_dev/
├── etl/
│   ├── dags/
│   │   └── air_pollution_dag.py     # Airflow DAG 파일
│   ├── src/
│   │   ├── data_collector.py        # 데이터 수집
│   │   ├── data_proccess.py         # 데이터 가공
│   │   └── s3_uploader.py           # S3 업로드
│   ├── model/
│   │   └── manager_dao.py           # 데이터베이스 관리
│   ├── config.py                    # 설정 관리
│   ├── main.py                      # 메인 실행 파일
│   ├── logs/                        # 로그 파일
│   └── output/                      # 📁 로컬 파일 저장 위치
│       └── 202507/
│           └── 20250716_collect.csv
├── docker-compose.yml               # Airflow 서비스
├── docker-compose-db.yml            # PostgreSQL 서비스
├── Dockerfile                       # Airflow 이미지
├── requirements.txt                 # Python 의존성
└── README.md
```

## 빠른 시작

### 1. 환경 설정

프로젝트 루트에 `.env` 파일 생성:

```bash
# PostgreSQL 데이터베이스 설정
POSTGRES_HOST=postgres
POSTGRES_PORT=5432  # Docker 내부 통신용 (외부 접속은 5434)
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# AWS S3 설정
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=ap-northeast-2
S3_BUCKET_NAME=your_bucket_name

# API 키 설정
OPENAPI_SERVICE_KEY=your_openapi_service_key_here

# Airflow 보안 키
AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key_here

# 출력 디렉토리
OUTPUT_DIR=/opt/airflow/output
```

### 2. 서비스 시작

```bash
# 1. PostgreSQL 데이터베이스 시작
docker-compose -f docker-compose-db.yml up -d

# 2. Airflow 서비스 시작
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f
```

### 3. Airflow 웹 UI 접속

- **URL**: http://localhost:9090 (젠킨스 및 기존 서비스와 포트 충돌 방지)
- **계정**: admin / admin

## 스케줄링 설정

### 한국시간 기준으로 실행
- **기본 스케줄**: 매일 오후 11시 (KST)
- **시간대**: Asia/Seoul
- **재시도**: 실패 시 1회 재시도 (5분 간격)
- **스케줄 설정이유**: 대기오염 중금속 데이터가 당일 오후 10시에 당일 최종 데이터 호출 가능하기 때문서 설정함

### 스케줄 변경 방법

`etl/dags/air_pollution_dag.py` 파일에서 수정:

```python
# 매일 오전 9시
schedule_interval="0 9 * * *"

# 주중(월-금) 오전 9시  
schedule_interval="0 9 * * 1-5"

# 6시간마다
schedule_interval="0 */6 * * *"
```

## 수동 실행 (날짜 지정)

### 웹 UI에서 날짜 입력하여 실행

1. **DAG 페이지 접속**: `air_quality_etl_pipeline` 클릭
2. **"▶ Trigger DAG w/ Config"** 버튼 클릭
3. **Configuration JSON** 입력:

#### 특정 날짜로 실행
```json
{
  "target_date": "2025-01-15"
}
```

#### API ID도 변경하여 실행
```json
{
  "target_date": "2024-12-25",
  "api_id": "API_1"
}
```

#### 지원하는 날짜 형식
- `2025-01-15` (YYYY-MM-DD)
- `2025/01/15` (YYYY/MM/DD)
- `20250115` (YYYYMMDD)

## 데이터 플로우

```
1. 데이터 수집
   ↓ 공개데이터포털 OpenAPI 호출
   
2. 데이터 가공  
   ↓ pandas 데이터 처리
   
3. 로컬 저장
   ↓ CSV 파일로 저장
   
4. S3 업로드
   ↓ AWS S3 버킷에 업로드
   
5. 완료
```

## 📋 서버 배포 시 포트 설정

### 사용하는 포트들
- **Airflow Web UI**: 9090 (8080 젠킨스, 8090 등과 충돌 방지)
- **PostgreSQL**: 5434 (5432 기존 PostgreSQL과 충돌 방지)
- **이유**: 젠킨스 및 기존 PostgreSQL과의 포트 충돌 방지
