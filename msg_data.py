import re


command_handlers = {}

def register_command(func):
    """跨模块注册装饰器"""
    command_handlers[func.__name__] = func
    return func

class ctr:
    def __init__(self,raw):
        self.self_id = raw['self_id']
        self.user_id = raw['user_id']
        self.time = raw['time']
        self.message_id = raw['message_id']
        self.message_seq = raw['message_seq']
        self.real_id = raw['real_id']
        self.message_type = raw['message_type']
        if self.message_type != 'group':
            self.target_id = raw['target_id']
        else:
            self.target_id = None
        self.sender = raw['sender']
        self.sender_user_id = self.sender['user_id']
        self.sender_nickname = self.sender['nickname']
        self.sender_card = self.sender['card']
        if self.message_type == 'group':
            self.sender_role = self.sender['role']
            self.group_id = raw['group_id']
        else:
            self.sender_role = None
            self.group_id = None
        self.raw_message = raw['raw_message']
        self.font = raw['font']
        self.sub_type = raw['sub_type']
        self.message = ['message']
        self.message_forma = ['message_forma']
        self.post_type = raw['post_type']


async def messages(raw_message):
    """消息处理入口"""
    print(raw_message)
    try:
        ctx = ctr(raw_message)
        # 分割命令和参数
        text = raw_message['message'][0]['data']['text']
        match = re.match(r'(\w+)(.*)', text)
        if match:
            cmd, rest = match.groups()
            args = [arg for arg in rest.split(rest[0]) if arg] if rest else []
        # 获取对应处理器
        handler = command_handlers.get(cmd)
        
        if handler:
            # 传递参数和上下文信息
            await handler(*args,ctx=ctx)
        else:
            pass
            
    except KeyError as e:
        pass
    except Exception as e:
        print(f"消息处理异常: {e}")
