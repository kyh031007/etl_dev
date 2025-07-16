import polars as pl
from polars import col

POLARS_DTYPE_MAP = {
    "float": pl.Float64,
    "int": pl.Int64,
    "str": pl.Utf8,
    "date": pl.Date,
    "datetime": pl.Datetime,
    # 필요 시 추가
}


class dataProccess:
    def __init__(self, config, logger, managerDAO):
        self.config = config
        self.logger = logger
        self.managerDAO = managerDAO

    def set_date_expr(self, col_name):
        return col(col_name).cast(pl.Utf8).str.to_datetime("%Y%m%d%H%M%S").dt.date()

    def set_time_expr(self, col_name):
        return col(col_name).cast(pl.Utf8).str.to_datetime("%Y%m%d%H%M%S").dt.time().cast(pl.Utf8).str.slice(0, 8)

    def process_df(self, df):
        try:
            df = df.cast(pl.Utf8)
            col_config = self.set_col_config(df.columns)

            expressions = []

            for new_col, cfg in col_config.items():
                func_key = cfg.get("custom_expr")
                if func_key:
                    try:
                        func = getattr(self, func_key)
                    except AttributeError:
                        raise ValueError(f"Unknown custom_expr: {func_key}")

                    expr = func(cfg.get("source_col", new_col)).alias(new_col)
                    expressions.append(expr)
                    continue

                src = cfg.get("source_col", new_col)
                expr = col(src)

                if "map" in cfg:
                    expr = expr.replace(cfg["map"])

                if "dtype" in cfg:
                    expr = expr.cast(POLARS_DTYPE_MAP[cfg["dtype"]])

                expressions.append(expr.alias(new_col))

            new_df = df.select(expressions)

            return new_df
        except Exception as e:
            self.logger.error(f"데이터 가공 실패: {e}")
            raise e

    def set_col_config(self, df_ori_col):
        try:

            col_config = {}

            for ori_col in df_ori_col:
                proc_info_list = self.select_proc_info({"api_id": "API_1", "ori_col": ori_col})
                if len(proc_info_list) > 0:
                    for proc_info in proc_info_list:

                        info = proc_info.get("info", None)
                        alias_col = info.get("alias", None)

                        if info is not None:
                            info["source_col"] = ori_col
                            col_config[alias_col] = info
                        else:
                            col_config[ori_col] = ori_col

            return col_config
        except Exception as e:
            self.logger.error(f"컬럼 가공설정 세팅 실패: {e}")
            raise e

    def select_proc_info(self, info):
        return self.managerDAO.select_proc_info(info)
