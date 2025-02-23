import re


command_handlers = {}

def register_command(func):
    """跨模块注册装饰器"""
    command_handlers[func.__name__] = func
    return func

class ctr:
    def __init__(self,raw):
        self.group_id = raw['group_id']
        self.user_id = raw['user_id']
        self.text = raw['message'][0]['data']['text']

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