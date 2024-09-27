# audio_generator.py

from abc import ABC, abstractmethod
import os

class AudioGenerator(ABC):
    def __init__(self, language="es", audio_file='audio_story.wav'):
        self.language = language
        self.audio_file = audio_file

    def split_text(self, text, max_length=800):
        """
        Divide el texto en fragmentos de aproximadamente 'max_length' caracteres, sin cortar palabras.
        """
        words = text.split()
        fragments = []
        current_fragment = ""

        for word in words:
            if len(current_fragment) + len(word) + 1 <= max_length:
                if current_fragment:
                    current_fragment += " "
                current_fragment += word
            else:
                fragments.append(current_fragment)
                current_fragment = word

        if current_fragment:
            fragments.append(current_fragment)

        return fragments

    @abstractmethod
    def text_to_speech(self, text):
        """
        Convierte el texto a voz y guarda el archivo de audio resultante.
        """
        pass

    def get_audio_path(self):
        """
        Retorna la ruta al archivo de audio generado.
        """
        return os.path.abspath(self.audio_file)
