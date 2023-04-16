from datetime import datetime
from pkgutil import get_data
from os import path
from yaml import safe_load, dump


class Report:

    def __init__(self, rep_type: str, pid: str, date_time: datetime, report_text: str):
        self.pid = pid
        self.date_time = date_time
        self.report_text = report_text
        self.data = self.__gen_data_dict(rep_type)

    @staticmethod
    def __gen_data_dict(rep_type: str) -> dict:

        config_path = None
        if rep_type == "echocardiogram":
            config_path = path.join("configs", "echocardiogram.yml")

        read_bytes = get_data(__name__, config_path)
        config = safe_load(read_bytes)
        data_dict = dict(config)
        for k, d in data_dict.items():
            data_dict[k] = {"metadata": d,
                            "value": None,
                            "phrase": None}

        return data_dict

    def get_pid(self) -> str:
        return self.pid

    def get_date_time(self) -> datetime:
        return self.date_time

    def get_text(self) -> str:
        return self.report_text

    def __str__(self):
        return(
            "Report -----------------------\n" 
            "ID:     {0}\n" 
            "Date:   {1}\n"
            "Report: {2}\n"
            "Data:   {3}".format(self.pid, self.date_time, self.report_text, dump(self.data))
        )
