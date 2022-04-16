import json

from fastapi.encoders import jsonable_encoder


def message(params):
    print(json.dumps(jsonable_encoder(params), ensure_ascii=False))
