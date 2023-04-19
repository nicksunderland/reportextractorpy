from os import path
from yaml import safe_load
import glob
import importlib_resources
from pkgutil import walk_packages
import reportextractorpy.nlp_resources.annotation_patterns


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
    def pattern_modules_list(mode: str) -> list:
        try:
            if mode == "echocardiogram":
                phase_file = path.join(Utils.nlp_resources_path(), "annotation_patterns", mode, mode + "_phase_list.yml")
            else:
                # TODO: add cardiac MRI and other modes
                raise ValueError("Incorrect mode: [str] option passed to Utils.pattern_modules_list()")

            # Find all pattern modules in the package
            all_pattern_modules = []
            for _, name, is_pkg in walk_packages(reportextractorpy.nlp_resources.annotation_patterns.__path__,
                                                 reportextractorpy.nlp_resources.annotation_patterns.__name__ + "."):
                if not is_pkg:
                    all_pattern_modules.append(name)

            # Read from the pattern config file
            with open(phase_file) as f:
                phase_config = safe_load(f)
                phase_modules = [".".join([reportextractorpy.nlp_resources.annotation_patterns.__name__, module])
                                 for phase_section, phase_modules in phase_config["phases"].items()
                                 if phase_modules is not None
                                 for module in phase_modules]

            # Check that all the specified pattern modules actually exist in the package
            not_found_modules = [mod for mod in phase_modules if mod not in all_pattern_modules]
            print(not_found_modules)
            if len(not_found_modules) > 0:
                raise ModuleNotFoundError("""
                    One or more pattern modules not found.
                    Config file: {0}
                    Phase modules not found {1}:
                """.format(phase_file,  not_found_modules))

        except (ModuleNotFoundError, ValueError) as e:
            print(e)
            # TODO: add a warning for if there is a package pattern module for the mode that isn't used

        return phase_modules
