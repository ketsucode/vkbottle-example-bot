from vkbottle import Bot, Message
from tracemoe import ATraceMoe
from datetime import timedelta

bot = Bot("Vk group token")


@bot.on.message_handler(
    text=["откуда", "аниме", "что за аниме", "какое аниме"], lower=True, command=True
)
async def wrapper(ans: Message):
    if ans.attachments and ans.attachments[0].photo:
        res = await ATraceMoe().search(
            ans.attachments[0].photo.sizes[-1].url, is_url=True
        )
        titles = res["docs"][0]["title_english"]
        episode = res["docs"][0]["episode"]
        rtimef = round(res["docs"][0]["from"])
        timefrom = datetime.timedelta(seconds=rtimef)
        rtimet = round(res["docs"][0]["from"])
        timeto = datetime.timedelta(seconds=rtimet)
        similarity = round(res["docs"][0]["similarity"] * 100)
  
        await ans(
            """Аниме:{}
        Серия: {}
        Таймкод: с {} по {}
        Точность: {}%""".format(
                titles,
                episodes,
                timefrom,
                timeto,
                similaritys,
            )
        )
    else:
        await ans("Прикрепи скриншот, чтобы я нашел откуда он")


if __name__ == "__main__":
    bot.run_polling()
