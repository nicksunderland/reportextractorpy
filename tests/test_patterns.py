import unittest
import yaml
import tests
from reportextractorpy.data_processing import DataProcessing
from glob import glob

from pkgutil import walk_packages
import importlib_resources


class TestPatterns(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_processor = DataProcessing("echocardiogram")

    def test_parse_cases_yaml(self):

        pattern_fps = glob(tests.__path__[0] + '/**/*.yml', recursive=True)

        for yml in pattern_fps:
            with open(yml) as f:
                config = yaml.safe_load(f)
                var_name = config.get("var_name")
                for i, test_details in enumerate(config.get("phrases")):
                    text = test_details.get("text")
                    value = test_details.get("value")
                    units = test_details.get("units")
                    self.data_processor.load(text, "string")
                    self.data_processor.run(0)

                    ann_lst = [ann for ann in self.data_processor.corpus[0].annset("echocardiogram")
                               if ann.type == var_name]

                    ann_value, ann_units, ann_context = None, None, None
                    number = str(i+1).ljust(2, " ")
                    if ann_lst:
                        ann = ann_lst[0]
                        ann_value = ann.features.get("value")
                        ann_units = ann.features.get("units")
                        ann_context = ann.features.get("context")

                    try:
                        if all([value, ann_value]):
                            value = round(value, 2)
                            ann_value = round(ann_value, 2)
                        self.assertEqual(value, ann_value)
                        self.assertEqual(units, ann_units)
                        print(f'\033[92m{number} - {var_name} - PASS: value[{value} {units}] = annot[{ann_value} {ann_units}], context: {ann_context}\033[0m')
                    except AssertionError:
                        print(f'\033[91m{number} - {var_name} - FAIL: value[{value} {units}] != annot[{ann_value} {ann_units}], context: {ann_context}\033[0m')


if __name__ == '__main__':
    unittest.main()
