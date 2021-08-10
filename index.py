# -*- encoding: utf-8 -*-
import action

infos = {
    "cookie": '''cookie值''',
    "token" : "",
    "p00001" : "",
    "phone": "",
    "password": ""
}


def main_handler(event, context):
    action.main(infos)


if __name__ == "__main__":
    main_handler("", "")