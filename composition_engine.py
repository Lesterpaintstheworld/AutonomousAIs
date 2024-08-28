import logging
from typing import Dict, Any, Tuple
from ai_models import EnhancedAI
from nova.visual_storytelling import create_visual_elements, generate_visual_narrative

class CompositionEngine:
    def __init__(self, enhanced_ai: EnhancedAI, logger: logging.Logger):
        self.enhanced_ai = enhanced_ai
        self.logger = logger

    def generate_section(self, section: str, song_theme: str, song_mood: str, song_style: str) -> Tuple[str, str, str, Dict[str, Any]]:
        self.logger.info(f"Generating section: {section}")
        harmonic_structure = self.enhanced_ai.generate_harmonic_structure(section, song_theme, song_mood, song_style)
        melody = self.enhanced_ai.generate_melody(section, song_theme, song_mood, song_style, harmonic_structure)
        chord_progression = self.enhanced_ai.generate_chord_progression(section, song_theme, song_mood, song_style, harmonic_structure)
        rhythmic_patterns = self.enhanced_ai.generate_rhythmic_patterns(section, song_theme, song_mood, song_style)
        rhythm_spec = self.enhanced_ai.develop_rhythm_specification(section)
        return melody, chord_progression, rhythmic_patterns, rhythm_spec

    def generate_lyrics(self, section: str, song_theme: str, song_mood: str) -> str:
        self.logger.info(f"Generating lyrics for section: {section}")
        lyrics = self.enhanced_ai.generate_lyrics(section, song_theme, song_mood)
        return lyrics

    def compose_quantum_tango(self, song_theme: str, song_mood: str, song_style: str) -> Dict[str, Dict[str, Any]]:
        self.logger.info("Starting composition of Quantum Tango")

        song_sections = [
            {"name": "Intro", "prompt": "Create an otherworldly electronic tango rhythm with quantum-inspired glitch elements."},
            {"name": "Verse", "prompt": "Develop a subtle, intricate beat that blends traditional tango rhythms with quantum-inspired electronic elements."},
            {"name": "Chorus", "prompt": "Intensify the quantum tango beat with added percussion and a more prominent bassline representing quantum entanglement."},
            {"name": "Bridge", "prompt": "Construct a polyrhythmic pattern that combines tango syncopation with quantum-inspired randomness."},
            {"name": "Outro", "prompt": "Craft a gradually simplifying quantum tango beat that echoes elements from the intro, bringing the composition full circle."}
        ]

        composition = {}
        for section in song_sections:
            composition[section['name']] = self.process_song_section(section, song_theme, song_mood, song_style)

        self.logger.info("Quantum Tango composition completed")
        return composition

    def process_song_section(self, section: Dict[str, str], song_theme: str, song_mood: str, song_style: str) -> Dict[str, Any]:
        self.logger.info(f"Processing section: {section['name']}")

        try:
            # Generate musical elements
            melody, chord_progression,rhythmic_patterns, rhythm_spec = self.generate_section(section['name'], song_theme, song_mood, song_style)
            lyrics = self.generate_lyrics(section['name'], song_theme, song_mood)

            # Create visual storytelling elements
            visual_elements = create_visual_elements(self.enhanced_ai, section['name'], melody, chord_progression, rhythmic_patterns, rhythm_spec, lyrics)
            visual_narrative = generate_visual_narrative(visual_elements, lyrics, section['name'])

            # Compile section data
            section_data = {
                'melody': melody,
                'chord_progression': chord_progression,
                'rhythmic_patterns': rhythmic_patterns,
                'rhythm_spec': rhythm_spec,
                'lyrics': lyrics,
                'visual_elements': visual_elements,
                'visual_narrative': visual_narrative
            }

            # Log the results
            self.logger.info(f"Completed processing for section '{section['name']}'")
            self.logger.info(f"Melody: {melody[:50]}...")
            self.logger.info(f"Lyrics: {lyrics[:50]}...")
            self.logger.info(f"Visual Narrative: {visual_narrative[:50]}...")

            return section_data

        except Exception as e:
            self.logger.error(f"Error processing section '{section['name']}': {str(e)}")
            self.logger.exception("Detailed traceback:")
            return {}
