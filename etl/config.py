"""설정 관리 모듈"""

import os

# .env 파일을 로드하여 환경변수를 설정합니다.
from dotenv import load_dotenv


class Config:
    """애플리케이션 설정"""

    load_dotenv()
    # PostgreSQL 설정 (외부 DB 사용)
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_user: str = os.getenv("POSTGRES_USER", "airflow")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "airflow")
    postgres_db: str = os.getenv("POSTGRES_DB", "airflow")

    DB_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    # AWS S3 설정
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "s3-airflow-toypjt-yh")

    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "/Users/gim-yeonghwan/my_dev/etl_dev/etl/output")


# 전역 설정
config = Config()
