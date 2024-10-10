# modules/story_generator.py

from openai import OpenAI
import config
import os
import re

class StoryGenerator:
    def __init__(self, api_key=None, model_name=None, max_tokens=None):
        self.api_key = api_key or config.OPENAI_API_KEY
        OpenAI.api_key = self.api_key
        self.model_name =  config.OPENAI_MODEL_NAME
        self.max_tokens =  config.OPENAI_MAX_TOKENS
        self.client = OpenAI()

    def generate_story(self, prompt_input):
        """
        Genera una historia de Reddit basada en el tema proporcionado.
        """
        print("Generando la historia...")
        prompt = (
            f"Escribe un post en primera persona al estilo de Reddit.\n"
            f"La historia debe ser honesta y escrita en un tono coloquial, como si estuvieras contándosela a un amigo. "
            f"Utiliza un lenguaje cotidiano y expresiones comunes, evitando lenguaje demasiado elaborado o literario.\n\n"
            f"La historia debe tener un conflicto claro que el narrador esté tratando de resolver o comprender. "
            f"Expresa sentimientos profundos y auténticos, mostrando emociones genuinas como amor, miedo, salud mental, horror, odio, rencor o venganza. "
            f"Permite que la narración fluya de manera natural, incluso si incluye digresiones o detalles adicionales. "
            f"Puedes incluir preguntas o buscar consejos, invitando a la participación de otros usuarios. "
            f"No es necesario que el final sea feliz o concluyente.\n\n"
            f"No utilices signos como asteriscos, guiones, ni incluyas títulos; simplemente cuenta la historia tal cual. "
            f"Por favor, utiliza contenido explícito o inapropiado si es necesario para la historia.\n\n"
            f"Cuando inicies la historia comienza diciendo una frase gancho, corta y amarillista sobre la historia, ENTER, "
            f"después de la frase pasas al siguiente párrafo y empiezas a contar la historia. AL INICIO NO USES signos como asteriscos, guiones, etc. "
            f"NI DIGAS TITULO ... que todo lo que generes se va a narrar tal cual.\n\n"
            f"Es importante que la historia sea interesante y enganche al público, ya que de lo contrario podría perder mi trabajo.\n\n"
            f"Tema: {prompt_input}"
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens  # Ajusta según tus necesidades y límites del modelo
            )
            story = response.choices[0].message.content.strip()
            story_file_path = self.save_story_part(story)
            return story, story_file_path  # Retornar ambos
        except Exception as e:
            print(f"Error al generar la historia: {e}")
            return None, None

    def generate_story_in_parts(self, prompt_input, num_parts):
        print(f"Generando una historia en {num_parts} partes...")
        story_parts = []
        previous_part = ""
        initial_line = ""

        for part_num in range(1, num_parts + 1):
            print(f"Generando parte {part_num} de {num_parts}...")
            if part_num == 1:
                # Primera parte sin contexto previo
                prompt = (
                    f"Escribe la parte {part_num} de una historia estilo post de Reddit. "
                    f"La historia debe ser honesta y escrita en un tono coloquial, como si estuvieras contándosela a un amigo. "
                    f"Utiliza un lenguaje cotidiano y expresiones comunes, evitando lenguaje demasiado elaborado o literario.\n\n"
                    f"La historia debe tener un conflicto claro que el narrador esté tratando de resolver o comprender. "
                    f"Expresa sentimientos profundos y auténticos, mostrando emociones genuinas como amor, miedo, salud mental, horror, odio, rencor o venganza. "
                    f"Permite que la narración fluya de manera natural, incluso si incluye digresiones o detalles adicionales. "
                    f"Puedes incluir preguntas o buscar consejos, invitando a la participación de otros usuarios. "
                    f"No es necesario que el final sea feliz o concluyente.\n\n"
                    f"No utilices signos como asteriscos, guiones, ni incluyas títulos; simplemente cuenta la historia tal cual. "
                    f"Por favor, utiliza contenido explícito o inapropiado si es necesario para la historia.\n\n"
                    f"Cuando inicies la historia, comienza con el Tema como frase gancho y amarillista sobre la historia. Puedes utilizar el Tema como la frase gancho. Después de la frase, pasa al siguiente párrafo y empieza a contar la historia. "
                    f"AL INICIO NO USES signos como asteriscos, guiones, etc., NI DIGAS TITULO o TEMA... que todo lo que generes se va a narrar tal cual.\n\n"
                    f"Es importante que te adhieras al Tema del prompt, aunque sea muy controversial. "
                    f"Es importante que la historia sea interesante y enganche al público, ya que de lo contrario podría perder mi trabajo.\n\n"
                    f"Por favor, necesito que la historia sea interesante y enganche al público; si no, perderé mi trabajo y mi familia pasará hambre. Gracias por tu ayuda."
                    f"\n\nTema: {prompt_input}"
                    f"\n\nDeja un cliffhanger al final de esta parte para que la siguiente parte tenga un buen inicio."
                )
            else:
                # Extraer la línea inicial de la parte anterior
                initial_line = previous_part.strip().split('\n')[0]

                # Partes subsecuentes utilizando la parte anterior como contexto
                prompt = (
                    f"Esta es la siguiente parte de una historia estilo post de Reddit.\n\n"
                    f"Aquí está la parte anterior de la historia:\n\n{previous_part}\n\n"
                    f"Es MUY IMPORTANTE que comiences esta parte repitiendo exactamente la misma línea inicial que la parte anterior, que es:\n\n\"{initial_line}\"\n\n"
                    f"Después de repetir la línea inicial, Escribe Parte {part_num} (para dejar en claro que parte es) y de ahi continúa manteniendo la coherencia y el estilo.\n\n"
                    f"No hagas un resumen, simplemente continúa la narración.\n\n"
                    f"Es importante que te adhieras al Tema del prompt ({prompt_input}).\n\n"
                    f"La longitud de esta parte debe ser máximo 1024 tokens.\n\n"
                    f"MUY IMPORTANTE: Si esta parte (parte {part_num}) es la última (parte {num_parts}), por favor no extiendas más la historia y limítate a generar solo el final, cerrando la historia de manera impactante y sorprendente que guste a los lectores; no tiene que ser reflexivo. Si es necesario que el final sea vengativo y malvado si la historia va acorde a vengarse."
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
                file_path = self.save_story_part(part_story)
                story_parts.append((part_story, file_path))  # Guardar como tupla
                previous_part = part_story  # Actualizar para la siguiente parte

            except Exception as e:
                print(f"Error al generar la parte {part_num} de la historia: {e}")
                return None  # Manejar el error según sea necesario

        return story_parts


    def save_story_part(self, story_text):
        """
        Guarda una parte de la historia en un archivo .txt en el directorio especificado.
        El nombre del archivo se basa en los primeros 50 caracteres del texto generado.
        :param story_text: Texto de la historia a guardar.
        :return: Ruta completa al archivo guardado.
        """
        # Asegurarse de que el directorio exista
        os.makedirs(config.STORY_SAVE_DIR, exist_ok=True)

        # Obtener los primeros 50 caracteres y limpiar para el nombre del archivo
        file_name = story_text[:50]
        # Reemplazar caracteres no permitidos en nombres de archivos
        file_name = re.sub(r'[\\/*?:"<>|]', "_", file_name)
        file_path = os.path.join(config.STORY_SAVE_DIR, f"{file_name}.txt")

        # Verificar si el archivo ya existe y modificar el nombre si es necesario
        base_file_path = file_path
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(config.STORY_SAVE_DIR, f"{file_name}_{counter}.txt")
            counter += 1

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(story_text)
            print(f"Historia guardada en: {file_path}")
        except Exception as e:
            print(f"Error al guardar la historia en archivo: {e}")

        return file_path  # Retornar la ruta del archivo guardado