import asyncio
import random

import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN, Message
from nonebot.permission import SUPERUSER

from ...extraApi.permission import MASTER
from ...extraApi.rule import plugin_enable
from .stApi import *

#    ahhaha
setConfig = on_command(cmd="设置属性", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
getConfig = on_command(cmd="获取属性", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
send_mutil_msg = on_command(cmd="群发消息", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
backup_data = on_command(cmd="备份数据", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
statistics_data = on_command(cmd='统计数据', rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
enable_group = on_command(cmd="群聊启用", rule=plugin_enable("kami.super_tool", False), permission=SUPERUSER | MASTER, priority=10, block=True)
disable_group = on_command(cmd="群聊停用", rule=plugin_enable("kami.super_tool", False), permission=SUPERUSER | MASTER, priority=10, block=True)
call_api = on_command(cmd="/api", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)
update = on_command(cmd="/update", rule=plugin_enable("kami.super_tool"), permission=SUPERUSER | MASTER, priority=10, block=True)


@enable_group.handle()
async def enable_group_handle(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], state: T_State):
    if len(event.raw_message.split()) == 2:
        group_id = int(event.raw_message.split()[1])
    elif type(event) is GroupMessageEvent:
        group_id = event.group_id
    else:
        group_id = 0
    state2 = await ExtraData.get_group_data(group_id=group_id, key="enable", default=False)
    if state2:
        await enable_group.send(message="该群已启用机器人")
    else:
        await ExtraData.set_group_data(group_id=group_id, key="enable", value=True)
        await enable_group.send(message="群聊启用成功")


@disable_group.handle()
async def enable_group_handle(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], state: T_State):
    if len(event.raw_message.split()) == 2:
        group_id = int(event.raw_message.split()[1])
    elif type(event) is GroupMessageEvent:
        group_id = event.group_id
    else:
        group_id = 0
    state2 = await ExtraData.get_group_data(group_id=group_id, key="enable", default=False)
    if not state2:
        await disable_group.send(message="该群已停用机器人")
    else:
        await ExtraData.set_group_data(group_id=group_id, key="enable", value=False)
        await enable_group.send(message="群聊停用成功")


@setConfig.handle()
async def setConfigHandle(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    try:
        args, kws = Command.formatToCommand(Command.escape(event.raw_message))

        targetType = args[1]
        targetId = args[2]
        key = args[3]
        value = eval(Command.formatToString(*args[4:]))
        if targetType == "gm":
            r = await ExtraData.set_group_member_data(event.group_id, targetId, key=key, value=value)
            if r:
                await setConfig.send("属性设置成功:\n%s%s\n%s:%s" % (targetType, targetId, key, value))
            else:
                await setConfig.send("属性设置失败")
        else:
            r = await ExtraData.setData(targetType=targetType, targetId=targetId, key=key, value=value)
            if r:
                await setConfig.send("属性设置成功:\n%s%s\n%s:%s" % (targetType, targetId, key, value))
            else:
                await setConfig.send("属性设置失败")
    except BaseException as e:
        await Session.sendException(bot, event, state, e, text="请检查字符串是否用单双引号括起来了，括号是否成对输入，特殊字符是否转义")


@getConfig.handle()
async def getConfigHandle(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    try:
        args, kws = Command.formatToCommand(event.raw_message)
        targetType = args[1]
        targetId = int(args[2])
        key = args[3]

        if targetType in ["g", "gm"] and await(GROUP_OWNER | GROUP_ADMIN | SUPERUSER)(bot, event) or await SUPERUSER(bot, event):
            if targetType == "gm":
                r = await ExtraData.get_group_member_data(event.group_id, targetId, key=key)
            else:
                r = await ExtraData.getData(targetType=targetType, targetId=targetId, key=key)
            args = list(args)
            args.append(r)
            args.append(type(r))
            await getConfig.send("- 类: %s\n- 值: %s" % (type(r), r))
        else:
            await getConfig.send("你没有权限查看此条目", at_sender=True)
    except BaseException as e:
        await Session.sendException(bot, event, state, e)


@send_mutil_msg.handle()
async def send_mutil_msg_handle(bot: Bot, event: PrivateMessageEvent, state: T_State):
    friend_list = await bot.get_friend_list()
    args = event.raw_message.split()
    msg = Message(" ".join(args[1:]))
    for friend in friend_list:
        try:
            friend_info = await bot.get_stranger_info(user_id=friend["user_id"])
            if await ExtraData.get_user_data(user_id=friend["user_id"], key="enable", default=False):
                await bot.send_private_msg(user_id=friend["user_id"], message=msg)
                await send_mutil_msg.send(message="消息已发送到：%s(%s)" % (friend_info["nickname"], friend["user_id"]))
        except BaseException as e:
            await Session.sendException(bot, event, state, e)

        await asyncio.sleep(random.randint(15, 30))


@backup_data.handle()
async def backup_data_handle(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    f, n = await backup()
    await backup_data.send(message="数据备份完成：%s，共计%s个数据库" % (f, n))


@call_api.handle()
async def call_api_handle(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], state: T_State):
    try:
        args, kws = Command.formatToCommand(cmd=event.raw_message)
        r = await bot.call_api(args[1], **kws)
        await call_api.send(message=str(r))
    except BaseException as e:
        await Session.sendException(bot, event, state, e)


@update.handle()
async def update_handle(bot: Bot, event: PrivateMessageEvent, state: T_State):
    try:
        now_version = await ExtraData.get_resource_data(key="liteyuki.bot.version", default="0.0.0")
        now_version_description = await ExtraData.get_resource_data(key="liteyuki.bot.version_description", default="0.0.0")
        async with aiohttp.request("GET", url="https://gitee.com/snowykami/Liteyuki/raw/master/resource/resource_database.json") as r:
            online_version = (await r.json())["liteyuki.bot.version"]
        if now_version != online_version:
            await update.send("开始下载更新：%s -> %s" % (now_version, online_version))
            r = await ExtraData.download_file("https://github.com/snowyfirefly/Liteyuki/archive/refs/heads/master.zip",
                                              os.path.join(ExConfig.res_path, "version/new_code.zip"))
            if r:
                await update.send("正在安装")
                await update_move()
                await update.send("更新完成")
            else:
                await update.send("下载更新失败")
        else:
            await update.send("当前已是最新版本：%s(%s)" % (now_version, now_version_description))

    except BaseException as e:
        await Session.sendException(bot, event, state, e, "检查更新失败")