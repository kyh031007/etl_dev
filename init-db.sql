create table public.api_info
(
    api_id    varchar(255)                              not null
        primary key,
    api_url   varchar(255)                              not null,
    api_name  varchar(255)                              not null,
    actv_yn   varchar(2) default 'Y'::character varying not null,
    created_at timestamp  default now()
);

alter table public.api_info
    owner to airflow;

create table public.api_request_params
(
    api_id         varchar(255)                              not null,
    req_params     varchar(255)                              not null,
    req_params_kor varchar(255)                              not null,
    actv_yn        varchar(2) default 'Y'::character varying not null,
    created_at     timestamp  default now()
);

alter table public.api_request_params
    owner to airflow;

create table public.params_value
(
    api_id     varchar(255) not null,
    req_params varchar(255) not null,
    value      varchar(255),
    value_kor  varchar(255),
    actv_yn    varchar(2) default 'Y'::character varying,
    created_at timestamp  default now()
);

alter table public.params_value
    owner to airflow;

create table public.proc_info
(
    api_id     varchar(255) not null,
    ori_col    varchar(255) not null,
    info       json,
    created_at timestamp default now()
);

alter table public.proc_info
    owner to airflow;



INSERT INTO public.api_info (api_id, api_url, api_name, actv_yn, created_at) VALUES ('API_1', 'http://apis.data.go.kr/1480523/MetalMeasuringResultService/MetalService', '환경부 국립환경과학원_미세먼지(금속성분) 실시간 정보', 'Y', '2025-07-16 10:32:22.341323');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'numOfRows', '페이지 크기', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'pageNo', '페이지 번호', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'serviceKey', '서비스 키', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'resultType', '결과형식', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'date', '검색조건 날짜', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '검색조건 대기환경연구소 코드', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '검색조건 항목코드', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.api_request_params (api_id, req_params, req_params_kor, actv_yn, created_at) VALUES ('API_1', 'timecode', '검색조건 시간구분', 'Y', '2025-07-16 10:34:40.035583');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'resultType', 'XML', 'XML', 'Y', '2025-07-16 11:38:48.810937');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'pageNo', '1', '1', 'Y', '2025-07-16 11:38:48.844341');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '1', '수도권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '2', '백령도', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '3', '호남권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '4', '중부권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '5', '제주도', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '6', '영남권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '7', '경기권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '8', '충청권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '9', '전북권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '10', '강원권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'stationcode', '11', '충북권', 'Y', '2025-07-16 11:38:48.859372');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90303', '납', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90304', '니켈', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90305', '망간', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90314', '아연', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90319', '칼슘', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90318', '칼륨', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'itemcode', '90325', '황', 'Y', '2025-07-16 11:38:48.868513');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'serviceKey', 'IYsD28DLAMecMtEqrYo0zoFaYsFM4wrtJ6eP9zbDox7txQGhUSaaV0mfHlo2Y50iwq5iHXQid91qB34h+BHt9Q==', '인증키', 'Y', '2025-07-16 11:38:48.823103');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'date', '20250710', '날짜', 'Y', '2025-07-16 11:38:48.851246');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'numOfRows', '12', '10', 'Y', '2025-07-16 11:38:48.835756');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'timecode', 'RH24', '24시간이동평균', 'N', '2025-07-16 11:38:48.875894');
INSERT INTO public.params_value (api_id, req_params, value, value_kor, actv_yn, created_at) VALUES ('API_1', 'timecode', 'RH02', '2시간이동평균', 'Y', '2025-07-16 11:38:48.875000');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'stationcode', e'{
  "alias": "지역명",
  "map": {
    "1": "수도권",
    "2": "백령도",
    "3": "호남권",
    "4": "중부권",
    "5": "제주도",
    "6": "영남권",
    "7": "경기권",
    "8": "충청권",
    "9": "전북권",
    "10": "강원권",
    "11": "충북권"
  }
}', '2025-07-16 14:18:05.860170');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'itemcode', e'{
  "alias": "항목명",
  "map": {
    "90303": "납",
    "90304": "니켈",
    "90305": "망간",
    "90314": "아연",
    "90319": "칼슘",
    "90318": "칼륨",
    "90325": "황"
  }
}', '2025-07-16 14:18:05.860170');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'timecode', e'{
  "alias": "시간구분",
  "map": {
    "RH02": "2시간이동평균",
    "RH24": "24시간이동평균"
  }
}', '2025-07-16 14:18:05.860170');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'sdate', e'{
  "alias": "측정시간",
  "custom_expr": "set_time_expr"
}', '2025-07-16 14:18:05.860170');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'sdate', e'{
  "alias": "측정날짜",
  "custom_expr": "set_date_expr"
}', '2025-07-16 14:18:05.860170');
INSERT INTO public.proc_info (api_id, ori_col, info, created_at) VALUES ('API_1', 'value', e'{
  "alias": "측정수치(ng/m3)",
  "dtype": "float"
}', '2025-07-16 14:18:05.860170');


create table aws_s3_info(
    aws_access_key_id varchar(1000) not null ,
    aws_secret_access_key varchar(1000) not null ,
    aws_default_region varchar(255) not null ,
    s3_bucket_name varchar(255) not null
);


insert into public.aws_s3_info(aws_access_key_id, aws_secret_access_key, aws_default_region, s3_bucket_name)
values ('your_access_key_id','your_secret_access_key','your_default_region','your_bucket_name')