import os


class s3Uploader:
    def __init__(self, s3, bucket_name, logger, managerDAO):
        self.s3 = s3
        self.bucket_name = bucket_name
        self.logger = logger
        self.managerDAO = managerDAO

    # 파일 업로드
    def upload_file(self, file_path):
        try:

            subfolder = os.path.basename(os.path.dirname(file_path))  # '202507'
            filename = os.path.basename(file_path)  # '20250710_result.csv'
            s3_path = f"{subfolder}/{filename}"
            self.s3.upload_file(file_path, self.bucket_name, s3_path)
            self.logger.info(f"S3에 파일 업로드 완료: {s3_path}")
            # self.delete_local_file(file_path)
            # self.logger.info(f"로컬 파일 삭제 완료: {file_path}")
        except Exception as e:
            self.logger.error(f"파일 업로드 실패: {e}")

    def delete_local_file(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.info(f"로컬 파일 삭제 완료: {file_path}")
            else:
                self.logger.warning(f"로컬 파일이 존재하지 않아 삭제하지 않음: {file_path}")
        except Exception as e:
            self.logger.error(f"로컬 파일 삭제 실패: {e}")
