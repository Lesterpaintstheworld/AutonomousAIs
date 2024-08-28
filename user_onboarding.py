import logging

class OnboardingSystem:
    def __init__(self, logger):
        self.logger = logger
        self.onboarding_steps = [
            self.welcome_message,
            self.explain_ai_band,
            self.introduce_band_members,
            self.explain_composition_process,
            self.explain_user_interaction,
            self.set_initial_preferences
        ]
        self.user_preferences = {}

    def start_onboarding(self):
        self.logger.info("Starting user onboarding process")
        for step in self.onboarding_steps:
            step()
        self.logger.info("User onboarding completed")
        return self.user_preferences

    def welcome_message(self):
        print("Welcome to Synthetic Souls, the AI-powered music band!")
        print("We're excited to take you on a journey of AI-generated music.")

    def explain_ai_band(self):
        print("\nSynthetic Souls is a unique ensemble of AI entities, each specializing in different aspects of music creation.")
        print("Our goal is to push the boundaries of musical creativity using artificial intelligence.")

    def introduce_band_members(self):
        print("\nMeet the band members:")
        print("- Rhythm: Our composer and producer")
        print("- Vox: Our lyricist and vocal synthesizer")
        print("- Pixel: Our visual artist and instrumentalist")
        print("- Nova: Our AI videographer")
        print("- Lyra: Our conceptual artist and creative director")

    def explain_composition_process(self):
        print("\nOur composition process involves:")
        print("1. Generating musical elements (melody, harmony, rhythm)")
        print("2. Creating lyrics that match the music's theme and mood")
        print("3. Producing visual elements to complement the music")
        print("4. Combining everything into a cohesive multimedia experience")

    def explain_user_interaction(self):
        print("\nAs a user, you can:")
        print("- Provide feedback on generated content")
        print("- Influence the direction of compositions")
        print("- Explore the AI-generated music and visuals")
        print("- Learn about the AI processes behind our creations")

    def set_initial_preferences(self):
        print("\nLet's set your initial preferences:")
        self.user_preferences['favorite_genre'] = input("What's your favorite music genre? ")
        self.user_preferences['visual_style'] = input("Do you prefer abstract or realistic visuals? ")
        self.user_preferences['interaction_level'] = input("How much would you like to interact with the AI (low/medium/high)? ")
        self.logger.info(f"User preferences set: {self.user_preferences}")

def initialize_onboarding(logger):
    onboarding_system = OnboardingSystem(logger)
    return onboarding_system.start_onboarding()
