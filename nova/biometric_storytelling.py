import random
from typing import Dict, Any, List

class BiometricStorytelling:
    def __init__(self):
        self.biometric_data = {
            "heart_rate": 0,
            "skin_conductance": 0,
            "brain_waves": {
                "alpha": 0,
                "beta": 0,
                "theta": 0,
                "delta": 0
            }
        }
        self.emotional_states = ["calm", "excited", "focused", "stressed", "relaxed"]
        self.current_emotional_state = "calm"
        self.story_elements = {
            "intensity": 0,
            "pacing": 0,
            "emotional_tone": "neutral"
        }

    def update_biometric_data(self, data: Dict[str, Any]):
        """Update the biometric data with new readings."""
        self.biometric_data.update(data)
        self._analyze_emotional_state()

    def _analyze_emotional_state(self):
        """Analyze the biometric data to determine the current emotional state."""
        # This is a simplified example. In a real system, this would involve more complex analysis.
        if self.biometric_data["heart_rate"] > 100:
            self.current_emotional_state = "excited" if self.biometric_data["skin_conductance"] > 5 else "stressed"
        elif self.biometric_data["heart_rate"] < 60:
            self.current_emotional_state = "relaxed"
        else:
            self.current_emotional_state = "focused" if self.biometric_data["brain_waves"]["beta"] > 20 else "calm"

    def adapt_story(self) -> Dict[str, Any]:
        """Adapt the story based on the current emotional state."""
        if self.current_emotional_state in ["excited", "stressed"]:
            self.story_elements["intensity"] += 0.1
            self.story_elements["pacing"] += 0.1
        elif self.current_emotional_state in ["relaxed", "calm"]:
            self.story_elements["intensity"] -= 0.1
            self.story_elements["pacing"] -= 0.1
        
        self.story_elements["emotional_tone"] = self._get_complementary_emotion()
        
        return self.story_elements

    def _get_complementary_emotion(self) -> str:
        """Get a complementary emotion to balance the current emotional state."""
        if self.current_emotional_state in ["excited", "stressed"]:
            return random.choice(["calming", "soothing"])
        elif self.current_emotional_state in ["relaxed", "calm"]:
            return random.choice(["intriguing", "mysterious"])
        else:
            return random.choice(["neutral", "balanced"])

    def generate_biometric_event(self) -> Dict[str, Any]:
        """Generate a story event based on significant biometric changes."""
        if self.biometric_data["heart_rate"] > 120:
            return {
                "type": "action",
                "description": "A sudden, intense event occurs, causing your heart to race."
            }
        elif self.biometric_data["skin_conductance"] > 10:
            return {
                "type": "suspense",
                "description": "The atmosphere becomes tense, filling you with anticipation."
            }
        elif self.biometric_data["brain_waves"]["theta"] > 30:
            return {
                "type": "revelation",
                "description": "A moment of clarity strikes, revealing a hidden truth."
            }
        else:
            return {
                "type": "ambient",
                "description": "The story continues at a steady pace, reflecting your current state."
            }

    def get_storytelling_suggestions(self) -> List[str]:
        """Provide storytelling suggestions based on the current emotional state and biometric data."""
        suggestions = []
        if self.current_emotional_state == "excited":
            suggestions.append("Introduce a plot twist or unexpected event.")
        elif self.current_emotional_state == "stressed":
            suggestions.append("Offer a moment of respite or introduce a calming element.")
        elif self.current_emotional_state == "focused":
            suggestions.append("Present a complex puzzle or challenge for the user to solve.")
        elif self.current_emotional_state == "relaxed":
            suggestions.append("Deepen character development or explore the story world.")
        elif self.current_emotional_state == "calm":
            suggestions.append("Gradually build tension or introduce a new mystery.")
        
        return suggestions

# Example usage:
# biometric_storyteller = BiometricStorytelling()
# biometric_storyteller.update_biometric_data({"heart_rate": 90, "skin_conductance": 4, "brain_waves": {"alpha": 10, "beta": 15, "theta": 8, "delta": 5}})
# adapted_story = biometric_storyteller.adapt_story()
# event = biometric_storyteller.generate_biometric_event()
# suggestions = biometric_storyteller.get_storytelling_suggestions()
# print(f"Adapted story elements: {adapted_story}")
# print(f"Generated event: {event}")
# print(f"Storytelling suggestions: {suggestions}")
