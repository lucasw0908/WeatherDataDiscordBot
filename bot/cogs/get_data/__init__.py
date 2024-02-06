import discord
from discord.ext import commands
import logging
import os
from time import strptime, mktime
from datetime import datetime

from bot.utils.embed import EmbedMaker
from bot.utils.weather import location_choice, data_type_choice, get_weather_data, description_to_elementname, city, city_choice
from bot.utils.plot import save_plot_data

log = logging.getLogger(__name__)


class GetData(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="天氣資訊", description="取得當前天氣資訊(只支援台北)")
    async def get_weather_data(self, ctx: discord.ApplicationContext, 
                               城市: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(city_choice)), 
                               地區: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(location_choice)), 
                               資料類型: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(data_type_choice)), 
                               動態資料: discord.Option(bool)
                               ):
        
        animated = 動態資料
        location = 地區
        data_type = 資料類型
        weather_data = get_weather_data(location_name=location)
        data = {}
        data["X"] = []
        data["Y"] = []
        
        for time_data in weather_data[description_to_elementname(data_type)]:
            
            start_time = strptime(time_data["startTime"], "%Y-%m-%d %H:%M:%S")
            end_time = strptime(time_data["endTime"], "%Y-%m-%d %H:%M:%S")
            
            try: 
                y = int(time_data["elementValue"][0]["value"])
            except:
                await ctx.respond(embed=EmbedMaker(status=False, description="選取了無效的資料類型"))
                return
            
            data["X"].append(datetime.fromtimestamp(mktime(start_time)))
            data["Y"].append(y)
            
        percentage_mode = (time_data["elementValue"][0]["measures"] == "百分比")
            
        save_plot_data(data,
                       title=f"{location} {data_type}資料",
                       xlabel="時間",
                       ylabel=description_to_elementname(data_type),
                       percentage_mode=percentage_mode,
                       gif=animated
                       )
        
        file = discord.File(f'data.{"gif" if animated else "png"}')
        await ctx.respond(file=file)
        
        log.debug(f"{ctx.author.name}({ctx.author.id}) used {ctx.command.name}.")
            
def setup(bot: commands.Bot):
    bot.add_cog(GetData(bot))