from typing import Dict, Optional

from sqlalchemy import text


class ManagerDAO:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def select_api_info(self, info=None):

        api_id = info.get("api_id", None)

        sql = """
            SELECT api_id, api_url, api_name
            FROM api_info 
            WHERE actv_yn = 'Y'
        """
        if api_id is not None:
            sql += " AND api_id = :api_id"

        payload = {"api_id": api_id}

        with self.db.connect() as connection:
            result = connection.execute(text(sql), payload)
            result_set = [dict(row) for row in result]

            return result_set

    def select_req_params(self, info):
        api_id = info.get("api_id", None)

        sql = """
            SELECT api_id, req_params from api_request_params
            WHERE api_id = :api_id and actv_yn = 'Y'
        """

        payload = {
            "api_id": api_id,
        }

        with self.db.connect() as connection:
            result = connection.execute(text(sql), payload)
            result_set = [dict(row) for row in result]

            return result_set

    def select_params_value(self, info):
        api_id = info.get("api_id", None)
        req_params = info.get("req_params", None)

        sql = """
            SELECT api_id, req_params, value from params_value
            WHERE api_id = :api_id and actv_yn = 'Y' and req_params = :req_params
        """

        payload = {
            "api_id": api_id,
            "req_params": req_params,
        }

        with self.db.connect() as connection:
            result = connection.execute(text(sql), payload)
            result_set = [dict(row) for row in result]

            return result_set

    def select_proc_info(self, info):
        api_id = info.get("api_id", None)
        ori_col = info.get("ori_col", None)

        sql = """
            SELECT api_id, ori_col, info from proc_info
            WHERE api_id = :api_id and ori_col = :ori_col
        """

        payload = {"api_id": api_id, "ori_col": ori_col}

        with self.db.connect() as connection:
            result = connection.execute(text(sql), payload)
            result_set = [dict(row) for row in result]

            return result_set
