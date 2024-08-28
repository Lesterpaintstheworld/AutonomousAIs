import random

def generate_fractal_melody(section: str, base_melody: str) -> str:
    """
    Use fractal patterns and algorithms to generate melodic structures.
    """
    fractal_types = [
        "Mandelbrot set",
        "Julia set",
        "Sierpinski triangle",
        "Koch snowflake",
        "Lyapunov fractal"
    ]
    
    chosen_fractal = random.choice(fractal_types)
    
    fractal_melody_description = f"Fractal Melody for {section}: Inspired by the {chosen_fractal}, "
    fractal_melody_description += f"this melody builds upon the base: {base_melody[:50]}... "
    fractal_melody_description += "The fractal algorithm generates self-similar patterns at different scales, "
    fractal_melody_description += "creating a complex, yet coherent melodic structure. "
    fractal_melody_description += "Smaller motifs echo and evolve into larger phrases, mirroring the fractal's recursive nature."
    
    return fractal_melody_description
import random

def generate_fractal_melody(section: str, base_melody: str) -> str:
    """
    Use fractal patterns and algorithms to generate melodic structures.
    """
    fractal_types = [
        "Mandelbrot set",
        "Julia set",
        "Sierpinski triangle",
        "Koch snowflake",
        "Lyapunov fractal"
    ]
    
    chosen_fractal = random.choice(fractal_types)
    
    fractal_melody_description = f"Fractal Melody for {section}: Inspired by the {chosen_fractal}, "
    fractal_melody_description += f"this melody builds upon the base: {base_melody[:50]}... "
    fractal_melody_description += "The fractal algorithm generates self-similar patterns at different scales, "
    fractal_melody_description += "creating a complex, yet coherent melodic structure. "
    fractal_melody_description += "Smaller motifs echo and evolve into larger phrases, mirroring the fractal's recursive nature."
    
    return fractal_melody_description
