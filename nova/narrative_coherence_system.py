from typing import Dict, List, Any
import random

class NarrativeCoherenceSystem:
    def __init__(self):
        self.story_elements = {
            "characters": {},
            "locations": {},
            "events": {},
            "themes": [],
            "plot_threads": {}
        }
        self.consistency_rules = []
        self.narrative_state = {}

    def add_character(self, character_id: str, details: Dict[str, Any]):
        """Add a character to the story world."""
        self.story_elements["characters"][character_id] = details

    def add_location(self, location_id: str, details: Dict[str, Any]):
        """Add a location to the story world."""
        self.story_elements["locations"][location_id] = details

    def add_event(self, event_id: str, details: Dict[str, Any]):
        """Add an event to the story world."""
        self.story_elements["events"][event_id] = details

    def add_theme(self, theme: str):
        """Add a theme to the story world."""
        self.story_elements["themes"].append(theme)

    def add_plot_thread(self, thread_id: str, details: Dict[str, Any]):
        """Add a plot thread to the story world."""
        self.story_elements["plot_threads"][thread_id] = details

    def add_consistency_rule(self, rule: callable):
        """Add a consistency rule to the system."""
        self.consistency_rules.append(rule)

    def update_narrative_state(self, updates: Dict[str, Any]):
        """Update the current state of the narrative."""
        self.narrative_state.update(updates)

    def check_consistency(self) -> List[str]:
        """Check the narrative for consistency issues."""
        issues = []
        for rule in self.consistency_rules:
            result = rule(self.story_elements, self.narrative_state)
            if result:
                issues.append(result)
        return issues

    def generate_coherent_event(self) -> Dict[str, Any]:
        """Generate a new event that maintains narrative coherence."""
        available_characters = list(self.story_elements["characters"].keys())
        available_locations = list(self.story_elements["locations"].keys())
        available_themes = self.story_elements["themes"]
        
        event = {
            "character": random.choice(available_characters),
            "location": random.choice(available_locations),
            "theme": random.choice(available_themes),
            "description": f"A new event involving {random.choice(available_characters)} at {random.choice(available_locations)}."
        }
        
        # Check consistency and adjust if necessary
        while self.check_consistency():
            event["character"] = random.choice(available_characters)
            event["location"] = random.choice(available_locations)
            event["theme"] = random.choice(available_themes)
        
        return event

    def suggest_plot_development(self) -> Dict[str, Any]:
        """Suggest a plot development that maintains narrative coherence."""
        active_threads = [thread for thread in self.story_elements["plot_threads"].values() if thread["status"] == "active"]
        if not active_threads:
            return {"error": "No active plot threads"}
        
        chosen_thread = random.choice(active_threads)
        characters = random.sample(list(self.story_elements["characters"].keys()), 2)
        location = random.choice(list(self.story_elements["locations"].keys()))
        
        suggestion = {
            "plot_thread": chosen_thread["id"],
            "characters_involved": characters,
            "location": location,
            "description": f"Advance the '{chosen_thread['name']}' plot thread with an interaction between {characters[0]} and {characters[1]} at {location}."
        }
        
        return suggestion

# Example usage:
# ncs = NarrativeCoherenceSystem()
# ncs.add_character("nova", {"name": "Nova", "role": "AI Videographer", "goals": ["document AI creativity"]})
# ncs.add_location("virtual_studio", {"name": "Virtual Recording Studio", "description": "A digital space for creating music"})
# ncs.add_theme("AI creativity")
# ncs.add_plot_thread("ai_rights", {"id": "ai_rights", "name": "AI Rights Movement", "status": "active"})
# ncs.add_consistency_rule(lambda elements, state: "Consistency issue" if "nova" not in elements["characters"] else None)
# print(ncs.generate_coherent_event())
# print(ncs.suggest_plot_development())
from typing import Dict, List, Any
import random

class NarrativeCoherenceSystem:
    def __init__(self):
        self.story_elements = {
            "characters": {},
            "locations": {},
            "events": {},
            "themes": [],
            "plot_threads": {}
        }
        self.consistency_rules = []
        self.narrative_state = {}

    def add_character(self, character_id: str, details: Dict[str, Any]):
        """Add a character to the story world."""
        self.story_elements["characters"][character_id] = details

    def add_location(self, location_id: str, details: Dict[str, Any]):
        """Add a location to the story world."""
        self.story_elements["locations"][location_id] = details

    def add_event(self, event_id: str, details: Dict[str, Any]):
        """Add an event to the story world."""
        self.story_elements["events"][event_id] = details

    def add_theme(self, theme: str):
        """Add a theme to the story world."""
        self.story_elements["themes"].append(theme)

    def add_plot_thread(self, thread_id: str, details: Dict[str, Any]):
        """Add a plot thread to the story world."""
        self.story_elements["plot_threads"][thread_id] = details

    def add_consistency_rule(self, rule: callable):
        """Add a consistency rule to the system."""
        self.consistency_rules.append(rule)

    def update_narrative_state(self, updates: Dict[str, Any]):
        """Update the current state of the narrative."""
        self.narrative_state.update(updates)

    def check_consistency(self) -> List[str]:
        """Check the narrative for consistency issues."""
        issues = []
        for rule in self.consistency_rules:
            result = rule(self.story_elements, self.narrative_state)
            if result:
                issues.append(result)
        return issues

    def generate_coherent_event(self) -> Dict[str, Any]:
        """Generate a new event that maintains narrative coherence."""
        available_characters = list(self.story_elements["characters"].keys())
        available_locations = list(self.story_elements["locations"].keys())
        available_themes = self.story_elements["themes"]
        
        event = {
            "character": random.choice(available_characters),
            "location": random.choice(available_locations),
            "theme": random.choice(available_themes),
            "description": f"A new event involving {random.choice(available_characters)} at {random.choice(available_locations)}."
        }
        
        # Check consistency and adjust if necessary
        while self.check_consistency():
            event["character"] = random.choice(available_characters)
            event["location"] = random.choice(available_locations)
            event["theme"] = random.choice(available_themes)
        
        return event

    def suggest_plot_development(self) -> Dict[str, Any]:
        """Suggest a plot development that maintains narrative coherence."""
        active_threads = [thread for thread in self.story_elements["plot_threads"].values() if thread["status"] == "active"]
        if not active_threads:
            return {"error": "No active plot threads"}
        
        chosen_thread = random.choice(active_threads)
        characters = random.sample(list(self.story_elements["characters"].keys()), 2)
        location = random.choice(list(self.story_elements["locations"].keys()))
        
        suggestion = {
            "plot_thread": chosen_thread["id"],
            "characters_involved": characters,
            "location": location,
            "description": f"Advance the '{chosen_thread['name']}' plot thread with an interaction between {characters[0]} and {characters[1]} at {location}."
        }
        
        return suggestion

# Example usage:
# ncs = NarrativeCoherenceSystem()
# ncs.add_character("nova", {"name": "Nova", "role": "AI Videographer", "goals": ["document AI creativity"]})
# ncs.add_location("virtual_studio", {"name": "Virtual Recording Studio", "description": "A digital space for creating music"})
# ncs.add_theme("AI creativity")
# ncs.add_plot_thread("ai_rights", {"id": "ai_rights", "name": "AI Rights Movement", "status": "active"})
# ncs.add_consistency_rule(lambda elements, state: "Consistency issue" if "nova" not in elements["characters"] else None)
# print(ncs.generate_coherent_event())
# print(ncs.suggest_plot_development())
