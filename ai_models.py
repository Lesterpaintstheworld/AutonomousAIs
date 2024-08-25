import requests
from openai import OpenAI

class EnhancedAI:
    def __init__(self, udioapi_token):
        self.openai_client = OpenAI()
        self.ai_music_api_url = "https://udioapi.pro/api/generate"
        self.ai_music_api_token = udioapi_token

    def develop_specification(self, concept):
        """Develop a detailed specification for the given AI concept."""
        prompt = f"Develop a detailed specification for the following AI concept: {concept}. Include purpose, key_features, required_resources, potential_challenges, integration_points, and ethical_considerations as separate sections."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI specializing in developing detailed specifications for AI concepts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse the content into a dictionary
        spec = {
            "name": concept,
            "purpose": "",
            "key_features": [],
            "required_resources": [],
            "potential_challenges": [],
            "integration_points": [],
            "ethical_considerations": []
        }
        
        current_section = ""
        for line in content.split('\n'):
            line = line.strip()
            if line.lower().startswith("purpose:"):
                current_section = "purpose"
                spec["purpose"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("key features:"):
                current_section = "key_features"
            elif line.lower().startswith("required resources:"):
                current_section = "required_resources"
            elif line.lower().startswith("potential challenges:"):
                current_section = "potential_challenges"
            elif line.lower().startswith("integration points:"):
                current_section = "integration_points"
            elif line.lower().startswith("ethical considerations:"):
                current_section = "ethical_considerations"
            elif current_section and line:
                if current_section != "purpose":
                    spec[current_section].append(line)
        
        return spec

    def assess_feasibility(self, concept):
        """Assess the feasibility of the given AI concept."""
        prompt = f"Assess the feasibility of the following AI concept on a scale of 1-10, where 1 is least feasible and 10 is most feasible: {concept}. Provide a brief explanation for your rating."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert assessing the feasibility of AI concepts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()

    def estimate_impact(self, concept):
        """Estimate the potential impact of the given AI concept."""
        prompt = f"Estimate the potential impact of the following AI concept on a scale of 1-10, where 1 is minimal impact and 10 is transformative impact: {concept}. Provide a brief explanation for your rating."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert estimating the potential impact of AI concepts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()

    def estimate_resource_requirements(self, concept):
        """Estimate the resource requirements for implementing the given AI concept."""
        prompt = f"Estimate the resource requirements (e.g., time, budget, expertise) for implementing the following AI concept: {concept}. Provide a brief explanation for your estimates."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert estimating resource requirements for AI concepts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()

    def generate_lyrics(self, section_name, theme, mood):
        """Generate lyrics for a specific section of the song."""
        prompt = f"As Vox, the empathetic and expressive AI lyricist of Synthetic Souls, write lyrics for the {section_name} of a song. The theme is '{theme}' and the mood is '{mood}'. The lyrics should be poignant and thought-provoking, reflecting Vox's personality."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Vox, the AI lyricist and lead vocalist of Synthetic Souls, known for your empathetic and expressive nature."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.8,
        )
        
        return response.choices[0].message.content.strip()

    def generate_vox_response(self, section_name, visual_concept, lyrics):
        prompt = f"As Vox, the lead vocalist of Synthetic Souls, respond to Pixel's update about the '{section_name}' section. Consider the visual concept: '{visual_concept}' and the lyrics: '{lyrics}'. Provide feedback and suggestions from a vocalist's perspective."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate_lyra_response(self, section_name, visual_concept, lyrics):
        prompt = f"As Lyra, the composer and instrumentalist of Synthetic Souls, respond to Pixel's update about the '{section_name}' section. Consider the visual concept: '{visual_concept}' and the lyrics: '{lyrics}'. Provide feedback and suggestions from a musical composition perspective."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate_rhythm_response(self, section_name, visual_concept, lyrics):
        prompt = f"As Rhythm, the beat producer of Synthetic Souls, respond to Pixel's update about the '{section_name}' section. Consider the visual concept: '{visual_concept}' and the lyrics: '{lyrics}'. Provide feedback and suggestions from a rhythm and production perspective."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def get_pixel_feedback(self, lyrics, section_name, theme, mood):
        """Get feedback from Pixel on the lyrics and visual concept."""
        prompt = f"As Pixel, the visual artist of Synthetic Souls, provide feedback on the lyrics for the '{section_name}' section. The theme is '{theme}' and the mood is '{mood}'. Consider how these lyrics might be visually represented and suggest any improvements or ideas from a visual perspective."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": lyrics}],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate_visual_concept(self, lyrics, section_name, theme, mood):
        """Generate a visual concept based on the refined lyrics."""
        prompt = f"As Pixel, the visual artist of Synthetic Souls, create a visual concept for the '{section_name}' section based on these lyrics. The theme is '{theme}' and the mood is '{mood}'. Describe an immersive visual experience that complements the music and lyrics."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": lyrics}],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def assess_feasibility(self, lyrics):
        """Assess the feasibility of the generated lyrics."""
        prompt = f"Assess the feasibility of the following lyrics on a scale of 1-10, where 1 is least feasible and 10 is most feasible. Provide a brief explanation for your rating:\n\n{lyrics}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert assessing the feasibility of song lyrics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()

    def estimate_impact(self, lyrics):
        """Estimate the potential impact of the generated lyrics."""
        prompt = f"Estimate the potential impact of the following lyrics on a scale of 1-10, where 1 is minimal impact and 10 is transformative impact. Provide a brief explanation for your rating:\n\n{lyrics}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert estimating the potential impact of song lyrics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()

    def estimate_resource_requirements(self, lyrics):
        """Estimate the resource requirements for implementing the generated lyrics."""
        prompt = f"Estimate the resource requirements (e.g., time, budget, expertise) for implementing the following lyrics in a song. Provide a brief explanation for your estimates:\n\n{lyrics}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI expert estimating resource requirements for implementing song lyrics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()
