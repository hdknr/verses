from verses.aws import base

from ..base import filters, to_value
from .base import client, delete_tags


def remove_tags(searching: dict, exclude_ids=None, removing: dict = None):
    exclude_ids = exclude_ids or []
    res = base.describe(
        None,
        client().describe_images,
        filters=filters(searching, {}),
    )
    resources = [image.ImageId for image in res.Images if image.ImageId not in exclude_ids]
    if resources:
        return delete_tags(resources, removing)


def to_values(data, fields):
    data = dict((i, to_value(data, i)) for i in fields)
    tags = data.get("Tags", None) or []
    data["Tags"] = dict((to_value(i, "Key"), to_value(i, "Value")) for i in tags)
    return data


def find(tags, fields=None, raw=False):
    res = base.describe(
        None,
        client().describe_images,
        filters=filters(tags, {}),
        raw=raw,
    )
    if fields:
        return [to_values(i, fields) for i in to_value(res, "Images")]
    return res
