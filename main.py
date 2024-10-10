# main.py

import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"  # Asegúrate de que esta ruta es correcta

import torch
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from modules.text_overlay import TextOverlay
from modules.story_generator import StoryGenerator
from modules.audio_duration_calculator import AudioDurationCalculator
from modules.video_selector import VideoSelector
from modules.music_adder import MusicAdder
import config  # Importar el archivo de configuración
from pydub import AudioSegment

# Selección del motor de TTS
USE_EDGE_TTS = config.USE_EDGE_TTS  # Cambia a False para usar TTS con clonación de voz

if USE_EDGE_TTS:
    from modules.edge_tts_generator import EdgeTTSGenerator as AudioGenerator
else:
    from modules.tts_api_generator import TTSApiGenerator as AudioGenerator

class RedditStoryVideoCreator:
    def __init__(self):
        """
        Inicializa todas las componentes necesarias para crear el video basándose en la configuración.
        """
        # Configurar la clave API de OpenAI
        self.api_key = config.OPENAI_API_KEY

        # Ruta a la carpeta con los clips de video preprocesados
        self.video_dir = config.VIDEO_DIR_PREPROCESSED  # Asegúrate de definir esta variable en config.py

        # Marca de agua
        self.marca_agua = config.WATERMARK_TEXT

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Inicializar componentes
        self.story_generator = StoryGenerator(api_key=self.api_key)

        # Inicializar el generador de audio según el motor seleccionado
        if USE_EDGE_TTS:
            self.audio_generator = AudioGenerator(
                language=config.EDGE_TTS_LANGUAGE,
                audio_file=config.AUDIO_FILE,
                voice_gender=config.EDGE_TTS_VOICE_GENDER
            )
        else:
            self.audio_generator = AudioGenerator(
                device=self.device,
                speaker_wav=config.SPEAKER_WAV_FEMALE,
                language="es",
                audio_file=config.AUDIO_FILE,
                tts_model=config.TTS_MODEL
            )

        self.music_adder = MusicAdder(
            music_dir=config.MUSIC_DIR,
            volume_reduction_db=config.VOLUME_REDUCTION_DB,
        )

        self.video_selector = VideoSelector(video_dir=self.video_dir)

    def run(self, prompts, parts_per_video):
        """
        Ejecuta todo el flujo de creación de videos con la lista de prompts y sus respectivas partes.
        :param prompts: Lista de temas para generar historias.
        :param parts_per_video: Lista con el número de partes para cada video.
        """
        try:
            n_videos = len(prompts)
            for i in range(n_videos):
                prompt_input = prompts[i]
                num_parts = parts_per_video[i]
                print(f"\nGenerando historia para el video {i+1} con el prompt: '{prompt_input}' en {num_parts} partes.")

                if num_parts == 1:
                    # Generar una historia única
                    story, story_file_path = self.story_generator.generate_story(prompt_input)
                    if not story:
                        print(f"No se pudo generar la historia para el video {i+1}. Terminando el proceso.")
                        continue

                    # Procesar la historia normalmente
                    self.process_story(story, story_file_path, i+1)
                else:
                    # Generar historia en múltiples partes
                    story_parts = self.story_generator.generate_story_in_parts(prompt_input, num_parts)
                    if not story_parts:
                        print(f"No se pudo generar la historia para el video {i+1}. Terminando el proceso.")
                        continue

                    for part_num, (story_part, story_file_path) in enumerate(story_parts, start=1):
                        try:
                            # Procesar cada parte de la historia
                            self.process_story(story_part, story_file_path, i+1, part_num)
                        except Exception as e:
                            print(f"Error al procesar la parte {part_num} de la historia para el video {i+1}: {e}")
                            continue

        except Exception as e:
            print(f"\nError durante el proceso de creación de los videos: {e}")

    def process_story(self, story_text, story_file_path, video_number, part_number=None):
        """
        Procesa una historia o parte de ella y genera el video correspondiente.
        :param story_text: Texto de la historia o parte de la historia.
        :param story_file_path: Ruta al archivo de texto donde se guardó la historia.
        :param video_number: Número del video principal.
        :param part_number: Número de la parte dentro de la historia larga (si aplica).
        """
        # Obtener el nombre base del archivo de historia sin extensión
        story_base_name = os.path.splitext(os.path.basename(story_file_path))[0]

        # Definir los nombres de los archivos de audio y video basados en el nombre de la historia
        audio_file = f"{story_base_name}.wav"
        final_output = f"{story_base_name}.mp4"

        # Inicializar el generador de audio con el archivo de audio específico
        if USE_EDGE_TTS:
            audio_generator = AudioGenerator(
                language=config.EDGE_TTS_LANGUAGE,
                audio_file=config.AUDIO_FILE,  # Asegúrate de que esto apunta al archivo correcto
                voice_gender=config.EDGE_TTS_VOICE_GENDER
            )
        else:
            audio_generator = AudioGenerator(
                device=self.device,
                speaker_wav=config.SPEAKER_WAV_FEMALE,
                language="es",
                audio_file=config.AUDIO_FILE,
                tts_model=config.TTS_MODEL
            )

        # Paso 2: Convertir texto a voz (TTS)
        print(f"\nConvirtiendo el texto a voz para el video {video_number}, parte {part_number if part_number else ''}...")
        audio_generator.text_to_speech(story_text)
        narration_audio_path = audio_generator.get_audio_path()
        print(f"Narración guardada en: {narration_audio_path}")

        # Paso 3: Calcular la duración del audio
        print(f"Calculando la duración del audio para el video {video_number}, parte {part_number if part_number else ''}...")
        audio_duration_calculator = AudioDurationCalculator(audio_file=narration_audio_path)
        audio_duration = audio_duration_calculator.get_audio_duration()
        print(f"Duración del audio: {audio_duration:.3f} segundos")

        # Paso 4: Combinar narración con música de fondo
        print("Combinando narración con música de fondo...")
        combined_audio = self.music_adder.add_music_to_audio(
            narration_audio_path=narration_audio_path,
            target_duration=audio_duration
        )
        if combined_audio is None:
            print("Error: El audio combinado es None.")
            return
        print(f"Duración del audio combinado: {len(combined_audio)/1000:.3f} segundos")

        # Guardar el audio combinado como un archivo temporal
        temp_audio_path = f"{story_base_name}_temp_audio.wav"
        combined_audio.export(temp_audio_path, format="wav")
        print(f"Audio combinado guardado en: {temp_audio_path}")

        # Paso 5: Seleccionar y ajustar clips de video que coincidan con la duración del audio
        print("Seleccionando y ajustando clips de video para la duración de la narración...")
        video_clip = self.video_selector.select_video_clips(audio_duration)
        if video_clip is None:
            print("Error: El clip de video seleccionado es None.")
            return
        print("Clips de video seleccionados y ajustados correctamente.")

        # Paso 6: Asignar el audio combinado al video
        print("Asignando audio al video...")
        try:
            audio_clip = AudioFileClip(temp_audio_path)
            video_with_audio = video_clip.set_audio(audio_clip)
            if video_with_audio is None:
                print("Error: video_with_audio es None.")
                return
            print("Audio asignado al video correctamente.")
        except Exception as e:
            print(f"Error al asignar el audio al video: {e}")
            return

        # Paso 7: Añadir la marca de agua (comentar si es necesario)
        print("Añadiendo marca de agua...")
        try:
            text_overlay = TextOverlay(
                text=self.marca_agua,
                fontsize=50,
                color='white',
                position=('center', 'bottom'),
                duration=video_with_audio.duration
            )
            final_video = text_overlay.apply(video_with_audio)
            if final_video is None:
                print("Error: El video final con marca de agua es None.")
                return
            print("Marca de agua añadida correctamente.")
        except Exception as e:
            print(f"Error al añadir la marca de agua: {e}")
            return

        # Paso 8: Exportar el video final
        print(f"Exportando el video final a: {final_output}")
        try:
            # Agregar impresiones de depuración antes de exportar
            print(f"Tipo de final_video: {type(final_video)}")
            print(f"Duración de final_video: {final_video.duration} segundos")
            print(f"FPS de final_video: {final_video.fps}")
            print(f"Tamaño de final_video: {final_video.size}")
            print(f"final_video contiene audio: {final_video.audio is not None}")

            # Exportar el video
            final_video.write_videofile(
                final_output,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=12,
                fps=30,  # Ajustado a un valor estándar
                preset='superfast'  # Comentar o ajustar si es necesario
            )
            print(f"Video final creado: {final_output}")
        except Exception as e:
            print(f"Error durante write_videofile: {e}")
            return
        finally:
            # Liberar recursos
            audio_clip.close()
            video_with_audio.close()
            final_video.close()
            video_clip.close()
            # Eliminar archivo de audio temporal
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

if __name__ == "__main__":
    creator = RedditStoryVideoCreator()
    # Preguntar al usuario cuántos videos quiere generar, asegurándose de que el número sea válido
    while True:
        try:
            num_videos = int(input("Introduce el número de videos a generar: "))
            if num_videos > 0:
                break
            else:
                print("Por favor, introduce un número mayor que 0.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")
    # Recibir N cantidad de prompts y su respectiva cantidad de partes
    prompts = []
    parts_per_video = []
    for i in range(num_videos):
        prompt = input(f"\nIntroduce el tema para la historia de Reddit {i+1}: ")
        prompts.append(prompt)
        while True:
            try:
                num_parts = int(input(f"Introduce el número de partes para la historia de Reddit {i+1}: "))
                if num_parts > 0:
                    parts_per_video.append(num_parts)
                    break
                else:
                    print("Por favor, introduce un número mayor que 0.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número entero.")
    creator.run(prompts, parts_per_video)
