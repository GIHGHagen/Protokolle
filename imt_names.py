imt_names = {
    "manns": {"name": "Sascha Manns", "protocol_title": "Protokollant"}
}


def name_lookup(name):
    return imt_names[name]["name"]

def protocol_title_lookup(name):
    return imt_names[name]["protocol_title"]