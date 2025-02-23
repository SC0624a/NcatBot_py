import json
import aiohttp
import asyncio

api_url = 'http://127.0.0.1:3000'

class Bot_api:
    def __init__(self):
        self.message = []
        self.content = []

    async def get(self,url):
        async with aiohttp.ClientSession() as fw:
            try:
                data = await fw.get(f'{api_url}{url}')
                return await data.text()
            except:
                pass

    async def post(self,url,data=None,json=None):
        async with aiohttp.ClientSession() as fw:
            try:
                data = await fw.get(f'{api_url}{url}',data=data, json=json)
                return await data.text()
            except:
                pass

    async def func(self,func_name,*args):
        try:
            a = await Bot_api.__dict__[func_name](self,*args)
            return a
        except KeyError as e:
            return Bot_api.__dict__

    #发送群消息（拼接版）
    async def send_group_msg(self,**kwargs):
        '''
        发送拼接群消息\n
        传入示例：func_name=data，at='123456',text='文本'，按照传入的func_name顺序发送
        :param kwargs:
        :return: dict|str
        '''
        if 'group_id' not in kwargs:
            return {'code':'-1','msg':'缺少必要的形参"group_id"'}
        if len(kwargs) == 1:
            return {'code':'-2','msg':'至少传递两个形参'}
        group_id = kwargs['group_id']
        for key in kwargs:
            func_1 = f'add_{key}'
            await self.func(func_1,f'{kwargs[key]}')
        body = {
            "group_id":f"{group_id}",
            "message":self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg', data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送群文本
    async def send_group_text(self,group_id,text):
        '''
        发送群文本
        :param group_id: 群号
        :param text: 内容
        :return: dict|str
        '''
        await self.add_text(f'{text}')
        body = {
    "group_id": f"{group_id}",
    "message": self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg',data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送群at
    async def send_group_at(self,group_id: int,at_qq: int):
        '''
        发送群at\n
        此为纯at无携带文本
        :param group_id: 群号
        :param qq: 被at人（all为全体成员）
        :param text: 内容
        :return: dict|str
        '''
        await self.add_at(at_qq)
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg', data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送群图片
    async def send_group_img(self,group_id: int,img: str):
        '''
        发送群图片
        :param group_id: 群号
        :param img: 本地：file://D:/a.jpg，网络：http://xxxx，base64：base64://xxxx
        :return:dict|str
        '''
        await self.add_img(img)
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg', data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送群表情
    async def send_group_face(self,group_id: int,face: int):
        '''
        发送群表情
        :param group_id: 群号
        :param face: https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#EmojiType
        :return: dict|str
        '''
        await self.add_face(f'{face}')
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg', data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送群卡片
    async def send_group_json_card(self,group_id: int,json_card: dict|str):
        '''
        发送群卡片
        :param group_id: 群号
        :param json_card: 卡片带{}
        :return: dict|str
        '''
        await self.add_json_card(f'{json_card}')
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        body = json.dumps(body)
        a = await self.post('/send_group_msg', data=body)
        a = json.loads(a)
        self.message = []
        return a

    #发送合并聊天记录
    async def send_group_forward(self,forward_id=None,**kwargs):
        if 'group_id' not in kwargs:
            return {'code':'-1','msg':'缺少必要的形参"group_id"'}
        if len(kwargs) == 1:
            return {'code':'-2','msg':'至少传递两个形参'}
        group_id = kwargs['group_id']
        for key in kwargs:
            func_1 = f'add_forward_{key}'
            await self.func(func_1,f'{kwargs[key]}')
        if forward_id is None:
            message = await self.add_forward()
        else:
            message = await self.add_forward(forward_id)
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        #body = json.dumps(body)
        a = await self.post('/send_group_forward_msg', json=body)
        a = json.loads(a)
        self.message = []
        self.content = []
        return a
        
        #发送md消息
    async def send_group_md(self,group_id: int,markdown: str):
        '''
        :param group_id: 群号
        :param markdown: md格式的文本
        :return: dict|str
        '''
        await self.add_md(markdown)
        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        #body = json.dumps(body)
        a = await self.post('/send_group_forward_msg', json=body)
        a = json.loads(a)
        self.message = []
        return a

    async def send_constructed_msg(self, group_id):
        """发送已构造的消息"""
        if not self.message:
            return {'code': -3, 'msg': '消息内容为空'}

        body = {
            "group_id": f"{group_id}",
            "message": self.message
        }
        a = await self.post('/send_group_msg', data=json.dumps(body))
        a = json.loads(a)
        self.message = []
        return a

    async def add_text(self,text):
        self.message.append({
            "type": "text",
            "data": {
                "text": f"{text}"
            }})
        return self

    async def add_forward_text(self,text):
        self.content.append({
            "type": "text",
            "data": {
                "text": f"{text}"
            }})
        return self

    async def add_at(self,qq):
        '''
        :param qq: 被at人 all为全体成员
        :return: self
        '''
        self.message.append({
            "type": "at",
            "data": {
                "qq": f"{qq}",
            }})
        await self.add_text(' ')
        return self

    async def add_forward_at(self,qq):
        '''
        :param qq: 被at人 all为全体成员
        :return: self
        '''
        self.content.append({
            "type": "at",
            "data": {
                "qq": f"{qq}",
            }})
        await self.add_forward_text(' ')
        return self

    async def add_img(self,file):
        '''
        :param file:
                本地file://D:\\a.jpg
                网络http://XXX
                base64编码base64://xxxxxxxx
        :return:
        '''
        self.message.append({
            "type": "image",
            "data": {
                "file": f"{file}"
            }
        })
        return self

    async def add_forward_img(self,file):
        '''
        :param file:
                本地file://D:\\a.jpg
                网络http://XXX
                base64编码base64://xxxxxxxx
        :return:
        '''
        self.content.append({
            "type": "image",
            "data": {
                "file": f"{file}"
            }
        })
        return self


    async def add_face(self,face_id):
        self.message.append({
            "type": "face",
            "data": {
                "id": face_id
            }
        })
        return self

    async def add_forward_face(self,face_id):
        self.content.append({
            "type": "face",
            "data": {
                "id": face_id
            }
        })
        return self

    async def add_json_card(self,json):
        self.message.append({
            "type": "json",
            "data": {
                "data": f"{json}"
            }
        })
        return self
        
    async def add_md(self,md):
        self.message.append(
            {
                "type": "node",
                "data": {
                    "nickname": "qwq",
                    "user_id": "114514",
                    "content": [
                        {
                            "type": "markdown",
                            "data": {
                                "content": f"{md}"
                            }
                        }
                    ]
                }
            }
        )
        return self

    async def add_forward(self,forward_id=None):
        if forward_id is None:
            self.message.append(
                {
                    "type": "node",
                    "data": {
                        "nickname": "qwq",
                        "user_id": "114514",
                        "content": self.content
                    }
                }
            )
        else:
            self.message.append(
                {
                    "type": "node",
                    "data": {
                        "nickname": "qwq",
                        "user_id": "114514",
                        "content": [
                            {
                                "type": "forward",
                                "data": {
                                    "id": f"{forward_id}"
                                }
                            }
                        ]
                    }
                }
            )
        return self


Bot_Api = Bot_api()
