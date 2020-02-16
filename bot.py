import typing
from vkbottle import *
from vkbottle.rule import ChatActionRule
from vkbottle.api import Api
from vkbottle.keyboard import Keyboard, Text
from vkbottle.types import GroupJoin



bot = Bot("VK Group Token")

@bot.on.message_handler(text="My name is Van")
async def wrapper(ans: Message):
    await ans("1 message")
    await ans("2 message")
    await ans("3 message")
    await ans("4 message", keyboard=keyboard_gen([[{'text': 'test'}]], one_time=True)) # test keyboard



@bot.on.chat_message(text="test", lower=True)
async def wrapper(ans: Message):
	await ans(attachment = f'vk photo url') # (attachment = f'photo-185367978_457239106')





@bot.on.message_handler(text="text <text>", lower=True)
async def wrapper(ans: Message, text):
    await ans("test {}".format(text))




@bot.on.chat_message(text="info", lower=True)
async def wrapper(ans: Message):
    if ans.reply_message:
    	await ans(f"Id чата: {ans.peer_id}\nId ответа: {ans.reply_message.from_id}\nId сообщения: {ans.conversation_message_id} или {ans.id}\nId пользователя: {ans.from_id}")  # chat info
    else:
        await ans(f"Id чата: {ans.peer_id}\nId сообщения: {ans.conversation_message_id} или {ans.id}\nId пользователя: {ans.from_id}")




@bot.on.message_handler(text="who i'm", lower=True)
async def wrapper(ans: Message):
    await ans(f'Who are @id{ans.from_id}(you)')





@bot.on.chat_message(lev=["кик","kick"])
async def ban(ans: Message):
    if ans.reply_message:
        if await check(ans):
            if ans.reply_message.from_id!=-185367978:
                if await checkre(ans):
                    await ans("Я не могу исключить администратора беседы")
                else:
                    await ans("пока")
                    await bot.api.messages.removeChatUser(chat_id=ans.peer_id-2000000000, member_id=ans.reply_message.from_id)       #kick sistem
            else:
                await ans("Ты еблан?")
        else:
            await ans("Ты не админ")
    else:
        await ans("Перешли сообщение того, кого нужно исключить из беседы")


async def check(message: Message):
    items = (await bot.api.messages.getConversationsById(peer_ids = message.peer_id))['items']
    if not items: return False
    chat_settings = items[0]['chat_settings']
    is_admin = message.from_id == chat_settings['owner_id'] or message.from_id in chat_settings['admin_ids']   #check admin
    return is_admin


async def checkre(message: Message):
    items = (await bot.api.messages.getConversationsById(peer_ids = message.peer_id))['items']
    if not items: return False
    chat_settings = items[0]['chat_settings']
    is_admin = message.reply_message.from_id == chat_settings['owner_id'] or message.reply_message.from_id in chat_settings['admin_ids']  # check admin in reply message
    return is_admin




@bot.on.chat_message(ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]))  #send message on groupchat join
async def invite(ans: Message):
    await ans("Welcome")



@bot.on.event.group_join()
async def join(event: GroupJoin):
		await bot.api.messages.send(peer_id=event.user_id, message="♂Welcome to the club, buddy♂", attachment="photo-185367978_457239102", random_id=0)     #send message on group subscribe


@bot.on.chat_message(IsAdmin(True), text = ['echo <text>', 'echo'], lower=True)
async def echo(message, text = 'Сообщение не указано'):
	member_ids = (item['member_id'] for item in (await bot.api.request('messages.getConversationMembers', {'peer_id' : message.peer_id}))['items'] if item['member_id'] > 0 and item['member_id'] != id)  #  @everyone
	await message(f"{text}\n{''.join(f'[id{member_id}|.]' for member_id in member_ids)}")



if __name__ == "__main__":
 bot.run_polling()
