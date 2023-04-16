from os import path
import glob
import importlib_resources


class Utils:

    @staticmethod
    def configs_path() -> str:
        return str(importlib_resources.files("reportextractorpy").joinpath("configs"))

    @staticmethod
    def nlp_resources_path() -> str:
        return str(importlib_resources.files("reportextractorpy").joinpath("nlp_resources"))

    @staticmethod
    def gazetteer_config_files() -> list:
        gaz_glob_pattern = path.join(Utils.nlp_resources_path(), "gazetteers", "**", "*.yml")
        return glob.glob(gaz_glob_pattern, recursive=True)
