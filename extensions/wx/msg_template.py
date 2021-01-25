

def init_template(open_id, template_id, data, url=None, mp_app_id=None, mp_page_path=None):
    miniprogram = {
        "appid": mp_app_id,
        "pagepath": mp_page_path,
    } if mp_app_id else None

    return {
           "touser": open_id,
           "template_id": template_id,
           "url": url or None,
           "miniprogram": miniprogram,
           "data": data,
       }


