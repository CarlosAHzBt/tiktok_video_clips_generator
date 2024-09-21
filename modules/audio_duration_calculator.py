# modules/audio_duration_calculator.py

import os
from pydub import AudioSegment

class AudioDurationCalculator:
    def __init__(self, audio_file='audio_story.wav'):
        """
        Inicializa el calculador de duración de audio.
        """
        self.audio_file = audio_file

    def get_audio_duration(self):
        """
        Calcula la duración del archivo de audio en segundos.
        """
        print("Calculando la duración del audio...")
        print(f"Intentando abrir el archivo de audio en {self.audio_file}")

        # Verificar si el archivo de audio existe
        if not os.path.isfile(self.audio_file):
            print("Error: El archivo de audio no se ha creado correctamente.")
            raise FileNotFoundError(f"No se encontró el archivo de audio en {self.audio_file}")

        try:
            # Cargar el archivo de audio
            audio = AudioSegment.from_file(self.audio_file)
            duration = len(audio) / 1000.0  # Duración en segundos
            print(f"Duración del audio: {duration} segundos")
            return duration
        except Exception as e:
            print(f"Error al obtener la duración del audio: {e}")
            raise
