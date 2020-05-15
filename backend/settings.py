import yaml
from os.path import abspath, dirname, join
from collections import namedtuple, OrderedDict


PROJECT_ROOT = abspath(dirname(__file__))
SETTINGS_FILE = join(PROJECT_ROOT, "settings.yml")
db = None


def create_namedtuple_from_dict(obj):
    if isinstance(obj, dict):
        fields = sorted(obj.keys())
        namedtuple_type = namedtuple(
            typename='TupleObject',
            field_names=fields,
            rename=True,
        )
        field_value_pairs = OrderedDict(
            (str(field), create_namedtuple_from_dict(obj[field]))
            for field in fields
        )
        try:
            return namedtuple_type(**field_value_pairs)
        except TypeError:
            # Cannot create_schedule namedtuple instance so fallback to dict (invalid attribute names)
            return dict(**field_value_pairs)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        return [create_namedtuple_from_dict(item) for item in obj]
    else:
        return obj


def parse():
    """
    Parse each key from the setting.yml file into a namedtuple global variable
    """
    with open(SETTINGS_FILE, 'r', encoding='utf-8-sig') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(
                "The configuration file does not respect the YAML format"
            )
            raise e

    for k, v in config.items():
        globals()[k] = create_namedtuple_from_dict(v)

