def Object(item, root="Object"):
    def _convert(item, name):
        if isinstance(item, dict):
            return type(f"_{name}", (), {k: _convert(v, k) for k, v in item.items()})

        if isinstance(item, list):

            def yield_convert(item):
                for _i, value in enumerate(item):
                    yield _convert(value, name)

            return list(yield_convert(item))
        else:
            return item

    return _convert(item, root)


def filters(*tags, **params):
    def _q(key, value):
        return {"Name": key, "Values": [value]}

    return [_q(f"tag:{key}", value) for (key, value) in tags] + [
        _q(key, value) for (key, value) in params.items()
    ]
