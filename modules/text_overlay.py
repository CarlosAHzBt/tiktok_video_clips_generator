# text_overlay.py

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class TextOverlay:
    def __init__(self, text, font='Arial', fontsize=24, color='white', position=('center', 'bottom-30'), duration=None):
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.color = color
        self.position = position
        self.duration = duration

    def apply(self, video_clip):
        # Crear el TextClip
        txt_clip = TextClip(self.text, fontsize=self.fontsize, font=self.font, color=self.color)
        txt_clip = txt_clip.set_position(self.position).set_duration(self.duration or video_clip.duration)

        # Combinar el TextClip con el VideoFileClip
        video_with_text = CompositeVideoClip([video_clip, txt_clip])

        return video_with_text
