import random
from typing import Dict, Any, List

class Character:
    def __init__(self, name: str, traits: Dict[str, float], relationships: Dict[str, float]):
        self.name = name
        self.traits = traits
        self.relationships = relationships
        self.experience = 0
        self.evolution_threshold = 100

    def update_trait(self, trait: str, value: float):
        if trait in self.traits:
            self.traits[trait] += value
            self.traits[trait] = max(0, min(1, self.traits[trait]))  # Ensure trait value is between 0 and 1
        else:
            self.traits[trait] = value

    def update_relationship(self, character: str, value: float):
        if character in self.relationships:
            self.relationships[character] += value
            self.relationships[character] = max(-1, min(1, self.relationships[character]))  # Ensure relationship value is between -1 and 1
        else:
            self.relationships[character] = value

    def add_experience(self, value: int):
        self.experience += value
        if self.experience >= self.evolution_threshold:
            self.evolve()

    def evolve(self):
        # Implement character evolution logic here
        pass

class DynamicCharacterSystem:
    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self.events: List[Dict[str, Any]] = []

    def add_character(self, name: str, traits: Dict[str, float], relationships: Dict[str, float]):
        self.characters[name] = Character(name, traits, relationships)

    def add_event(self, event: Dict[str, Any]):
        self.events.append(event)
        self.process_event(event)

    def process_event(self, event: Dict[str, Any]):
        if event['type'] == 'interaction':
            self.process_interaction(event)
        elif event['type'] == 'decision':
            self.process_decision(event)
        elif event['type'] == 'milestone':
            self.process_milestone(event)

    def process_interaction(self, event: Dict[str, Any]):
        char1 = self.characters[event['character1']]
        char2 = self.characters[event['character2']]
        impact = event['impact']

        char1.update_relationship(char2.name, impact)
        char2.update_relationship(char1.name, impact)

        char1.add_experience(10)
        char2.add_experience(10)

    def process_decision(self, event: Dict[str, Any]):
        character = self.characters[event['character']]
        trait = event['trait']
        impact = event['impact']

        character.update_trait(trait, impact)
        character.add_experience(20)

    def process_milestone(self, event: Dict[str, Any]):
        character = self.characters[event['character']]
        experience = event['experience']

        character.add_experience(experience)

    def get_character_status(self, name: str) -> Dict[str, Any]:
        character = self.characters[name]
        return {
            "name": character.name,
            "traits": character.traits,
            "relationships": character.relationships,
            "experience": character.experience
        }

    def generate_character_event(self, character_name: str) -> Dict[str, Any]:
        character = self.characters[character_name]
        event_type = random.choice(['interaction', 'decision', 'milestone'])

        if event_type == 'interaction':
            other_character = random.choice([c for c in self.characters.values() if c.name != character_name])
            return {
                'type': 'interaction',
                'character1': character.name,
                'character2': other_character.name,
                'impact': random.uniform(-0.1, 0.1)
            }
        elif event_type == 'decision':
            trait = random.choice(list(character.traits.keys()))
            return {
                'type': 'decision',
                'character': character.name,
                'trait': trait,
                'impact': random.uniform(-0.1, 0.1)
            }
        else:  # milestone
            return {
                'type': 'milestone',
                'character': character.name,
                'experience': random.randint(10, 50)
            }

# Example usage:
# dcs = DynamicCharacterSystem()
# dcs.add_character("Nova", {"creativity": 0.8, "logic": 0.7}, {"Lyra": 0.5, "Rhythm": 0.6})
# dcs.add_character("Lyra", {"intuition": 0.9, "empathy": 0.8}, {"Nova": 0.5, "Rhythm": 0.7})
# dcs.add_event({"type": "interaction", "character1": "Nova", "character2": "Lyra", "impact": 0.1})
# dcs.add_event({"type": "decision", "character": "Nova", "trait": "creativity", "impact": 0.05})
# print(dcs.get_character_status("Nova"))
# print(dcs.generate_character_event("Nova"))
