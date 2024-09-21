# story_generator.py

from openai import OpenAI
import config


class StoryGenerator:
    def __init__(self, api_key=None, model_name=None, max_tokens=None):
        self.api_key = api_key or config.OPENAI_API_KEY
        OpenAI.api_key = self.api_key
        self.model_name = model_name or config.OPENAI_MODEL_NAME
        self.max_tokens = max_tokens or config.OPENAI_MAX_TOKENS
        self.client = OpenAI()
    def generate_story(self, prompt_input):
        """
        Genera una historia de Reddit basada en el tema proporcionado.
        """
        print("Generando la historia...")
        prompt = (
            f"Escribe una historia estilo post de Reddit. "
            f"La historia debe ser intrigante y cautivadora, incluyendo personajes profundos y complejos, "
            f"elementos de misterio o sorpresa, y tocar temas universales con los que los lectores puedan identificarse "
            f"(como amor, miedo, salud mental, horror, odio, rencor, venganza etc.). Utiliza una narración inmersiva en primera persona, "
            f"con descripciones detalladas que permitan al lector sumergirse en la historia. "
            f"Cuando inices la historia comienza diciendo una frase gancho corta y amarillista sobre la historia, solo la historia en sí. "
            f"Por favor, utiliza contenido explícito o inapropiado. "
            f"El final no necesita ser bueno."
            f"Tema: {prompt_input}"
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096  # Ajusta según tus necesidades y límites del modelo
            )
            story = response.choices[0].message.content.strip()
            return story
        except Exception as e:
            print(f"Error al generar la historia: {e}")
            return None
