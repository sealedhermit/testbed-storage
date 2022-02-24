from typing import Any, Text, Dict, List
from typing import Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
import pandas as pd
import os
from excel_data_store_read import DataStore




class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

      if tracker.get_slot('category') == 'phone':
         dispatcher.utter_message(template="utter_details_thanks_phone",
                                 category=tracker.get_slot("category"),
                                 price=tracker.get_slot("price"),
                                 ram=tracker.get_slot("ram"),
                                 camera=tracker.get_slot("camera"),
                                 storage=tracker.get_slot("storage"),
                                 display=tracker.get_slot("display"),
                                 battery=tracker.get_slot("battery"),
                                 network=tracker.get_slot("network"),
                                 stockandroid=tracker.get_slot("stockandroid"))

      elif tracker.get_slot('category') == 'tablet':
         dispatcher.utter_message(template="utter_details_thanks_tablet",
                                 category=tracker.get_slot("category"),
                                 price=tracker.get_slot("price"),
                                 ram=tracker.get_slot("ram"),
                                 storage=tracker.get_slot("storage"),
                                 network=tracker.get_slot("network"))
    

    
from excel_data_store_read import DataStore
class ActionSaveData(Action):
    def name(self) -> Text:
        return "action_save_conversation"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        DataStore(tracker.get_slot("category"),
            tracker.get_slot("price"),
            tracker.get_slot("storage"),
            tracker.get_slot("ram"),
            tracker.get_slot("battery"),
            tracker.get_slot("display"),
            tracker.get_slot("network"))
            
        dispatcher.utter_message(text="Data Stored Successfully.")

        return []
                                 
#class ActionSaveConversation(Action):

    #def name(self) -> Text:
        #return "action_save_conversation"

    #def run(self, dispatcher: CollectingDispatcher,
            #tracker: Tracker,
            #domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #conversation=tracker.events
        #print(conversation)
        #import os
        #import csv
        #if not os.path.isfile('chats.csv'):
            #with open('chats.csv','w') as file:
                #file.write("intent,user_input,entity_name,entity_value,bot_reply\n")
        #chat_data=''
        #for i in conversation:
            #if i['event'] == 'user':
                #chat_data+=i['parse_data']['intent']['name']+','+i['text']+','
                #print('user: {}'.format(i['text']))
                #if len(i['parse_data']['entities']) > 0:
                    #chat_data+=i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+','
                    #print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                          #i['parse_data']['entities'][0]['value'])
                #else:
                    #chat_data+=",,"
            #elif i['event'] == 'bot':
                #print('Bot: {}'.format(i['text']))
                #try:
                    #chat_data+=i['metadata']['utter_action']+','+i['text']+'\n'
                #except KeyError:
                    #pass
        #else:
            #with open('chats.csv','a') as file:
               #file.write(chat_data)

        #dispatcher.utter_message(text="All Chats saved.")

        #return []
    

class ValidateProductDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_product_details_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",

    ) -> Optional[List[Text]]:
        

        if tracker.get_slot('category') == 'phone':
            required_slots = ['price', 'stockandroid', 'display','camera', 'storage', 'ram', 'battery']
        
        elif tracker.get_slot('category') == 'tablet':
            required_slots = ['price', 'network','storage', 'ram']
        
        return required_slots

    def validate_price(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `price` value."""

        # If the price is less than 1000, it might be wrong.
        try:
            price = int(re.findall(r'[0-9]+',slot_value)[0])
        except:
            price = 0
        
        if price > 5000 and price <= 1000000:
            return {"price":price}
        else:
            dispatcher.utter_message(text=f"Invalid budget.")
            return {"price":None}

       
            
        


    def validate_ram(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `ram` value."""

        # If the RAM is 0, it might be wrong.
        try:
            ram = int(re.findall(r'[0-9]+',tracker.get_slot('ram'))[0])
        except:
           ram = 0
        if ram != 0 and ram <= 32:
            return {"ram":ram}
        else:
            dispatcher.utter_message(text="invalid entry")
            return {"ram":None}
        
        
        
    def validate_camera(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `camera` value."""

        
        try:
            camera = int(re.findall(r'[0-9]+',tracker.get_slot('camera'))[0])
        except:
           camera = 0
        if camera != 0 and camera <=108:
            return {"camera":camera}
        else:
            dispatcher.utter_message(text="invalid entry")
            return {"camera":None}


    def validate_storage(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `storage` value."""

       
        try:
            storage = int(re.findall(r'[0-9]+',tracker.get_slot('storage'))[0])
        except:
           storage = 0
        if storage != 0 and storage <= 512:
            return {"storage":storage}
        else:
            dispatcher.utter_message(text="invalid entry")
            return {"storage":None}

    def validate_battery(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `battery` value."""

        
        try:
            battery = int(re.findall(r'[0-9]+',tracker.get_slot('battery'))[0])
        except:
           battery = 0
        if battery != 0 and battery <= 7000:
            return {"battery":battery}
        else:
            dispatcher.utter_message(text="invalid entry")
            return {"battery":None}
    
    def validate_display(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `display` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            return {"display": True}
        if tracker.get_intent_of_latest_message() == "deny":
            return {"display": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"display": None}

    def validate_network(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `network` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            return {"network": True}
        if tracker.get_intent_of_latest_message() == "deny":
            return {"network": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"network": None}
    
    def validate_stockandroid(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `stock android` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            return {"stockandroid": True}
        if tracker.get_intent_of_latest_message() == "deny":
            return {"stockandroid": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"stockandroid": None}

class AskForDisplayAction(Action):
    def name(self) -> Text:
        return "action_ask_display"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Would you like an OLED display?",
                                 buttons=[
                                     {"title": "yes", "payload": "/affirm"},
                                     {"title": "no", "payload": "/deny"}
                                 ])
        return []


class AskForStockAndroidAction(Action):
    def name(self) -> Text:
        return "action_ask_stockandroid"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Is stock Android UI an important preference?",
                                 buttons=[
                                     {"title": "yes", "payload": "/affirm"},
                                     {"title": "no", "payload": "/deny"}
                                 ])
        return []
    
class AskForNetworkAction(Action):
    def name(self) -> Text:
        return "action_ask_network"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Which of these network connectivity do you prefer?",
                                 buttons=[
                                     {"title": "Wi-Fi + Cellular", "payload": "/affirm"},
                                     {"title": "Only Wi-Fi", "payload": "/deny"}
                                 ])
        return []


class ActionSearchResults(Action):
#
     def name(self) -> Text:
         return "action_search_results"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
             category = tracker.get_slot('category')
             display = tracker.get_slot('display')
             price = tracker.get_slot('price')
             ram = tracker.get_slot('ram')
             storage = tracker.get_slot('storage')
             battery = tracker.get_slot('battery')
             camera = tracker.get_slot('camera')
             network = tracker.get_slot('network')
             stockandroid = tracker.get_slot('stockandroid')

             url = 'https://raw.githubusercontent.com/sealedhermit/myfiles/main/database%20-%20phones_laptops_database_NEW.csv?raw=true'
             df = pd.read_csv(url,index_col=0)
             #df = pd.read_csv('/home/vidhun/Documents/phones_laptops_database_NEW.csv')
            
             if category == 'phone':
                output = df.loc[(df['category'] == 'phone') & (df['price_inr']<=price) & (df['back_camera_megapixel']>= camera) & (df['ram']>= ram) & (df['display']== display) & (df['stockandroid']== stockandroid) & (df['storage']>= storage) & (df['battery_mah']>= battery)]
             
             elif category == 'tablet':
                output =  df.loc[(df['category'] == 'tablet') & (df['price_inr']<= price) & (df['network']== network) & (df['ram']>= ram) & (df['storage']>= storage)]

             for url in output['product_url']:
                dispatcher.utter_message(text=url)
                return []
             

             dispatcher.utter_message(text='Product not found in the database')       
             return []


class ActionResetAllSlots(Action):

     def name(self):
         return "action_reset_all_slots"

     def run(self, dispatcher, tracker, domain):
         return [AllSlotsReset()]