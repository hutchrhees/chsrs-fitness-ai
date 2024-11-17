from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCalculateCalorieBurn(Action):
    def name(self) -> Text:
        return "action_calculate_calorie_burn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              # Get the activity and user weight from slots
        activity = tracker.get_slot("exercise")
        user_weight = tracker.get_slot("weight")  # Optional slot for weight in kg

        # If weight is not provided, prompt the user to specify it
        if not user_weight:
            dispatcher.utter_message(
                text="To calculate calories burned accurately, could you please tell me your weight in kilograms?"
            )
            return [SlotSet("exercise", activity)]  # Retain the activity slot for the next round

        # Check if activity is provided
        if not activity:
            dispatcher.utter_message(
                text="Could you tell me which activity you'd like to calculate calories for?"
            )
            return []

        # MET values for various activities
        met_values = {
            "running": 9.8,
            "cycling": 7.5,
            "swimming": 8.0,
            "walking": 3.5,
            "yoga": 2.5,
            "weightlifting": 6.0,
        }

        # Calculate calories
        met = met_values.get(activity.lower(), None)
        if met:
            try:
                user_weight = float(user_weight)  # Ensure weight is numeric
                calories_per_minute = (met * 3.5 * user_weight) / 200
                calories_30_min = round(calories_per_minute * 30)
                response =  f"You burn approximately {calories_30_min} calories per 30 minutes of {activity}."
            except ValueError:
                response = f"It seems the weight provided is not valid. Please provide a numeric value for your weight."
        else:
            response = f"Sorry, I don't have calorie burn data for {activity}. Can you try another activity?"

        # Send the response back to the user
        dispatcher.utter_message(text=response)

        return []
