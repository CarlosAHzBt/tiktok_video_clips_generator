# main.py

import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"  # Asegúrate de que esta ruta es correcta

import torch
from moviepy.editor import VideoFileClip, AudioFileClip
from modules.story_generator import StoryGenerator
from modules.audio_generator import AudioGenerator
from modules.audio_duration_calculator import AudioDurationCalculator
from modules.video_selector import VideoSelector
from modules.music_adder import MusicAdder
import config  # Importar el archivo de configuración
from pydub import AudioSegment

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
        self.audio_generator = AudioGenerator(
            device=self.device, 
            speaker_wav=config.SPEAKER_WAV,  # Ruta al archivo de voz de referencia
            audio_file=self.audio_file
        )
        self.audio_duration_calculator = AudioDurationCalculator(audio_file=self.audio_file)
        self.video_selector = VideoSelector(video_dir=self.video_dir)
        self.music_adder = MusicAdder(
            music_dir=config.MUSIC_DIR, 
            volume_reduction_db=config.VOLUME_REDUCTION_DB,
            
        )

    def run(self, prompts):
        """
        Ejecuta todo el flujo de creación de videos con la lista de prompts.
        """
        try:
            n_videos = len(prompts)
            for i in range(n_videos):
                # Paso 1: Usar el prompt de la lista
                prompt_input = prompts[i]
                print(f"Generando historia para el video {i+1} con el prompt: {prompt_input}")
                story = self.story_generator.generate_story(prompt_input)
                if not story:
                    print(f"No se pudo generar la historia para el video {i+1}. Terminando el proceso.")
                    continue  # Saltar al siguiente video si no se pudo generar la historia

                # Paso 2: Convertir texto a voz (TTS)
                print(f"Convirtiendo el texto a voz para el video {i+1}...")
                self.audio_generator.text_to_speech(story)

                # Paso 3: Calcular la duración del audio
                print(f"Calculando la duración del audio para el video {i+1}...")
                audio_duration = self.audio_duration_calculator.get_audio_duration()

                # Paso 4: Seleccionar clips de video que coincidan con la duración del audio
                print(f"Seleccionando clips de video para el video {i+1}...")
                video_clip = self.video_selector.select_video_clips(audio_duration)

                # Paso 5: Crear el video con el audio de narración y la música de fondo
                print(f"Creando el video {i+1} con narración y música de fondo...")
                self.create_video_with_audio_and_music(video_clip, i+1)

        except Exception as e:
            print(f"Error durante el proceso de creación de los videos: {e}")

    def create_video_with_audio_and_music(self, video_clip, video_number):
        """
        Combina los clips de video seleccionados con el audio de narración y la música de fondo.
        """
        # Combinar la música de fondo con el audio de narración usando Pydub
        mixed_audio_path = self.music_adder.add_music_to_audio(
            narration_audio_path=self.audio_generator.get_audio_path(),
            target_duration=video_clip.duration
        )

        # Verificar la duración del audio combinado
        mixed_audio = AudioSegment.from_file(mixed_audio_path)
        print(f"Duración del audio combinado: {len(mixed_audio)/1000} segundos")
        assert len(mixed_audio) == int(video_clip.duration * 1000), "La duración del audio combinado no coincide con la duración del video."

        # Asignar el audio combinado al video usando context manager para asegurar el cierre
        try:
            mixed_audio_clip = AudioFileClip(mixed_audio_path)
            final_video = video_clip.set_audio(mixed_audio_clip)
            
            # Exportar el video con narración y música de fondo
            final_output_path = f"{self.final_output}_{video_number}.mp4"  # Nombrar los videos de forma única
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
            mixed_audio = None
            final_video = None
            video_clip.close()
            video_clip = None

        except Exception as e:
            print(f"Error al combinar el video con la narración y la música: {e}")
            raise

        print(f"Video con narración y música de fondo creado: {self.final_output}_{video_number}.mp4")

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
    # Recibir N cantidad de prompts de uno en uno
    prompts = []
    for i in range(num_videos):
        prompt = input(f"Introduce el tema para la historia de Reddit {i+1}: ")
        prompts.append(prompt)
    
      
    creator.run(prompts)