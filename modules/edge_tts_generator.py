# edge_tts_generator.py

import config
from pydub import AudioSegment
import edge_tts
import asyncio
from modules.audio_generator import AudioGenerator
import os

class EdgeTTSGenerator(AudioGenerator):
    def __init__(self, voice_gender="female", **kwargs):
        super().__init__(**kwargs)
        self.voice_gender = voice_gender.lower()  # 'male' o 'female'
        self.voice_name = None  # Se asignará más adelante
        self.voice_speed = config.SPEED_VOICE_EDGE_TTS

    async def get_voice_name(self):
        """
        Obtiene el nombre de la voz según el idioma y el género.
        """
        voices = await edge_tts.list_voices()
        # Filtrar voces por idioma y género
        filtered_voices = [voice for voice in voices if voice["Locale"] == self.language and voice["Gender"].lower() == self.voice_gender]

        if not filtered_voices:
            raise ValueError(f"No se encontraron voces para el idioma {self.language} y género {self.voice_gender}")

        # Usar la primera voz encontrada
        self.voice_name = filtered_voices[0]["ShortName"]

    async def text_to_speech_async(self, text):
        """
        Convierte el texto a voz utilizando edge-tts de forma asíncrona.
        """
        print("Convirtiendo texto a voz utilizando edge-tts...")
        try:
            if not self.voice_name:
                await self.get_voice_name()

            # Dividir el texto en fragmentos
            text_fragments = self.split_text(text, max_length=5000)

            # Generar audio y combinar fragmentos
            audio_segments = []
            for i, fragment in enumerate(text_fragments):
                temp_audio_file = f"temp_audio_{i}.mp3"
                communicate = edge_tts.Communicate(text=fragment, voice=self.voice_name)
                await communicate.save(temp_audio_file)
                audio_segments.append(AudioSegment.from_file(temp_audio_file, format="mp3"))

            # Unir todos los fragmentos de audio
            combined_audio = sum(audio_segments)

            # Ajustar la velocidad del audio combinado
            speed_factor = 1.1
            combined_audio = combined_audio.speedup(playback_speed=speed_factor)

            # Guardar el audio combinado en el archivo final
            combined_audio.export(self.audio_file, format="wav")
            print(f"Audio final guardado en {self.get_audio_path()}")

            # Limpiar archivos temporales
            for i in range(len(text_fragments)):
                os.remove(f"temp_audio_{i}.mp3")

            if not os.path.isfile(self.audio_file):
                print("Error: El archivo de audio no se ha creado correctamente.")
                raise FileNotFoundError(f"No se encontró el archivo de audio en {self.audio_file}")
        except Exception as e:
            print(f"Error al convertir texto a voz con edge-tts: {e}")
            raise

    def text_to_speech(self, text):
        asyncio.run(self.text_to_speech_async(text))