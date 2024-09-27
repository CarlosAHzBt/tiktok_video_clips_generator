# tts_api_generator.py

from TTS.api import TTS
import config
from pydub import AudioSegment
from modules.audio_generator import AudioGenerator
import os

class TTSApiGenerator(AudioGenerator):
    def __init__(self, device='cuda', speaker_wav=None, tts_model="tts_models/multilingual/multi-dataset/xtts_v2", **kwargs):
        super().__init__(**kwargs)
        self.device = device
        self.speaker_wav = speaker_wav or config.SPEAKER_WAV
        self.tts_model = tts_model

        # Inicializar el modelo de TTS
        self.tts = TTS(self.tts_model, gpu=True if self.device == "cuda" else False)

    def text_to_speech(self, text):
        """
        Convierte el texto a voz utilizando TTS con clonación de voz.
        """
        print("Convirtiendo texto a voz con clonación de voz en fragmentos...")
        try:
            # Dividir el texto en fragmentos
            text_fragments = self.split_text(text)

            # Lista para almacenar los fragmentos de audio temporales
            audio_segments = []

            # Generar un archivo temporal para cada fragmento
            for i, fragment in enumerate(text_fragments):
                temp_audio_file = f"temp_audio_{i}.wav"
                print(f"Generando audio para el fragmento {i+1}: {fragment[:50]}...")
                self.tts.tts_to_file(
                    text=fragment,
                    speaker_wav=self.speaker_wav,  # Archivo de voz de referencia
                    language=self.language,
                    file_path=temp_audio_file
                )
                audio_segments.append(AudioSegment.from_wav(temp_audio_file))

            # Unir todos los fragmentos de audio
            combined_audio = sum(audio_segments)

            # Guardar el audio combinado en el archivo final
            combined_audio.export(self.audio_file, format="wav")
            print(f"Audio final guardado en {self.get_audio_path()}")

            # Limpiar archivos temporales
            for i in range(len(text_fragments)):
                os.remove(f"temp_audio_{i}.wav")

            if not os.path.isfile(self.audio_file):
                print("Error: El archivo de audio no se ha creado correctamente.")
                raise FileNotFoundError(f"No se encontró el archivo de audio en {self.audio_file}")
        except Exception as e:
            print(f"Error al convertir texto a voz: {e}")
            raise
