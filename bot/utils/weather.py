import requests
import logging
import discord
import time

from bot.utils.url import WeatherUrl


log = logging.getLogger(__name__)

remove_element_names = ["風向", "天氣預報綜合描述", "天氣現象"]
description_to_elementname_dict = {}

url = None
        
def city(cityname: str) -> None:
    global url
    if cityname in WeatherUrl:
        url = WeatherUrl[cityname]
    else:
        log.error("Unkwnown city name.")
        
def get_weather_data(location_name: str) -> dict | None:
    
    global url
    if url is None:
        log.error("URL was not found.")
        return None
        
    data = requests.get(url).json()
    weather_data = {}
    
    if not data["success"]: 
        log.warning("Weather data was not found.")
        return None
        
    for location in data["records"]["locations"][0]["location"]:
        
        if location["locationName"] == location_name: 
            weather_elements = location["weatherElement"]
            
    for weather_element in weather_elements:
        weather_data[weather_element["elementName"]] = weather_element["time"]
        
    return weather_data

def city_choice(ctx: discord.AutocompleteContext) -> list:
    return list(WeatherUrl.keys())
   
def location_choice(ctx: discord.AutocompleteContext) -> list[str] | None: 
    
    city(ctx.options["城市"])
    
    global url
    if url is None:
        log.error("URL was not found.")
        return None
        
    data = requests.get(url).json()
    
    location_list = []
    
    for location in data["records"]["locations"][0]["location"]:
        location_list.append(location["locationName"])
        
    return location_list

def data_type_choice(ctx: discord.AutocompleteContext) -> list | None:
    
    global url
    if url is None:
        log.error("URL was not found.")
        return None
        
    data = requests.get(url).json()
    data_type_list = []
    for weather_element in data["records"]["locations"][0]["location"][0]["weatherElement"]:
        
        global description_to_elementname_dict
        description_to_elementname_dict[weather_element["description"]] = weather_element["elementName"]
        
        if weather_element["description"] not in remove_element_names:
            data_type_list.append(weather_element["description"])
        
    return data_type_list

def description_to_elementname(element_description: str) -> str | None:
    
    if element_description not in description_to_elementname_dict:
        log.error("Variable: description_to_elementname_dict was not found.")
        return None
    
    return description_to_elementname_dict[element_description]