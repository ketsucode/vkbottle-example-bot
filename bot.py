from vkbottle import Bot, Message, keyboard_gen
from vkbottle.rule import ChatActionRule


bot = Bot("VK Group Token")


async def check(ans: Message, id):
    items = (await bot.api.messages.getConversationsById(peer_ids=ans.peer_id))["items"]
    if not items:
        return False
    chat_settings = items[0]["chat_settings"]
    is_admin = id == chat_settings["owner_id"] or id in chat_settings["admin_ids"]
    return is_admin


async def get_id(bot, pattern: str) -> int:
    if pattern.isdigit():
        return int(pattern)
    elif (
        "vk.com/" in pattern
        or "http://vk.com/" in pattern
        or "https://vk.com/" in pattern
    ):
        uid = (await bot.api.users.get(user_ids=pattern.split("/")[-1]))[0]
        return uid["id"]
    elif "[id" in pattern:
        uid = pattern.split("|")[0]
        return int(uid.replace("[id", ""))


@bot.on.chat_invite()
async def wrapper(ans: Message):
    await ans(
        "Привет! \nДля полноценной работы бота необходимо выдать админку. \n"
        "Список доступных команд можно узнать написав !help или !помощь."
    )


@bot.on.message_handler(text="shue")
async def wrapper(ans: Message):
    await ans("1 message")
    await ans("2 message")
    await ans("3 message")
    await ans(
        "4 message", keyboard=keyboard_gen([[{"text": "test"}]], one_time=True)
    )  # test keyboard


@bot.on.chat_message(text="test", lower=True)
async def wrapper(ans: Message):
    await ans(attachment=f"vk photo url")  # (attachment = f'photo-185367978_457239106')


@bot.on.message_handler(text="text <text>", lower=True)
async def wrapper(ans: Message, text):
    await ans("test {}".format(text))


@bot.on.chat_message(text="инфо", lower=True, command=True)
async def wrapper(ans: Message):
    if ans.reply_message:
        await ans(
            f"""Id чата: {ans.peer_id}
        Id из ответа: {ans.reply_message.from_id}
        Id сообщения: {ans.conversation_message_id} или {ans.id}
        Id пользователя: {ans.from_id}"""
        )
    else:
        await ans(
            f"""Id чата: {ans.peer_id}
        Id сообщения: {ans.conversation_message_id} или {ans.id}
        Id отправителя: {ans.from_id}"""
        )


@bot.on.message_handler(text="who i'm", lower=True)
async def wrapper(ans: Message):
    await ans(f"Who are @id{ans.from_id}(you)")


@bot.on.chat_message(
    lev=["!кик", "!kick", "!kick <domain>", "!кик <domain>"], lower=True
)
async def ban(ans: Message, domain=""):
    if await get_id(bot, domain):
        user = await get_id(bot, domain)
    else:
        if not ans.reply_message:
            return (
                f"Напиши ид или ответь на сообщение того, кого нужно исключить из чата"
            )
        user = ans.reply_message.from_id
    if not await check(ans, ans.from_id):
        return "Ты не админ"
    if user == -185367978:
        return "Ты еблан?"
    if await check(ans, user):
        return "Я не могу исключить администратора беседы"
    await ans("пока", sticker_id=13607)
    await bot.api.messages.removeChatUser(
        chat_id=ans.peer_id - 2000000000, member_id=user
    )


@bot.on.chat_message(
    ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"])
)  # send message on groupchat join
async def invite(ans: Message):
    await ans("Welcome")


@bot.on.chat_message(text=["echo <text>", "echo"], lower=True)
async def echo(ans, text="Сообщение не указано"):
    if await check(ans, id=ans.from_id):
        member_ids = (
            item["member_id"]
            for item in (
                await bot.api.request(
                    "messages.getConversationMembers", {"peer_id": ans.peer_id}
                )
            )["items"]
            if item["member_id"] > 0 and item["member_id"] != id
        )
        await ans(
            f"{text}\n{''.join(f'[id{member_id}|.]' for member_id in member_ids)}",
            attachment=f"photo-185367978_457239114",
        )
    else:
        await ans("Ты не админ")


if __name__ == "__main__":
    bot.run_polling()
