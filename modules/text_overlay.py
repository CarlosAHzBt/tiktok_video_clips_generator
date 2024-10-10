# modules/text_overlay.py

from moviepy.editor import TextClip, CompositeVideoClip

class TextOverlay:
    def __init__(self, text, fontsize, color, position, duration):
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.position = position
        self.duration = duration

    def apply(self, video_clip):
        try:
            txt_clip = TextClip(self.text, fontsize=self.fontsize, color=self.color)
            txt_clip = txt_clip.set_position(self.position).set_duration(self.duration)
            video_with_text = CompositeVideoClip([video_clip, txt_clip])
            print("Marca de agua aplicada correctamente.")
            return video_with_text
        except Exception as e:
            print(f"Error al crear o aplicar el TextClip: {e}")
            return video_clip  # Retornar el video sin la marca de agua si ocurre un error
