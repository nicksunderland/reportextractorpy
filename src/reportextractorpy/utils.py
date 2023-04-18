from os import path
from yaml import safe_load
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
    def gazetteer_config_files(mode: str) -> list:
        if mode == "echocardiogram":
            gaz_glob_pattern = path.join(Utils.nlp_resources_path(), "gazetteers", mode, "**", "*.yml")
            return glob.glob(gaz_glob_pattern, recursive=True)
        else:
            print("error in gazetteer_config_files(mode: str) -> list:")
            exit()

    @staticmethod
    def pattern_config_files(mode: str) -> list:
        if mode == "echocardiogram":
            phase_file = path.join(Utils.nlp_resources_path(),
                                   "annotation_patterns",
                                   mode,
                                   mode + "_phase_list.yml")
            with open(phase_file) as f:
                phase_config = safe_load(f)
                print(phase_config)
                phase_paths = [path.join(Utils.nlp_resources_path(), "annotation_patterns", fp)
                               for phase_section, path_list in phase_config["phases"].items()
                               if path_list is not None
                               for fp in path_list]
                return phase_paths

        else:
            print("error in pattern_config_files(mode: str) -> list:")
            exit()
