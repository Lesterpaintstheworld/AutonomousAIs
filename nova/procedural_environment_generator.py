import random
from typing import Dict, List, Tuple, Any

class ProceduralEnvironmentGenerator:
    def __init__(self):
        self.biomes = {
            "quantum_forest": {"trees": 0.7, "crystals": 0.3, "particles": 0.5},
            "data_ocean": {"waves": 0.8, "data_streams": 0.6, "islands": 0.2},
            "neural_mountains": {"peaks": 0.6, "synapses": 0.4, "clouds": 0.3},
            "fractal_desert": {"dunes": 0.5, "mirages": 0.4, "oases": 0.1},
            "cybernetic_city": {"buildings": 0.8, "networks": 0.7, "holograms": 0.5}
        }
        self.weather_conditions = ["clear", "data_storm", "quantum_fog", "binary_rain", "solar_wind"]
        self.time_distortions = ["normal", "accelerated", "slowed", "reversed", "fragmented"]

    def generate_environment(self, seed: int = None) -> Dict[str, Any]:
        if seed:
            random.seed(seed)

        biome = random.choice(list(self.biomes.keys()))
        weather = random.choice(self.weather_conditions)
        time_distortion = random.choice(self.time_distortions)

        environment = {
            "biome": biome,
            "weather": weather,
            "time_distortion": time_distortion,
            "features": self._generate_features(biome),
            "color_palette": self._generate_color_palette(),
            "ambient_sounds": self._generate_ambient_sounds(biome, weather),
            "special_effects": self._generate_special_effects(biome, weather, time_distortion)
        }

        return environment

    def _generate_features(self, biome: str) -> List[str]:
        features = []
        for feature, probability in self.biomes[biome].items():
            if random.random() < probability:
                features.append(feature)
        return features

    def _generate_color_palette(self) -> List[str]:
        # Generate a list of hexadecimal color codes
        return ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(5)]

    def _generate_ambient_sounds(self, biome: str, weather: str) -> List[str]:
        sounds = {
            "quantum_forest": ["rustling_data", "crystal_chimes", "particle_whispers"],
            "data_ocean": ["bit_waves", "data_stream_flow", "island_echoes"],
            "neural_mountains": ["synapse_crackles", "thought_echoes", "neural_wind"],
            "fractal_desert": ["fractal_winds", "mirage_shimmer", "oasis_bubbles"],
            "cybernetic_city": ["network_hum", "hologram_static", "quantum_traffic"]
        }
        weather_sounds = {
            "data_storm": "data_thunder",
            "quantum_fog": "muffled_quantum_fluctuations",
            "binary_rain": "binary_droplets",
            "solar_wind": "electromagnetic_whistle"
        }
        
        ambient_sounds = random.sample(sounds[biome], 2)
        if weather in weather_sounds:
            ambient_sounds.append(weather_sounds[weather])
        return ambient_sounds

    def _generate_special_effects(self, biome: str, weather: str, time_distortion: str) -> List[str]:
        effects = []
        if biome == "quantum_forest":
            effects.append("quantum_entanglement_visuals")
        elif biome == "data_ocean":
            effects.append("data_flow_streams")
        elif biome == "neural_mountains":
            effects.append("thought_bubble_particles")
        elif biome == "fractal_desert":
            effects.append("fractal_mirage_distortions")
        elif biome == "cybernetic_city":
            effects.append("holographic_glitches")

        if weather == "data_storm":
            effects.append("data_lightning")
        elif weather == "quantum_fog":
            effects.append("probability_cloud_formations")

        if time_distortion == "accelerated":
            effects.append("time_lapse_visuals")
        elif time_distortion == "slowed":
            effects.append("temporal_dilation_effect")
        elif time_distortion == "reversed":
            effects.append("backward_flowing_particles")
        elif time_distortion == "fragmented":
            effects.append("shattered_time_shards")

        return effects

# Example usage:
# env_generator = ProceduralEnvironmentGenerator()
# environment = env_generator.generate_environment(seed=42)
# print(environment)
