<div align="center">

# Liteyuki Bot

### 基于[Nonebot](https://v2.nonebot.dev/)库和[go-cqhttp](https://docs.go-cqhttp.org/)的QQ机器人

</div>

## 简介

作者没有女朋友那段时间一个人过于寂寞，便写了这个bot来陪伴自己，顺便学习一些相关知识。使用了Nonebot库，继承了Nonebot的大部分优点，作者自己造了很多轮子和~~屎山~~。有相对简洁的插件管理功能。代码很烂，自己用的。

## 安装

- 环境：Python3.10+(3.9及以下不行的哦，因为用的3.10的语法格式)

- 依赖：requirements.txt(除此之外，报错缺啥你装啥)

- cqhttp自行下载

## 配置

启动机器人时，会默认生成配置文件data/g0.json，里面会告诉你那些配置怎么填，自己去看

发送liteyuki，若回复测试成功即安装成功

自行创建并配置.env文件

## 常见问题

#### 1.机器人不响应群聊消息

- 机器人加入群聊需要超级用户手动开启，私聊bot发送“群聊启用 <群号>”
- .env中COMMAND_START中没有""空命令前缀选项，命令需接斜杠

#### 2.bot无法注册，收不到邮箱验证码

- bot注册需要在配置中配置bot注册验证码发送的邮箱和邮箱登录码（只能用网易163邮箱，其他邮箱没有支持，你也可以改src/kami_user_manager/userApi.py的代码来实现），并且邮箱要开启POP3/SMTP/IMAP服务
- 邮箱配置无误后，若用户未收到验证码请检查垃圾邮件，90%的可能在那里面

#### 3.其他问题

- 请提交issue，我每天应该能看一两次github
- 加我qq[2238694726](http://ti.qq.com/friend/recall?uin=2238694726)

###### 程序留有一个最高主人权限，如果不想要删除README.md即可。
