# NcatBot_py
基于[**NapCatQQ**](https://github.com/NapNeko/NapCatQQ)搓的python脚手架(~~其实也不怎么好用~~)

python小白，主要为了练手，做的不好多多批评

> 对于**NapCatQQ**推荐的[**python社区资源**](https://github.com/liyihao1110/NcatBot)

~~虽然不提倡重复做一个功能，但还是想练手，如果不可以的话请联系作者删除此项目~~

# 食用说明
~~~
支持的python版本：3.13.X（本人用的是3.13.0）
index.py       #入口文件，负责ws连接及抛出消息
msg_data.py    #消息处理文件
api_data.py    #API部分
fn.py          #消息函数部分(使用@register_command注册命令)
~~~
下载项目后按照**fn.py**示例编写消息函数，然后直接运行index.py即可
