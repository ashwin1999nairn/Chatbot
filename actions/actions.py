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
#
#
def Weather(place):
    API_key = "d535fb9e379e10ee57c2ace5c31726a9"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    Final_url = base_url + "appid=" + API_key + "&q=" + place + "&units=metric"
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

        msg_temp = f"Current temperature is {main_temp} degree celcius while the minimum temperature is {main_min_temp} degree celcius and maximum temperature is {main_max_temp} degree celcius in {current_place} today. So there's a bit {temp_des} today"
        dispatcher.utter_message(text=msg_temp)
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
