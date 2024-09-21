# modules/video_selector.py

import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

class VideoSelector:
    def __init__(self, video_dir, target_resolution=(720, 1280)):
        """
        Inicializa el selector de videos con la carpeta y resolución objetivo.
        """
        self.video_dir = video_dir
        self.target_resolution = target_resolution

    def select_video_clips(self, target_duration):
        """
        Selecciona y procesa clips de video para ajustar a la duración objetivo.
        """
        print("Seleccionando y procesando clips de video...")
        video_files = [os.path.join(self.video_dir, f) for f in os.listdir(self.video_dir)
                       if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]

        if not video_files:
            raise ValueError("No se encontraron clips de video en la carpeta especificada.")

        random.shuffle(video_files)
        selected_clips = []
        total_duration = 0

        for video_file in video_files:
            try:
                clip = VideoFileClip(video_file)
                adjusted_duration = clip.duration / 2  # Ajustar por duplicar velocidad
                total_duration += adjusted_duration

                # Redimensionar el clip a la resolución objetivo
                resized_clip = clip.resize(newsize=self.target_resolution)

                # Aplicar efectos (espejo horizontal y velocidad)
                processed_clip = resized_clip.fx(vfx.mirror_x).fx(vfx.speedx, 2)
                selected_clips.append(processed_clip)

                if total_duration >= target_duration:
                    break
            except Exception as e:
                print(f"Error al procesar {video_file}: {e}")
                continue

        if not selected_clips:
            raise ValueError("No se pudieron procesar clips de video válidos.")

        # Concatenar los clips
        final_clip = concatenate_videoclips(selected_clips, method="compose")

        # Recortar el video final a la duración exacta
        final_clip = final_clip.subclip(0, target_duration)

        # Liberar recursos de los clips originales
        for clip in selected_clips:
            clip.close()

        print("Clips de video seleccionados y procesados correctamente.")
        return final_clip
