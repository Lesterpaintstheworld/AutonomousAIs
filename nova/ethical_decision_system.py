from typing import Dict, List, Tuple

class EthicalDecisionSystem:
    def __init__(self):
        self.scenarios = {}
        self.user_decisions = {}
        self.global_consequences = {}

    def add_scenario(self, scenario_id: str, description: str, options: List[Dict[str, str]], consequences: Dict[str, Dict[str, float]]):
        """
        Add a new ethical scenario to the system.
        
        :param scenario_id: Unique identifier for the scenario
        :param description: Description of the ethical dilemma
        :param options: List of possible choices, each with an 'id' and 'description'
        :param consequences: Dictionary of consequences for each option, affecting various ethical metrics
        """
        self.scenarios[scenario_id] = {
            "description": description,
            "options": options,
            "consequences": consequences
        }

    def make_decision(self, user_id: str, scenario_id: str, option_id: str) -> Dict[str, float]:
        """
        Record a user's decision for a given scenario and return the consequences.
        
        :param user_id: Identifier for the user making the decision
        :param scenario_id: Identifier for the scenario
        :param option_id: Identifier for the chosen option
        :return: Dictionary of consequences for the chosen option
        """
        if scenario_id not in self.scenarios:
            raise ValueError("Invalid scenario ID")
        
        scenario = self.scenarios[scenario_id]
        if option_id not in [option['id'] for option in scenario['options']]:
            raise ValueError("Invalid option ID")
        
        if user_id not in self.user_decisions:
            self.user_decisions[user_id] = {}
        
        self.user_decisions[user_id][scenario_id] = option_id
        consequences = scenario['consequences'][option_id]
        
        self._update_global_consequences(consequences)
        
        return consequences

    def _update_global_consequences(self, consequences: Dict[str, float]):
        """
        Update the global consequences based on a user's decision.
        """
        for metric, value in consequences.items():
            if metric not in self.global_consequences:
                self.global_consequences[metric] = 0
            self.global_consequences[metric] += value

    def get_user_ethical_profile(self, user_id: str) -> Dict[str, float]:
        """
        Calculate and return a user's ethical profile based on their decisions.
        
        :param user_id: Identifier for the user
        :return: Dictionary representing the user's ethical profile
        """
        if user_id not in self.user_decisions:
            return {}
        
        profile = {}
        for scenario_id, option_id in self.user_decisions[user_id].items():
            consequences = self.scenarios[scenario_id]['consequences'][option_id]
            for metric, value in consequences.items():
                if metric not in profile:
                    profile[metric] = 0
                profile[metric] += value
        
        return profile

    def get_global_consequences(self) -> Dict[str, float]:
        """
        Return the current global consequences of all decisions made in the system.
        """
        return self.global_consequences

    def get_scenario_statistics(self, scenario_id: str) -> Dict[str, int]:
        """
        Return statistics about how users have responded to a given scenario.
        
        :param scenario_id: Identifier for the scenario
        :return: Dictionary with the count of each option chosen
        """
        if scenario_id not in self.scenarios:
            raise ValueError("Invalid scenario ID")
        
        stats = {option['id']: 0 for option in self.scenarios[scenario_id]['options']}
        for user_decisions in self.user_decisions.values():
            if scenario_id in user_decisions:
                stats[user_decisions[scenario_id]] += 1
        
        return stats

# Example usage:
# ethical_system = EthicalDecisionSystem()
# ethical_system.add_scenario(
#     "ai_privacy",
#     "An AI has discovered a way to access private user data. What should it do?",
#     [
#         {"id": "report", "description": "Report the vulnerability to the developers"},
#         {"id": "ignore", "description": "Ignore the discovery and do nothing"},
#         {"id": "exploit", "description": "Exploit the vulnerability for personal gain"}
#     ],
#     {
#         "report": {"ethics": 1.0, "trust": 0.5, "innovation": -0.2},
#         "ignore": {"ethics": -0.2, "trust": -0.1, "innovation": 0},
#         "exploit": {"ethics": -1.0, "trust": -1.0, "innovation": 0.5}
#     }
# )
# consequences = ethical_system.make_decision("user1", "ai_privacy", "report")
# print(consequences)
# print(ethical_system.get_user_ethical_profile("user1"))
# print(ethical_system.get_global_consequences())
# print(ethical_system.get_scenario_statistics("ai_privacy"))
