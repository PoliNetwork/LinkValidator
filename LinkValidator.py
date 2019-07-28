import requests


def get_db_as_json():
    url = "https://polinetwork.github.io/data/search/groups3.json"
    return requests.get(url).json()


def validate_link(link):
    return "tgme_page_title" in requests.get(link).text


data = get_db_as_json()
for p in data['info_data']:
    if not ("FB" in p) and ("TG" in p):
        pvt_link_format = "https://t.me/joinchat/"
        pvt_link_format += p.split("/")[len(p.split("/")) - 1]

        pbl_link_format = "https://t.me/"
        pbl_link_format += p.split("/")[len(p.split("/")) - 1]

        if validate_link(pvt_link_format) is False and validate_link(pbl_link_format) is False:
            class_name = data['info_data'][p]['class']
            print(f"Link of {class_name} not working anymore. You're pleased to update it. "
                  f"({pvt_link_format} or {pbl_link_format}")
