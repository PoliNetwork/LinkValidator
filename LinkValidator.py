import requests


def get_db_as_json():
    url = "https://polinetwork.github.io/data/search/groups3.json"
    return requests.get(url).json()


def validate_link(link):
    return "tgme_page_title" in requests.get(link).text


def main(yearSelected):
    separator = ' |-| '

    count_items = 0
    data = get_db_as_json()
    for p in data['info_data']:
        if not ("FB" in p) and ("TG" in p):

            year = data['info_data'][p]['year']
            if year is None or year == "" or year == yearSelected:
                pvt_link_format = "https://t.me/joinchat/"
                pvt_link_format += p.split("/")[len(p.split("/")) - 1]

                pbl_link_format = "https://t.me/"
                pbl_link_format += p.split("/")[len(p.split("/")) - 1]

                if validate_link(pvt_link_format) is False and validate_link(pbl_link_format) is False:
                    class_name = data['info_data'][p]['class']
                    print(f"{class_name}{separator}{pvt_link_format}{separator}{pbl_link_format}{separator}{year}")
                    count_items = count_items + 1

    print("Total " + str(count_items))


main("2019/2020")
