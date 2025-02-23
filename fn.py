from msg_data import register_command
from api_data import *




@register_command
async def 测试(*args,ctx):
    a = await Bot_Api.send_group_msg(group_id=ctx.group_id,at=ctx.user_id,text='测试拼接消息',img=f"http://q2.qlogo.cn/headimg_dl?dst_uin={ctx.user_id}&spec=5")
    print(a)


# 废弃
'''
非必要情况请不要使用合并转发md消息
只有部分功能可以渲染
而且发出来的速度很慢
并且在他发送的这段时间，还不能使用其他函数

async def md发送(*args,ctx):
    md = f"[测试](https://www.baidu.com)"
    a = await Bot_Api.send_group_md(group_id=group_id,markdown=md)
    b = a["message"]
    match = re.match(r'.*res_id(.*) 失败', b)
    id_s = match.groups()[0]
    id_s = id_s.replace("：","")
    print(id_s)
    a = await Bot_Api.send_group_forward(forward_id=id_s,group_id=ctx.group_id,text="测试")
    print(a)

'''


