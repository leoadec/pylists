from textwrap import wrap

def wrap_text(text: str, prefix: str):
    if len(prefix) > 76:
        raise BaseException("Prefix too long.")
    padding = " " * len(prefix)
    return_string = ""
    for item in text.splitlines():
        wrapped_item = wrap(item, width=80-len(prefix))
        return_string += f"{prefix}{wrapped_item[0]}\n"
        for line in wrapped_item[1:]:
            return_string += f"{padding}{line}\n"
    return return_string[:-1]
