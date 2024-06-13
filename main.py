import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json

with open('config.json', 'r') as f: DATA = json.load(f)
def getenv(var): return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = getenv("STRING")
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

# 下载状态函数
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# 上传状态
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# 进度写入函数
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


# 开始命令处理函数
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	#bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save File Bot\n你可以发送文件或受限内容的链接让我保存__\n\n{USAGE}",
	#reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]]), reply_to_message_id=message.id)
		bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save File Bot\n你可以发送文件或受限内容的链接让我保存__\n\n{USAGE}", reply_to_message_id=message.id)

#收到视频或图片执行

@bot.on_message(filters.photo | filters.video)
def save_media(client, message):
    if message.photo:
        # 处理收到的图片消息
        print("收到图片")
        # 下载图片
        #file_path = client.download_media(message)
        file_path = handle_save(message)
        print(f"图片已下载到: {file_path}")
        #message.reply_text("图片已收到并下载！")
    elif message.video:
        # 处理收到的视频消息
        print("收到视频")
        # 下载视频
        #file_path = client.download_media(message)
        file_path = handle_save(message)
        print(f"视频已下载到: {file_path}")
        #message.reply_text("视频已收到并下载！")

#收到“https://t.me/***”后执行
@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	print(message.text)

	# 加入聊天
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
				return
			bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
		except UserAlreadyParticipant:
			bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
		except InviteHashExpired:
			bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)

	# 收到消息
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		temp = datas[-1].replace("?single","").split("-")
		fromID = int(temp[0].strip())
		try: toID = int(temp[1].strip())
		except: toID = fromID

		for msgid in range(fromID, toID+1):

			# 私人的聊天
			if "https://t.me/c/" in message.text:
				chatid = int("-100" + datas[4])
				
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				
				handle_private(message,chatid,msgid)
				# try: handle_private(message,chatid,msgid)
				# except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
			
			# 机器人的聊天
			elif "https://t.me/b/" in message.text:
				username = datas[4]
				
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

			# 公开的聊天
			else:
				username = datas[3]

				try: msg  = bot.get_messages(username,msgid)
				except UsernameNotOccupied: 
					bot.send_message(message.chat.id,f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
					return
				try:
					if '?single' not in message.text:
						#bot.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
						handle_private(message,username,msgid)
					else:
						#bot.copy_media_group(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
						handle_private(message,username,msgid)
				except:
					if acc is None:
						bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
						return
					try: handle_private(message,username,msgid)
					except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

			# 等待时间
			time.sleep(3)


# 处理私人的聊天
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
		msg: pyrogram.types.messages_and_media.message.Message = acc.get_messages(chatid,msgid)
		msg_type = get_message_type(msg)

		if "Text" == msg_type:
			bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
			return

		smsg = bot.send_message(message.chat.id, '__下载中__', reply_to_message_id=message.id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')
		bot.delete_messages(message.chat.id,[smsg.id])
		smsg = bot.send_message(message.chat.id, '__保存成功__', reply_to_message_id=message.id)

		#upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		#upsta.start()
		
		#if "Document" == msg_type:
		#	try:
		#		thumb = acc.download_media(msg.document.thumbs[0].file_id)
		#	except: thumb = None
			
		#	bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
		#	if thumb != None: os.remove(thumb)

		#elif "Video" == msg_type:
		#	try: 
		#		thumb = acc.download_media(msg.video.thumbs[0].file_id)
		#	except: thumb = None

		#	bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
		#	if thumb != None: os.remove(thumb)

		#elif "Animation" == msg_type:
		#	bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
			   
		#elif "Sticker" == msg_type:
		#	bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

		#elif "Voice" == msg_type:
		#	bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

		#elif "Audio" == msg_type:
		#	try:
		#		thumb = acc.download_media(msg.audio.thumbs[0].file_id)
		#	except: thumb = None
				
		#	bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
		#	if thumb != None: os.remove(thumb)

		#elif "Photo" == msg_type:
		#	bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

		#os.remove(file)
		#if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		#bot.delete_messages(message.chat.id,[smsg.id])

# 保存发来的图片或视频
def handle_save(message: pyrogram.types.messages_and_media.message.Message):
		message_type = get_message_type(message)

		if "Text" == message_type:
			bot.send_message(message.chat.id, message.text, entities=message.entities, reply_to_message_id=message.id)
			return

		smsg = bot.send_message(message.chat.id, '__下载中__', reply_to_message_id=message.id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = bot.download_media(message, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')
		bot.delete_messages(message.chat.id,[smsg.id])
		smsg = bot.send_message(message.chat.id, '__保存成功__', reply_to_message_id=message.id)
		return file

		#upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		#upsta.start()
		
		#if "Document" == msg_type:
		#	try:
		#		thumb = acc.download_media(msg.document.thumbs[0].file_id)
		#	except: thumb = None
			
		#	bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
		#	if thumb != None: os.remove(thumb)

		#elif "Video" == msg_type:
		#	try: 
		#		thumb = acc.download_media(msg.video.thumbs[0].file_id)
		#	except: thumb = None

		#	bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
		#	if thumb != None: os.remove(thumb)

		#elif "Animation" == msg_type:
		#	bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
			   
		#elif "Sticker" == msg_type:
		#	bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

		#elif "Voice" == msg_type:
		#	bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

		#elif "Audio" == msg_type:
		#	try:
		#		thumb = acc.download_media(msg.audio.thumbs[0].file_id)
		#	except: thumb = None
				
		#	bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
		#	if thumb != None: os.remove(thumb)

		#elif "Photo" == msg_type:
		#	bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

		#os.remove(file)
		#if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		#bot.delete_messages(message.chat.id,[smsg.id])

# 获取消息类型
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass


USAGE = """**对于公开聊天的文件**

__只需发送相应链接__

**对于非公开聊天的文件**

__首先发送聊天的邀请链接 (如果当前提供会话的帐户已经是聊天成员，则不需要发送邀请链接)
然后发送链接__

**对于机器人聊天**

__发送带有“/b/”的链接、机器人的用户名和消息 ID，你可能需要安装一些非官方客户端来获取如下所示的 ID__

```
https://t.me/b/botusername/4321
```

**如果你需要一次保存多个受限文件**

__发送公共/私人帖子链接，如上所述，使用格式“发件人 - 收件人”发送多条消息，如下所示__

```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```

__最好在中间加上空格__
"""


# infinty polling
bot.run()
