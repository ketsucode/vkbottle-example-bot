from vkbottle import *
import asyncio
from tracemoe import ATraceMoe #for anime search by image https://github.com/Ethosa/tracemoe


@bot.on.message_handler(lev=["откуда","аниме","что за аниме","какое аниме"], lower=True)
async def wrapper(ans: Message):
	if ans.attachments and ans.attachments[0].photo:
	    res = await ATraceMoe().search(ans.attachments[0].photo.sizes[-1].url,is_url=True)
        title = res["docs"][0]["title_english"]
        episode = res["docs"][0]["episode"]
        dfrom = res["docs"][0]["from"]
        dto = res["docs"][0]["to"]
        similarity = round(res["docs"][0]["similarity"]*100
        hoursdf = dfrom // 3600
        minutesdf = dfrom % 3600 // 60
        secondsdf = dfrom % 60
        hoursdt = dto // 3600
        minutesdt = dto % 3600 // 60
        secondsdt = dto % 60
	    await ans('Аниме:{} \nСерия: {}\nТаймкод: с {:02d}:{:02d}:{:02d}  по {:02d}:{:02d}:{:02d} \nТочность: {}%'.format(title,episode,))
	else:
		await ans("Прикрепи картинку, чтобы я нашел откуда она")


if __name__ == "__main__":
	bot.run_polling()
