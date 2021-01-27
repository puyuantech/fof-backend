import time


class Msg(object):

    def results(self):
        return "success"


class TextMsg(Msg):

    def __init__(self, to_user_name, from_user_name, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_user_name
        self.__dict['FromUserName'] = from_user_name
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def results(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        # print(XmlForm)
        return xml_form.format(**self.__dict)


class ImageMsg(Msg):
    def __init__(self, to_user_name, from_user_name, media_id):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_user_name
        self.__dict['FromUserName'] = from_user_name
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = media_id

    def results(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return xml_form.format(**self.__dict)


class News(Msg):
    def __init__(self, to_user_name, from_user_name, title, description, pic_url, url):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_user_name
        self.__dict['FromUserName'] = from_user_name
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Title'] = title
        self.__dict['Description'] = description
        self.__dict['PicUrl'] = pic_url
        self.__dict['Url'] = url

    def results(self):
        xml_form = """
        <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
                <item>
                    <Title><![CDATA[{Title}]]></Title>
                    <Description><![CDATA[{Description}]]></Description>
                    <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
                    <Url><![CDATA[{Url}]]></Url>
                </item>
            </Articles>
        </xml>
        """
        return xml_form.format(**self.__dict)

