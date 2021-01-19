import requests

from extensions.wx.token_manager import TokenManager


class Menu(object):

    @staticmethod
    def create(post_data, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        if isinstance(post_data, str):
            post_data = post_data.encode('utf-8')
        url_resp = requests.post(url=post_url, data=post_data)
        print(url_resp.text)

    @staticmethod
    def query(access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % access_token
        url_resp = requests.get(url=post_url)
        print(url_resp.text)

    @staticmethod
    def delete(access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % access_token
        url_resp = requests.delete(url=post_url)
        print(url_resp.text)

    # 获取自定义菜单配置接口
    @staticmethod
    def get_current_self_menu_info(access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % access_token
        url_resp = requests.get(url=post_url)
        print(url_resp.text)


if __name__ == '__main__':
    postJson = """
        {
            "button":
            [
                {
                    "name": "",
                    "sub_button":
                    [
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        }
                    ]
                },
                {
                    "name": "能力测试",
                    "sub_button":
                    [
                        {
                            "type": "click",
                            "name": "👉点击测试👈",
                            "key": "clickTest"
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "click",
                            "name": "",
                            "key": "mpGuide"
                        }

                    ]
                },
                {
                    "name": "关于我们",
                    "sub_button":
                    [
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "view",
                            "name": "",
                            "url": ""
                        },
                        {
                            "type": "click",
                            "name": "联系我们",
                            "key": ""
                        },
                        {
                            "type": "click",
                            "name": "加入我们",
                            "key": ""
                        }
                    ]
                }
            ]
        }
        """
    accessToken = TokenManager().get_wechat_token_from_db()
    # myMenu.delete(accessToken)
    Menu.create(postJson, accessToken)
    # myMenu.get_current_self_menu_info(accessToken)
