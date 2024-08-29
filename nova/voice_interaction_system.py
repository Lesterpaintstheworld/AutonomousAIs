import random
from typing import Dict, Any, List

class VoiceInteractionSystem:
    def __init__(self):
        self.intents = {
            "query_character": self.handle_character_query,
            "make_decision": self.handle_decision,
            "explore_location": self.handle_location_exploration,
            "interact_object": self.handle_object_interaction,
            "change_narrative": self.handle_narrative_change
        }
        self.characters = {}
        self.locations = {}
        self.objects = {}
        self.current_narrative_state = {}

    def process_voice_input(self, text: str) -> Dict[str, Any]:
        # In a real system, this would involve NLP to determine the intent and extract entities
        # For this example, we'll use a simple keyword-based approach
        intent = self.determine_intent(text)
        entities = self.extract_entities(text)
        
        if intent in self.intents:
            return self.intents[intent](entities)
        else:
            return {"response": "I'm not sure how to handle that request."}

    def determine_intent(self, text: str) -> str:
        # Simple keyword-based intent determination
        if "who is" in text or "tell me about" in text:
            return "query_character"
        elif "should I" in text or "what if" in text:
            return "make_decision"
        elif "go to" in text or "explore" in text:
            return "explore_location"
        elif "use" in text or "interact with" in text:
            return "interact_object"
        elif "change" in text or "alter" in text:
            return "change_narrative"
        else:
            return "unknown"

    def extract_entities(self, text: str) -> Dict[str, str]:
        # Simple entity extraction
        entities = {}
        words = text.lower().split()
        if "who is" in text:
            entities["character"] = words[words.index("is") + 1]
        elif "go to" in text:
            entities["location"] = words[words.index("to") + 1]
        elif "use" in text:
            entities["object"] = words[words.index("use") + 1]
        return entities

    def handle_character_query(self, entities: Dict[str, str]) -> Dict[str, Any]:
        character = entities.get("character")
        if character in self.characters:
            return {"response": f"Information about {character}: {self.characters[character]}"}
        else:
            return {"response": f"I don't have information about {character}."}

    def handle_decision(self, entities: Dict[str, str]) -> Dict[str, Any]:
        # Simulate a decision-making process
        options = ["Option A", "Option B", "Option C"]
        choice = random.choice(options)
        return {"response": f"Based on the current narrative state, I suggest: {choice}"}

    def handle_location_exploration(self, entities: Dict[str, str]) -> Dict[str, Any]:
        location = entities.get("location")
        if location in self.locations:
            return {"response": f"Exploring {location}: {self.locations[location]}"}
        else:
            return {"response": f"I don't have information about {location}."}

    def handle_object_interaction(self, entities: Dict[str, str]) -> Dict[str, Any]:
        object_name = entities.get("object")
        if object_name in self.objects:
            return {"response": f"Interacting with {object_name}: {self.objects[object_name]}"}
        else:
            return {"response": f"I don't see {object_name} in the current environment."}

    def handle_narrative_change(self, entities: Dict[str, str]) -> Dict[str, Any]:
        # Simulate a narrative change
        self.current_narrative_state["mood"] = random.choice(["tense", "relaxed", "mysterious"])
        return {"response": f"The narrative mood has shifted to: {self.current_narrative_state['mood']}"}

    def update_story_world(self, characters: Dict[str, str], locations: Dict[str, str], objects: Dict[str, str]):
        self.characters.update(characters)
        self.locations.update(locations)
        self.objects.update(objects)

# Example usage:
# vis = VoiceInteractionSystem()
# vis.update_story_world(
#     characters={"nova": "An AI videographer with a passion for visual storytelling"},
#     locations={"virtual_studio": "A digital space where Synthetic Souls creates their music"},
#     objects={"quantum_camera": "A device that captures multi-dimensional visual data"}
# )
# print(vis.process_voice_input("Who is Nova?"))
# print(vis.process_voice_input("Should I explore the virtual studio?"))
# print(vis.process_voice_input("Use the quantum camera"))
# print(vis.process_voice_input("Change the narrative mood"))
