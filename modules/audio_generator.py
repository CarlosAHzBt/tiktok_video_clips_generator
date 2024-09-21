from TTS.api import TTS
import os
import config
from pydub import AudioSegment

class AudioGenerator:
    def __init__(self, device='cuda', speaker_wav=None, language="es", audio_file='audio_story.wav', tts_model="tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        Inicializa el generador de audio (TTS) con clonación de voz.
        """
        self.device = device
        self.speaker_wav = speaker_wav or config.SPEAKER_WAV
        self.language = language
        self.audio_file = audio_file or config.AUDIO_FILE
        self.tts_model = tts_model

        # Inicializar el modelo de TTS
        self.tts = TTS(self.tts_model, gpu=True if self.device == "cuda" else False)

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

    def text_to_speech(self, text):
        """
        Convierte el texto a voz en fragmentos y une los audios generados en un archivo final.
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
            print(f"Audio final guardado en {os.path.abspath(self.audio_file)}")

            # Limpiar archivos temporales
            for i in range(len(text_fragments)):
                os.remove(f"temp_audio_{i}.wav")

            if not os.path.isfile(self.audio_file):
                print("Error: El archivo de audio no se ha creado correctamente.")
                raise FileNotFoundError(f"No se encontró el archivo de audio en {self.audio_file}")
        except Exception as e:
            print(f"Error al convertir texto a voz: {e}")
            raise

    def get_audio_path(self):
        """
        Retorna la ruta al archivo de narración.
        """
        return self.audio_file
