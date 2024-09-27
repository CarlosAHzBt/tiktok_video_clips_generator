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
            f"Cuando inices la historia comienza diciendo una frase gancho corta y amarillista sobre la historia, solo la historia en sí. AL INICIO NO USES signos como asteriscos, guiones, etc. NI DIGAS TITULO ... que todo lo que generes se va a narrar tal cual. "
            f"Por favor, utiliza contenido explícito o inapropiado. "
            f"El final no necesita ser bueno."
            f"Por favor necesito que la historia sea interaste y enganche al publico si no perdere mi trabajo y mi familia pasara hambre. Gracias por tu ayuda."
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


    def generate_story_in_parts(self, prompt_input, num_parts):
        """
        Genera una historia dividida en partes.
        """
        print(f"Generando una historia en {num_parts} partes...")
        story_parts = []
        previous_part = ""

        for part_num in range(1, num_parts + 1):
            print(f"Generando parte {part_num} de {num_parts}...")
            if part_num == 1:
                # Primera parte sin contexto previo
                prompt = (
                    f"Escribe la parte {part_num} de una historia estilo post de Reddit. "
                    f"Debe ser intrigante y cautivadora, con personajes profundos y complejos, "
                    f"y tocar temas universales como amor, miedo, salud mental, horror, odio, rencor, venganza, etc. No utilices palabras complicadas, la historia debe ser dinamica e intrigante "
                    f"Utiliza una narración inmersiva en primera persona con descripciones detalladas. "
                    f"Cuando inices comienza diciendo una frase gancho corta y amarillista sobre la historia, solo la historia en sí. AL INICIO NO USES signos como asteriscos, guiones, etc. NI DIGAS TITULO ... que todo lo que generes se va a narrar tal cual. "
                    f"Por favor, utiliza contenido explícito o inapropiado. "
                    f"El final no necesita ser bueno."
                    f" Por favor necesito que la historia sea interaste y enganche al publico si no perdere mi trabajo y mi familia pasara hambre. Gracias por tu ayuda."
                    f"\n\nTema: {prompt_input}"
                )
            else:
                # Partes subsecuentes utilizando la parte anterior como contexto
                prompt = (
                    f"Aquí está la parte anterior de la historia:\n\n{previous_part}\n\n"
                    f"Continúa la historia en la parte {part_num}, manteniendo la coherencia y el estilo. "
                    f"Cuando inices comienza diciendo la misma frase gancho corta y amarillista que comienza la parte anterior de la historia, genera solo la historia en sí. AL INICIO NO USES signos como asteriscos, guiones, etc. NI DIGAS TITULO ... que todo lo que generes se va a narrar tal cual. "
                    f"Comienza diciendo la frase gancho corta y amarillista seguido de decir  Parte {part_num}"
                    f"No hagas un resumen, simplemente continúa la narración."
                    f" Si esta parte {part_num} es el mismo numero de parte que  la parte final {num_parts} por favor termina la historia con un final impactante y sorprendente. "

                )

            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens
                )
                part_story = response.choices[0].message.content.strip()
                story_parts.append(part_story)
                previous_part = part_story  # Actualizar para la siguiente parte
            except Exception as e:
                print(f"Error al generar la parte {part_num} de la historia: {e}")
                return None  # Manejar el error según sea necesario

        return story_parts