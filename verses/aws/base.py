from botocore.exceptions import ClientError


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


def to_value(source, field):
    if isinstance(source, dict):
        return source.get(field, None)
    return getattr(source, field, None)


def filters(tags: dict, params: dict):
    def _q(key, value):
        return {"Name": key, "Values": [value]}

    # tags: OR filter
    return [_q(f"tag:{key}", value) for (key, value) in tags.items()] + [
        _q(key, value) for (key, value) in params.items()
    ]


def args_filters(tag_list, params):
    return filters(keyvalues(tag_list), params)


def keyvalue_list(args):
    return [tuple(i.split("=")) for i in args if i.find("=") >= 0]


def keyvalues(args, extra=None):
    if extra:
        return {**dict(keyvalue_list(args)), **extra}
    return dict(keyvalue_list(args))


def to_tags(keyvalues: dict):
    return [{"Key": key, "Value": value} for key, value in keyvalues.items()]


def tag_specs(keyvalues, resource_type=None):
    rt = {"ResourceType": resource_type} if resource_type else {}
    return [
        {
            "Tags": to_tags(keyvalues),
            **rt,
        }
    ]


def call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except ClientError as e:
        if "DryRunOperation" == e.response["Error"]["Code"]:
            return e.response
        raise e


def describe(cls, func, filters=None, raw=False):
    """
    describe function call
    """
    q = filters and dict(Filters=filters) or {}
    res = func(**q)
    return res if raw else Object(res)
