import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xml_data = ET.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'image':
        return ImageMsg(xml_data)
    elif msg_type == 'event':
        event_type = xml_data.find('Event').text
        if event_type == 'CLICK':
            return Click(xml_data)
        elif event_type == 'SCAN':
            return Scan(xml_data)
        return EventMsg(xml_data)
        # elif event_type in ('subscribe', 'unsubscribe'):
        #     return Subscribe(xmlData)
        # elif event_type == 'VIEW':
        #     return View(xmlData)
        # elif event_type == 'LOCATION':
        #     return LocationEvent(xmlData)


class Msg(object):

    def __init__(self, xml_data):
        self.xml_data = xml_data
        print(xml_data)
        self.ToUserName = xml_data.find('ToUserName').text
        self.FromUserName = xml_data.find('FromUserName').text
        self.CreateTime = xml_data.find('CreateTime').text
        self.MsgType = xml_data.find('MsgType').text
        # self.MsgId = xmlData.find('MsgId').textclass

    def find(self, key):
        return self.xml_data.find(key).text


class TextMsg(Msg):

    def __init__(self, xml_data):
        super(TextMsg, self).__init__(xml_data)
        self.Content = xml_data.find('Content').text.encode("utf-8")


class ImageMsg(Msg):

    def __init__(self, xml_data):
        super(ImageMsg, self).__init__(xml_data)
        self.PicUrl = xml_data.find('PicUrl').text
        self.MediaId = xml_data.find('MediaId').text


class EventMsg(Msg):

    def __init__(self, xml_data):
        super(EventMsg, self).__init__(xml_data)
        self.Event = xml_data.find('Event').text


class Click(EventMsg):
    def __init__(self, xml_data):
        super(Click, self).__init__(xml_data)
        self.EventKey = xml_data.find('EventKey').text


class Scan(EventMsg):
    def __init__(self, xml_data):
        super(Scan, self).__init__(xml_data)
        self.EventKey = xml_data.find('EventKey').text
