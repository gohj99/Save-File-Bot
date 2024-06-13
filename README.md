# Save File Bot

*一个用来保存你发送的文件与一些受限内容的telegram机器人*

---

## 变量

- `HASH` 来自 my.telegram.org 的 API HASH
- `ID` 来自 my.telegram.org 的 API ID
- `TOKEN` 来自 @BotFather 的机器人TOKEN
- `STRING` 会话字符串，您可以通过运行 [gist](https://gist.github.com/bipinkrish/0940b30ed66a5537ae1b5aaaee716897#file-main-py) 来获取

---

# 用法

**对于公开聊天的文件**

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
