import yaml

constants = None
with open("constants.yml", "r") as stream:
    try:
        constants = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
