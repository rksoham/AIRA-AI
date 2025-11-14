from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionDefaultResponse(Action):
    """Custom action for default/fallback responses"""

    def name(self) -> Text:
        return "action_default"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Execute the action"""
        dispatcher.utter_message(text="I'm not sure I understand. Could you please rephrase your question?")
        return []
