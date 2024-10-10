# modules/video_selector.py

import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoSelector:
    def __init__(self, video_dir):
        """
        Inicializa el selector de videos con la carpeta de videos preprocesados.
        """
        self.video_dir = video_dir
        self.video_files = [os.path.join(self.video_dir, f) for f in os.listdir(self.video_dir)
                            if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        if not self.video_files:
            raise ValueError("No se encontraron clips de video en la carpeta especificada.")

    def select_video_clips(self, target_duration):
        """
        Selecciona clips de video preprocesados de forma aleatoria para alcanzar la duración objetivo.
        """
        print("Seleccionando clips de video preprocesados...")
        random.shuffle(self.video_files)
        selected_clips = []
        total_duration = 0

        for video_file in self.video_files:
            try:
                # Cargar el clip de video
                clip = VideoFileClip(video_file)

                # Obtener la duración del clip
                clip_duration = clip.duration
                total_duration += clip_duration

                selected_clips.append(clip)

                if total_duration >= target_duration:
                    break
            except Exception as e:
                print(f"Error al cargar {video_file}: {e}")
                continue

        if not selected_clips:
            raise ValueError("No se pudieron seleccionar clips de video válidos.")

        # Concatenar los clips
        final_clip = concatenate_videoclips(selected_clips, method="compose")

        # Recortar el video final a la duración exacta
        final_clip = final_clip.subclip(0, target_duration)

        # No cerrar los clips individuales aquí para evitar que final_clip pierda acceso a ellos
        # for clip in selected_clips:
        #     clip.close()

        print("Clips de video seleccionados y unidos correctamente.")
        return final_clip
