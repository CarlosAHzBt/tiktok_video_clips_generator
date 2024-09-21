# config.py

# Claves API y rutas
OPENAI_API_KEY = 'sk-XXXXXXXX'
OPENAI_MODEL_NAME = 'gpt-4o-mini'  # Actualiza según el modelo que estés utilizando
OPENAI_MAX_TOKENS = 4096 # Máximo número de tokens permitidos por solicitud

VIDEO_DIR = r'C:\Users\carlo\Downloads\Video\oddly satisfaying videos'  # Actualiza esta ruta a la carpeta con los clips de video a utilizar
VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv']
TARGET_RESOLUTION = (576, 1024) # Resolución objetivo para los clips de video (alto, ancho) 576 x 1024 es la comun de los clips descargados de tiktok, pero igualmente si es mayor se ajustara a esta resolucion
VIDEO_SPEED_FACTOR = 1.9  # Factor de velocidad para procesamiento de video

# Audio y Música
AUDIO_FILE = 'audio_story.wav'  # Ruta al archivo de narración (Este se puede dejar tal cual es un archivo que se creará)
SPEAKER_WAV = 'camilahermana.mp3'  # Ruta al archivo de voz de referencia para la clonación de voz TTS
MUSIC_DIR = r'C:\\Users\\carlo\\Desktop\\MusicBackground'  # Ruta a la carpeta de música de fondo
MUSIC_SUPPORTED_FORMATS = ['.mp3', '.wav', '.aac', '.flac', '.m4a']
VOLUME_REDUCTION_DB = 30

# Archivo de Video Final
VIDEO_FILE = 'video_with_audio.mp4'  
FINAL_OUTPUT = 'final_video.mp4' # Ruta al archivo de video final combinado con música
