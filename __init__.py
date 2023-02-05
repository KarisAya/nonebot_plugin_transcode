from nonebot.plugin.on import on_command,on_regex,on_startswith
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,Message
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg

import requests
import re
import hashlib

u2word = on_command(r"\u",rule = to_me(),priority = 20,block = True)

@u2word.handle()
async def _(bot:Bot, event: MessageEvent,arg: Message = CommandArg()):
    cmd = arg.extract_plain_text()
    u = cmd.split(r"\u")

    word = ""
    sentence = ""

    for x in u:
        try:
            int(x,16)
            res = chr(int(x,16))
        except:
            continue

        word +=f"\\u{x}：{res}\n"
        sentence += res

    await u2word.finish(word + sentence)

word2u = on_command("unicode",rule = to_me(),priority = 20,block = True)

@word2u.handle()
async def _(event: MessageEvent,arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    u = ""
    for x in msg:
        u += f"\\u{format(ord(x),'x')}"

    await word2u.finish(u)

def image_md5(event:MessageEvent) -> list:
    '''
    获取图片文件名
    '''
    MD5 = []
    for msg in event.message:
        if msg.type == "image":
            MD5.append(msg.data["file"])
    if event.reply:
        for msg in event.reply.message:
            if msg.type == "image":
                MD5.append(msg.data["file"])
    return MD5

msg2md5 = on_command("md5",rule = to_me(),priority = 20,block = True)

@msg2md5.handle()
async def _(event: MessageEvent,arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = arg.extract_plain_text().strip()
        md5 = hashlib.md5(msg.encode()).hexdigest().upper()
    elif MD5 := image_md5(event):
        md5 = ""
        for x in MD5:
            md5 += x.split(".")[0].upper()
            md5 += "\n"
        else:
            md5 = md5[:-1]
    else:
        md5 = ""

    await msg2md5.finish(md5)

def image_url(event:MessageEvent) -> list:
    '''
    获取图片url
    '''
    url = []
    for msg in event.message:
        if msg.type == "image":
            url.append(msg.data["url"])
    if event.reply:
        for msg in event.reply.message:
            if msg.type == "image":
                url.append(msg.data["url"])
    return url

msg2sha256 = on_command("sha256",rule = to_me(),priority = 20,block = True)

@msg2sha256.handle()
async def _(event: MessageEvent,arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = arg.extract_plain_text().strip()
        sha256 = hashlib.sha256(msg.encode()).hexdigest().upper()
    elif URL := image_url(event):
        sha256 = ""
        for url in URL:
            resp = requests.get(url)
            if resp.status_code == 200:
                sha256 += hashlib.sha256(resp.content).hexdigest().upper()
            else:
                sha256 += "【失败】"
            sha256 += "\n"
        else:
            sha256 = sha256[:-1]
    else:
        sha256 = ""

    await msg2sha256.finish(sha256)