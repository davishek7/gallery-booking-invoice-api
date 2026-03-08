def mongo_to_dict(doc: dict) -> dict:
    if not doc:
        return doc

    doc = dict(doc)  # avoid mutating original
    doc["id"] = str(doc.pop("_id"))
    return doc
