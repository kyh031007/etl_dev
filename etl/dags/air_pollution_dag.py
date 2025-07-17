import logging
import sys
from datetime import datetime, timedelta

import pytz
from airflow import DAG
from airflow.operators.python import PythonOperator

# Docker 컨테이너 내부에서 경로 설정
sys.path.insert(0, "/opt/airflow")

# 한국 시간대 설정
KST = pytz.timezone("Asia/Seoul")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 16, tzinfo=KST),  # 한국시간으로 설정
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def run_etl_task(**context):
    """ETL 파이프라인 실행 (로깅 충돌 방지)"""

    # Airflow 로거 사용
    logger = logging.getLogger(__name__)

    try:
        # DAG 실행 시 입력받은 설정값 가져오기
        dag_config = context.get("dag_run").conf or {}

        input_date = dag_config.get("target_date")
        current_time = datetime.now(KST)
        execution_date = current_time.strftime("%Y%m%d")

        if input_date:
            # 입력받은 날짜가 있으면 사용 (YYYY-MM-DD 또는 YYYYMMDD 형식 지원)
            target_date = input_date.replace("-", "").replace("/", "")
            logger.info(f"입력받은 날짜 사용: {input_date} → {target_date}")
        else:
            # 입력받은 날짜가 없으면 execution_date 사용
            target_date = execution_date
            logger.info(f"기본 실행 날짜 사용: {target_date}")

        logger.info(f"현재 시간(KST): {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info(f"ETL 파이프라인 시작 - 처리할 날짜: {target_date}")

        import boto3
        from config import config
        from model.manager_dao import ManagerDAO
        from sqlalchemy import create_engine
        from src.data_collector import dataCollector
        from src.data_proccess import dataProccess
        from src.s3_uploader import s3Uploader

        logger.info("모듈 import 완료")

        # DB 연결
        db = create_engine(config.DB_URL)
        logger.info("DB 연결 완료")

        # 객체 생성
        managerDAO = ManagerDAO(db, logger)
        dc = dataCollector(config, logger, managerDAO)
        dp = dataProccess(config, logger, managerDAO)

        def s3_connection(managerDAO, logger):
            try:
                aws_s3_info = managerDAO.get_aws_s3_client()[0]
                aws_access_key_id = aws_s3_info.get("aws_access_key_id")
                aws_secret_access_key = aws_s3_info.get("aws_secret_access_key")
                aws_default_region = aws_s3_info.get("aws_default_region")
                s3_bucket_name = aws_s3_info.get("s3_bucket_name")

                s3 = boto3.client(
                    service_name="s3",
                    region_name=aws_default_region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                )
                logger.info("S3 연결 완료")
                return s3, s3_bucket_name
            except Exception as e:
                logger.error(f"S3 연결 실패: {str(e)}")
                raise

        # s3_connection
        s3, s3_bucket_name = s3_connection(managerDAO, logger)

        su = s3Uploader(s3, s3_bucket_name, logger, managerDAO)

        # 데이터 설정 (입력받은 날짜 또는 기본 날짜 사용)
        api_id = dag_config.get("api_id", "API_1")  # API ID도 입력받을 수 있도록
        data = {"api_id": api_id, "date": target_date}

        logger.info(f"처리할 데이터: API_ID={api_id}, DATE={target_date}")

        # api 호출하여 공개데이터포탈 csv 수집
        logger.info("1. 데이터 수집 시작")
        df = dc.collect_data_from_api(data)

        # 가공
        logger.info("2. 데이터 가공 시작")
        new_df = dp.process_df(df)

        # 가공된 데이터 저장
        logger.info("3. 가공된 데이터 저장")
        path = dc.save_df_to_csv(new_df, target_date, "processed")

        # 가공된 데이터 S3 업로드
        logger.info("4. S3 업로드 시작")
        su.upload_file(path)

        logger.info("ETL 파이프라인 완료!")

    except Exception as e:
        logger.error(f"ETL 파이프라인 실행 중 오류 발생: {str(e)}")
        raise


with DAG(
    dag_id="air_quality_etl_pipeline",
    default_args=default_args,
    description="대기오염 중금속 데이터 ETL 파이프라인",
    # 스케줄 설정 예시들 (모두 한국시간 기준):
    # schedule_interval="0 9 * * *",    # 매일 오전 9시 (KST)
    # schedule_interval="0 9 * * 1-5",  # 주중(월-금) 오전 9시 (KST)
    # schedule_interval="0 */6 * * *",  # 6시간마다 (KST)
    # schedule_interval="@daily",       # 매일 자정 (KST)
    # schedule_interval="@hourly",      # 매시간 (KST)
    schedule_interval="0 23 * * *",  # 매일 오후 11시 (한국시간) 실행
    catchup=False,
    max_active_runs=1,
    tags=["환경", "ETL", "S3", "한국시간"],
    # Web UI에서 Configuration 입력을 받기 위한 파라미터 정의
    params={"target_date": None, "api_id": "API_1"},  # 처리할 날짜 (YYYY-MM-DD 또는 YYYYMMDD)  # API ID (기본값: API_1)
) as dag:

    run_task = PythonOperator(
        task_id="run_air_quality_pipeline",
        python_callable=run_etl_task,
        provide_context=True,
    )
