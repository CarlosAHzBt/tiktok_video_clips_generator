# modules/music_adder.py

import os
import random
from pydub import AudioSegment
import config

class MusicAdder:
    def __init__(self, music_dir=config.MUSIC_DIR, volume_reduction_db=config.VOLUME_REDUCTION_DB):
        """
        Inicializa MusicAdder con la carpeta de música y la reducción de volumen deseada.
        """
        self.music_dir = music_dir
        self.volume_reduction_db = volume_reduction_db  # Reducción de volumen en decibelios
        self.music_path = self.select_random_music()
        self.background_music = self.load_and_adjust_music()

    def select_random_music(self):
        """
        Selecciona una canción aleatoria de la carpeta especificada.
        """
        supported_formats = ('.mp3', '.wav', '.aac', '.flac', '.m4a')
        music_files = [
            f for f in os.listdir(self.music_dir)
            if f.lower().endswith(supported_formats)
        ]
        if not music_files:
            raise ValueError(f"No se encontraron archivos de música en la carpeta: {self.music_dir}")
        selected_music = random.choice(music_files)
        music_path = os.path.join(self.music_dir, selected_music)
        print(f"Canción seleccionada: {selected_music}")
        return music_path

    def load_and_adjust_music(self):
        """
        Carga la música seleccionada y ajusta su volumen.
        """
        try:
            music = AudioSegment.from_file(self.music_path)
            # Reducir el volumen
            music = music - self.volume_reduction_db
            print("Música cargada y volumen reducido correctamente.")
            return music
        except Exception as e:
            print(f"Error al cargar o ajustar la música: {e}")
            raise

    def adjust_music_duration(self, target_duration):
        """
        Ajusta la duración de la música para que coincida con la duración del audio.
        - Si la música es más corta, la repite en bucle.
        - Si es más larga, la corta.
        
        :param target_duration: Duración objetivo en segundos.
        :return: Objeto AudioSegment ajustado.
        """
        target_duration_ms = target_duration * 1000  # Pydub trabaja en milisegundos
        if len(self.background_music) < target_duration_ms:
            print("La música es más corta que el audio. Reproduciendo en bucle...")
            loops = int(target_duration_ms // len(self.background_music)) + 1  # Convertir a entero
            self.background_music = self.background_music * loops
        print("Cortando la música para que coincida con la duración objetivo...")
        self.background_music = self.background_music[:int(target_duration_ms)]
        print(f"Duración ajustada de la música: {len(self.background_music)/1000} segundos")
        return self.background_music

    def add_music_to_audio(self, narration_audio_path, target_duration):
        """
        Combina la música de fondo con el audio de narración utilizando Pydub.
        Retorna el audio combinado como un objeto AudioSegment.
        """
        print("Combinando música de fondo con la narración usando Pydub...")
        try:
            # Cargar la narración
            narration = AudioSegment.from_file(narration_audio_path)
            print(f"Narración cargada correctamente. Duración: {len(narration)/1000} segundos")
            
            # Ajustar la duración de la música
            adjusted_music = self.adjust_music_duration(target_duration)
            
            # Combinar la narración y la música
            combined = narration.overlay(adjusted_music)
            print(f"Audio combinado creado. Duración: {len(combined)/1000} segundos")
            
            # Asegurarse de que la duración es exactamente target_duration_ms
            target_duration_ms = target_duration * 1000
            combined = combined[:int(target_duration_ms)]
            print(f"Duración del audio combinado después de ajustes: {len(combined)/1000} segundos")
            
            print("Música de fondo combinada con la narración correctamente.")
            return combined  # Retornar el objeto AudioSegment
        except Exception as e:
            print(f"Error al combinar la música con la narración usando Pydub: {e}")
            raise
