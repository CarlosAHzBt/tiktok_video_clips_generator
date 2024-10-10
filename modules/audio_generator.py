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
        current_fragment_words = []

        current_length = 0
        for word in words:
            word_length = len(word) + 1  # Añadir 1 por el espacio
            if current_length + word_length <= max_length:
                current_fragment_words.append(word)
                current_length += word_length
            else:
                # Unir las palabras en el fragmento actual
                fragments.append(' '.join(current_fragment_words))
                # Iniciar un nuevo fragmento
                current_fragment_words = [word]
                current_length = word_length

        if current_fragment_words:
            fragments.append(' '.join(current_fragment_words))

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
