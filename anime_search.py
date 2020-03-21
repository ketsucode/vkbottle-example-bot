from vkbottle import Bot, Message
import asyncio
from tracemoe import ATraceMoe #for anime search by image https://github.com/Ethosa/tracemoe

bot = Bot("Vk group token")

@bot.on.message_handler(text=["откуда","аниме","что за аниме","какое аниме"],lower=True,command=True)
async def wrapper(ans: Message):
    if ans.attachments and ans.attachments[0].photo:
        res = await ATraceMoe().search(ans.attachments[0].photo.sizes[-1].url,is_url=True)
        titles = res["docs"][0]["title_english"]
        episodes = res["docs"][0]["episode"]
        dfrom = round(res["docs"][0]["from"])
        dto = round(res["docs"][0]["to"])
        similaritys = round(res["docs"][0]["similarity"]*100)
        hoursdf = dfrom // 3600
        minutesdf = dfrom % 3600 // 60
        secondsdf = dfrom % 60
        hoursdt = dto // 3600
        minutesdt = dto % 3600 // 60
        secondsdt = dto % 60
        await ans("""Аниме:{}
        Серия: {}
        Таймкод: с {:02d}:{:02d}:{:02d} по {:02d}:{:02d}:{:02d}
        Точность: {}%""".format(titles,
        episodes,
        hoursdf,
        minutesdf,
        secondsdf,
        hoursdt,
        minutesdt,
        secondsdt,
        similaritys))
    else:
        await ans("Прикрепи скриншот, чтобы я нашел откуда он")

if __name__ == "__main__":
	bot.run_polling()
