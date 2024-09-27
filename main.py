# main.py

import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"  # Asegúrate de que esta ruta es correcta

import torch
from moviepy.editor import VideoFileClip, AudioFileClip
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

        # Ruta a la carpeta con los clips de video
        self.video_dir = config.VIDEO_DIR

        # Archivos de audio y video
        self.audio_file = config.AUDIO_FILE
        self.video_file = config.VIDEO_FILE
        self.final_output = config.FINAL_OUTPUT

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Inicializar componentes
        self.story_generator = StoryGenerator(api_key=self.api_key)

        # Inicializar el generador de audio según el motor seleccionado
        if USE_EDGE_TTS:
            self.audio_generator = AudioGenerator(
                language=config.EDGE_TTS_LANGUAGE,
                audio_file=self.audio_file,
                voice_gender=config.EDGE_TTS_VOICE_GENDER
            )
        else:
            self.audio_generator = AudioGenerator(
                device=self.device,
                speaker_wav=config.SPEAKER_WAV_FEMALE,
                language="es",
                audio_file=self.audio_file,
                tts_model=config.TTS_MODEL
            )

        self.audio_duration_calculator = AudioDurationCalculator(audio_file=self.audio_file)
        self.video_selector = VideoSelector(video_dir=self.video_dir)
        self.music_adder = MusicAdder(
            music_dir=config.MUSIC_DIR,
            volume_reduction_db=config.VOLUME_REDUCTION_DB,
        )

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
                print(f"Generando historia para el video {i+1} con el prompt: {prompt_input} en {num_parts} partes.")

                if num_parts == 1:
                    # Generar una historia única
                    story = self.story_generator.generate_story(prompt_input)
                    if not story:
                        print(f"No se pudo generar la historia para el video {i+1}. Terminando el proceso.")
                        continue

                    # Procesar la historia normalmente
                    self.process_story(story, i+1)
                else:
                    # Generar historia en múltiples partes
                    story_parts = self.story_generator.generate_story_in_parts(prompt_input, num_parts)
                    if not story_parts:
                        print(f"No se pudo generar la historia para el video {i+1}. Terminando el proceso.")
                        continue

                    for part_num, story_part in enumerate(story_parts, start=1):
                        # Procesar cada parte de la historia
                        self.process_story(story_part, i+1, part_num)

        except Exception as e:
            print(f"Error durante el proceso de creación de los videos: {e}")

    def process_story(self, story_text, video_number, part_number=None):
        """
        Procesa una historia o parte de ella y genera el video correspondiente.
        :param story_text: Texto de la historia o parte de la historia.
        :param video_number: Número del video principal.
        :param part_number: Número de la parte dentro de la historia larga (si aplica).
        """
        # Modificar los nombres de los archivos si es una parte
        if part_number:
            audio_file = f"{self.audio_file}_video{video_number}_parte{part_number}.wav"
            final_output = f"{self.final_output}_video{video_number}_parte{part_number}.mp4"
        else:
            audio_file = f"{self.audio_file}_video{video_number}.wav"
            final_output = f"{self.final_output}_{video_number}.mp4"

        # Inicializar el generador de audio con el archivo de audio específico
        if USE_EDGE_TTS:
            audio_generator = AudioGenerator(
                language=config.EDGE_TTS_LANGUAGE,
                audio_file=audio_file,
                voice_gender=config.EDGE_TTS_VOICE_GENDER
            )
        else:
            audio_generator = AudioGenerator(
                device=self.device,
                speaker_wav=config.SPEAKER_WAV_FEMALE,
                language="es",
                audio_file=audio_file,
                tts_model=config.TTS_MODEL
            )

        # Paso 2: Convertir texto a voz (TTS)
        print(f"Convirtiendo el texto a voz para el video {video_number}, parte {part_number if part_number else ''}...")
        audio_generator.text_to_speech(story_text)

        # Paso 3: Calcular la duración del audio
        print(f"Calculando la duración del audio para el video {video_number}, parte {part_number if part_number else ''}...")
        audio_duration_calculator = AudioDurationCalculator(audio_file=audio_file)
        audio_duration = audio_duration_calculator.get_audio_duration()

        # Paso 4: Seleccionar clips de video que coincidan con la duración del audio
        print(f"Seleccionando clips de video para el video {video_number}, parte {part_number if part_number else ''}...")
        video_clip = self.video_selector.select_video_clips(audio_duration)

        # Paso 5: Crear el video con el audio de narración y la música de fondo
        print(f"Creando el video {video_number}, parte {part_number if part_number else ''} con narración y música de fondo...")
        self.create_video_with_audio_and_music(video_clip, audio_file, final_output)

    def create_video_with_audio_and_music(self, video_clip, audio_file, final_output_path):
        """
        Combina los clips de video seleccionados con el audio de narración y la música de fondo.
        :param video_clip: Clip de video seleccionado.
        :param audio_file: Archivo de audio de narración.
        :param final_output_path: Ruta de salida para el video final.
        """
        # Combinar la música de fondo con el audio de narración usando Pydub
        mixed_audio_path = self.music_adder.add_music_to_audio(
            narration_audio_path=audio_file,
            target_duration=video_clip.duration
        )

        # Verificar la duración del audio combinado
        mixed_audio = AudioSegment.from_file(mixed_audio_path)
        audio_duration_ms = len(mixed_audio)  # Duración en milisegundos
        video_duration_ms = int(video_clip.duration * 1000)  # Duración en milisegundos

        print(f"Duración del audio combinado: {audio_duration_ms / 1000} segundos")
        print(f"Duración del video: {video_clip.duration} segundos")

        # Permitir una diferencia de hasta 50 milisegundos
        tolerance = 10  # en milisegundos
        if abs(audio_duration_ms - video_duration_ms) > tolerance:
            raise ValueError("La duración del audio combinado no coincide con la duración del video.")
        else:
            print("Duración del audio combinado coincide con la duración del video dentro de la tolerancia permitida.")

        # Asignar el audio combinado al video
        try:
            mixed_audio_clip = AudioFileClip(mixed_audio_path)
            final_video = video_clip.set_audio(mixed_audio_clip)

            # Exportar el video con narración y música de fondo
            print(f"Exportando el video final a: {final_output_path}")
            final_video.write_videofile(
                final_output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=6,
                fps=30
            )

            # Liberar recursos
            mixed_audio_clip.close()
            final_video.close()
            video_clip.close()

        except Exception as e:
            print(f"Error al combinar el video con la narración y la música: {e}")
            raise

        print(f"Video con narración y música de fondo creado: {final_output_path}")


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
        prompt = input(f"Introduce el tema para la historia de Reddit {i+1}: ")
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
