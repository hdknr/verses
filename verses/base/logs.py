import json


def message(params):
    print(json.dumps(params, ensure_ascii=False))
