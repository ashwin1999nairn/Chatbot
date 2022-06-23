# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import random
#
#
def Weather(place):
    base_url = "http://api.openweathermap.org/data/2.5/weather?appid=d535fb9e379e10ee57c2ace5c31726a9"
    Final_url = base_url + "&q=" + place + "&units=metric"
    weather_data = requests.get(Final_url).json()
    return [weather_data['weather'], weather_data['main']]

class ActionTellWeather(Action):
    
    def name(self) -> Text:
        return "action_tell_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        res = Weather(current_place)
        main=res[1]
        main_temp=main['temp']
        main_min_temp=main['temp_min']
        main_max_temp=main['temp_max']
        
        des=res[0]
        temp_des=des[0]['description'] 

        msg_temp = f"Current temperature is {main_temp} degree celcius while the minimum temperature is {main_min_temp} degree celcius and maximum temperature is {main_max_temp} degree celcius in {current_place} today. So there's {temp_des} today"
        dispatcher.utter_message(text=msg_temp)
        case_rain=["light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain", "freezing rain", "light intensity shower rain", "shower rain", "heavy intensity shower rain", "ragged shower rain","light intensity drizzle", "drizzle", "heavy intensity drizzle", "light intensity drizzle rain", "drizzle rain", "heavy intensity drizzle rain", "shower rain and drizzle", "heavy shower rain and drizzle", "shower drizzle"]

        if temp_des in case_rain:
            response=[f"might wanna take an umbrella on your way out", f"Do not forget your raincoat", f"carry an umbrella with you",f"a good time to have snack served hot"]
            dispatcher.utter_message(text=random.choice(response)) 

        case_thunderstorm=["thunderstorm with light rain", "thunderstorm with rain", "thunderstorm with heavy rain", "light thunderstorm", "thunderstorm", "heavy thunderstorm", "ragged thunderstorm", "thunderstorm with light drizzle", "thunderstorm with drizzle", "thunderstorm with heavy drizzle"]
        if temp_des in case_thunderstorm:
            response=[f"Please try to stay indoors", f"Seek a shelter to protect yourself if it gets worse", f"Try to avoid electrical equipments"]
            dispatcher.utter_message(text=random.choice(response)) 

        case_snow=["light snow", "Snow", "Heavy snow", "Sleet", "Light shower sleet", "Shower sleet", "Light rain and snow", "Rain and snow", "Light shower snow", "Shower snow", "Heavy shower snow"]
        if temp_des in case_snow:
            response=[f"A perfect time to have hot chocolate", f"Have your shovels and sledges ready", f"Might need to wear multiple layer of clothes", f"Do not forget your caps and socks"]
            dispatcher.utter_message(text=random.choice(response))
        
        case_clear=["clear sky"]

        if temp_des in case_clear and main_temp>=35:
            response_hot=[f"Keep yourself hydrated", f"An ice cream would be nice", f"dont forget your sunscreen"]
            dispatcher.utter_message(text=random.choice(response_hot))

        if temp_des in case_clear and main_temp<=10:
            response_hot=[f"A hot chocolate would be nice", f"Dont forget your gloves and caps", f"dont forget to wear multiple layer of clothes"]
            dispatcher.utter_message(text=random.choice(response_hot))

        if temp_des in case_clear and main_temp>10 and main_temp<=35:
            response_normal=[f"A day filled with good vibes", f"A perfect day to go out", f"Lookout for the beautiful birds in the sky"]
            dispatcher.utter_message(text=random.choice(response_normal))
        
        case_atmos=["mist", "fog","smoke"]
        if temp_des in case_atmos:
            response_fog=[f"Keep your foglight on", f"be alert of vehicles"]
            dispatcher.utter_message(text=random.choice(response_fog))

        if temp_des in case_atmos and main_temp<=10:
            response_cold=[f"Gloves, socks and cap might be handy", f"Consume hot water instead of normal", f"wear more layers than usual"]
            dispatcher.utter_message(text=random.choice(response_cold))

        case_clouds=["few clouds", "scattered clouds", "broken clouds", "overcast clouds"]
        if temp_des in case_clouds:
            if temp_des=='overcast clouds':
                 response_clouds=[f"It looks like it might rain, take necessary precautions"]
                 dispatcher.utter_message(text=random.choice(response_clouds))



        return []

class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        
        return [SlotSet("location", current_place)] 
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
