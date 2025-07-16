import logging
import os
from logging.handlers import RotatingFileHandler

import boto3
from config import config  # config.py에서 Config 인스턴스 import
from model.manager_dao import ManagerDAO
from sqlalchemy import create_engine
from src.data_collector import dataCollector
from src.data_proccess import dataProccess
from src.s3_uploader import s3Uploader


def configure_logging():
    # 로그 폴더 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 로거 설정
    logger = logging.getLogger("airflow")
    logger.setLevel(logging.INFO)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 파일 핸들러 (일반 로그)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "airflow.log"), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # 에러 파일 핸들러
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, "error.log"), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)

    # 포매터 설정 (한국시간 적용)
    from datetime import datetime

    import pytz

    class KSTFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            seoul_tz = pytz.timezone("Asia/Seoul")
            ct = datetime.fromtimestamp(record.created, seoul_tz)
            if datefmt:
                s = ct.strftime(datefmt)
            else:
                s = ct.strftime("%Y-%m-%d %H:%M:%S")
            return s

    formatter = KSTFormatter("[%(asctime)s KST] [PID: %(process)d] %(levelname)s in %(name)s: %(message)s")

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger


# 로깅 설정
logger = configure_logging()

# DB 연결
db = create_engine(config.DB_URL)


def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name=config.AWS_DEFAULT_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )
    except Exception as e:
        print(e)
    else:
        logger.info("s3 bucket connected!")
        response = s3.list_buckets()
        logger.info("Buckets:", [b["Name"] for b in response["Buckets"]])
        return s3


s3 = s3_connection()

session = boto3.Session()
creds = session.get_credentials()

bucket_name = config.S3_BUCKET_NAME

managerDAO = ManagerDAO(db, logger)

dc = dataCollector(config, logger, managerDAO)
dp = dataProccess(config, logger, managerDAO)
su = s3Uploader(s3, bucket_name, logger, managerDAO)


# 데이터 수집저장 -> 가공저장 -> S3 업로드
# data = {"api_id": "API_1", "date": "20250710"}
def run_data_pipeline(data):
    # api 호출하여 공개데이터포탈 csv 수집
    df = dc.collect_data_from_api(data)

    # 가공
    new_df = dp.process_df(df)

    # 가공된 데이터 저장
    path = dc.save_df_to_csv(new_df, "20250710", "processed")

    # 가공된 데이터 S3 업로드
    su.upload_file(path)


if __name__ == "__main__":
    data = {"api_id": "API_1", "date": "20250710"}
    run_data_pipeline(data)
