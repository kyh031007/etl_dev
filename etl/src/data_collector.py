import os
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

import polars as pl
import requests


def fetch_one(idx, url, params, logger):
    while True:
        try:
            logger.info(f"{idx}번째 파라미터 호출 시작")

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            if "<OpenAPI_ServiceResponse>" in response.text:
                logger.warning(f"{idx}번째 호출: HTTP ROUTING ERROR 감지 → 1초 후 재시도")
                time.sleep(1)
                continue

            xml_str = ET.fromstring(response.text)

            # No Data: 정상 응답 but list/item 없음
            total_count = xml_str.findtext(".//totalCount")
            if total_count == "0":
                logger.info(f"{idx}번째 호출: 정상 응답, 데이터 없음 → 패스")
                return []

            items = xml_str.find(".//items") or xml_str.find(".//list")  # API에 따라
            if items is None:
                logger.warning(f"{idx}번째 호출 결과에 items 없음 → 재시도")
                time.sleep(1)
                continue

            item_list = items.findall("item")
            if not item_list:
                logger.info(f"{idx}번째 호출 결과에 item 없음 → 패스")
                return []

            records = []
            for item in item_list:
                record = {child.tag: child.text for child in item}
                records.append(record)

            logger.info(f"{idx}번째 파라미터 호출 성공, {len(records)}개")
            return records

        except Exception as e:
            logger.error(f"{idx}번째 호출 실패: {e} → 1초 후 재시도")
            time.sleep(1)


# 사용자 로직
class dataCollector:
    def __init__(self, config, logger, managerDAO):
        self.config = config
        self.logger = logger
        self.managerDAO = managerDAO

    def select_api_info(self, info):
        return self.managerDAO.select_api_info(info)

    def select_req_params(self, info):
        return self.managerDAO.select_req_params(info)

    def select_params_value(self, info):
        return self.managerDAO.select_params_value(info)

    def collect_data_from_api(self, info):
        try:
            api_id = info.get("api_id", "API_1")

            api_info = self.select_api_info({"api_id": api_id})[0]

            set_req_params = self.select_req_params(info)

            date = [info.get("date", "20250710")]

            params_value_list = {}
            for req_param in set_req_params:
                params_info = {
                    "api_id": api_id,
                    "req_params": req_param["req_params"],
                }
                if req_param["req_params"] == "date":
                    params_value_list[req_param["req_params"]] = date
                else:
                    params_value_list[req_param["req_params"]] = self.make_params_value_list(params_info)

            url = api_info.get("api_url", None)
            params_list = self.set_params_value(params_value_list)

            df = self.make_df_parallel(url, params_list)
            path = self.save_df_to_csv(df, date[0], "collect")

            return df
        except Exception as e:
            self.logger.error(f"데이터 수집 실패: {e}")
            raise e

    def make_params_value_list(self, params_info):

        params_value_list = self.select_params_value(params_info)

        value_list = []
        for params in params_value_list:
            value_list.append(params["value"])
        return value_list

    def set_params_value(self, params_value_list):
        """
        params_value_list는 다음과 같은 형태로 들어옴:
        {
            'numOfRows': ['10'],
            'pageNo': ['1'],
            'serviceKey': ['서비스키'],
            'resultType': ['XML'],
            'date': ['20231120'],
            'stationcode': ['1', '2', ...],
            'itemcode': ['90303', ...],
            'timecode': ['RH02', 'RH24']
        }
        stationcode, itemcode, timecode의 모든 조합별로 한 번씩 호출할 수 있도록
        params 딕셔너리 리스트를 반환
        """
        import itertools

        # 단일 값 파라미터 추출
        base_params = {}
        for key in ["numOfRows", "pageNo", "serviceKey", "resultType", "date"]:
            value = params_value_list.get(key)
            if value and len(value) > 0:
                base_params[key] = value
            else:
                base_params[key] = None

        # 조합이 필요한 파라미터
        stationcodes = params_value_list.get("stationcode", [])
        itemcodes = params_value_list.get("itemcode", [])
        timecodes = params_value_list.get("timecode", [])

        # stationcode, itemcode, timecode의 모든 조합 생성
        params_list = []
        for stationcode, itemcode, timecode in itertools.product(stationcodes, itemcodes, timecodes):
            params = base_params.copy()
            params["stationcode"] = stationcode
            params["itemcode"] = itemcode
            params["timecode"] = timecode
            params_list.append(params)

        # params_list의 각 원소는 실제 API 호출에 사용될 파라미터 딕셔너리
        self.logger.info(f"총 {len(params_list)}개의 파라미터 조합 생성 완료")
        return params_list

    # 파라미터 조합별로 병렬 호출(데이터프레임 생성)
    def make_df_parallel(self, url, params_list, max_workers=5):
        try:
            all_records = []

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(fetch_one, idx, url, params, self.logger) for idx, params in enumerate(params_list)
                ]

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        all_records.extend(result)

            df = pl.DataFrame(all_records)

            if "value" in df.columns:
                df = df.with_columns(pl.col("value").cast(pl.Float64))

                return df
        except Exception as e:
            self.logger.error(f"데이터 프레임 생성 실패: {e}")
            raise e

    # 원본 데이터 저장
    def save_df_to_csv(self, df, date, status):
        try:
            # DataFrame이 비어있지 않으면 pl.DataFrame으로 csv 저장
            if df.height > 0:
                output_dir = self.config.OUTPUT_DIR
                # date 값이 20250710이면 202507로 폴더 생성
                subfolder = str(date)[:6]
                output_dir = os.path.join(output_dir, subfolder)

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_path = os.path.join(output_dir, f"{date}_{status}.csv")
                df.write_csv(output_path)
                self.logger.info(f"{status} 데이터를 CSV로 저장했습니다: {output_path}")
                return output_path
            else:
                self.logger.warning(f"{status} 데이터가 없어 CSV로 저장하지 않습니다.")
        except Exception as e:
            self.logger.error(f"데이터 저장 실패: {e}")
            raise e
