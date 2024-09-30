# Generador Automático de Videos para TikTok

## Descripción
Este proyecto es una aplicación orientada a objetos (POO) diseñada para generar automáticamente videos en formato TikTok. Utiliza la API de GPT-4o-mini para la generación de historias, Text-to-Speech (TTS) para la narración, y sincroniza estos elementos con clips de video y música de fondo para crear contenido atractivo y listo para publicar en TikTok.

## Ejemplos
Puedes ver ejemplos de los videos generados en mi perfil de TikTok.

## Características
- **Generación de Historias**: Utiliza la API de GPT-4o-mini para crear historias intrigantes y cautivadoras basadas en temas proporcionados.
- **Conversión de Texto a Voz (TTS) con Múltiples Motores**:
  - **TTS con Clonación de Voz**: Utiliza modelos avanzados de TTS para generar narraciones con clonación de voz personalizada.
  - **Edge-TTS**: Integra el módulo edge-tts para aprovechar las voces de alta calidad de Microsoft Edge, incluyendo voces masculinas y femeninas de México.
- **Selección y Edición de Clips de Video**: Selecciona y procesa clips de video existentes para ajustarlos a la duración de la narración.
- **Adición de Música de Fondo**: Incorpora música de fondo seleccionada aleatoriamente y ajusta su volumen para complementar la narración.
- **Superposición de Marca de Agua**: Añade una marca de agua personalizada (por ejemplo, tu nombre de usuario de TikTok) a lo largo de todo el video para proteger y promocionar tu contenido.
- **Exportación de Videos Finales con Trazabilidad Mejorada**: Los videos generados tienen el mismo nombre que los archivos de texto de las historias, facilitando la organización y el seguimiento del contenido.

## Tecnologías Utilizadas
- Python 3.x
- GPT-4o-mini API para generación de texto
- TTS (Text-to-Speech) para narración
- TTS con Clonación de Voz
- Edge-TTS
- MoviePy para edición de video
- Pydub para manipulación de audio
- ImageMagick para procesamiento de imágenes
- PyTorch para procesamiento en GPU (opcional)
- Edge-TTS para síntesis de voz con las voces de Microsoft Edge

## Instalación

### Requisitos Previos
- **Python 3.10+** instalado en tu sistema.
- **ImageMagick**: Asegúrate de tener ImageMagick instalado y la ruta configurada correctamente en `main.py`.  
  **Nota**: ImageMagick es esencial para la superposición de texto en los videos.
- **FFmpeg**: Asegúrate de tener instalado FFmpeg en tu computadora y configura la ruta en tus variables de entorno.
- **Edge-TTS**: Se instalará como dependencia, pero requiere una conexión a Internet para funcionar correctamente.

### Pasos de Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/CarlosAHzBt/tiktok_video_clips_generator.git
    cd tiktok_video_clips_generator
    ```

2. Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Unix o MacOS:
    source venv/bin/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:
    Renombra `config.py.example` a `config.py` y actualiza las rutas y claves API según tu configuración.  
    Asegúrate de establecer tu clave de API de OpenAI y otros parámetros necesarios.

5. Verifica la instalación de ImageMagick:
    Asegúrate de que la ruta a `magick.exe` en `main.py` es correcta.
    ```python
    os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
    ```

6. Configura la marca de agua:
    En `config.py`, establece el texto que deseas utilizar como marca de agua:
    ```python
    WATERMARK_TEXT = '@TuNombreDeTikTok'  # Reemplaza con tu nombre de usuario
    ```

## Uso

1. **Selecciona el Motor de TTS**:  
   En el archivo `config.py`, establece la variable `USE_EDGE_TTS` según el motor de TTS que desees utilizar:
   ```python
   USE_EDGE_TTS = True  # Usa Edge-TTS
   # USE_EDGE_TTS = False  # Usa TTS con clonación de voz
2. **Ejecuta main.py**

### Sigue las instrucciones en pantalla:
- Introduce el número de videos que deseas generar.
- Proporciona los temas para cada historia de Reddit.
- Especifica el número de partes para cada historia (para historias largas).

### Resultado:
Los videos generados se guardarán en la ubicación especificada en `config.py`.

**Trazabilidad Mejorada**: Cada video tendrá el mismo nombre que el archivo de texto de la historia correspondiente, facilitando la organización.  
Por ejemplo:
- Historia: `Mi_historia_interesante.txt`
- Video: `Mi_historia_interesante.mp4`

---

## Roadmap

### Próximas Mejoras:
- **Soporte para Más Voces en TTS**:  
  Integrar múltiples voces y opciones de idioma para diversificar las narraciones y adaptarse a diferentes audiencias.
- **Mejoras Generales**:  
  - Optimización del rendimiento para reducir el tiempo de procesamiento.
  - Implementación de una interfaz gráfica de usuario (GUI) para facilitar el uso.
  - Añadir opciones de personalización avanzada, como selección de música específica o estilos de edición de video.
  - Integración con APIs de redes sociales para publicar automáticamente los videos generados en plataformas como TikTok.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. **Fork el repositorio.**
2. **Crea una rama para tu feature:**

    ```bash
    git checkout -b feature/nueva-funcionalidad
    ```

3. **Realiza tus cambios y haz commit:**

    ```bash
    git commit -m "Añadir nueva funcionalidad"
    ```

4. **Empuja tus cambios:**

    ```bash
    git push origin feature/nueva-funcionalidad
    ```

5. **Abre un Pull Request.**


## Contacto

Para cualquier consulta o sugerencia, por favor contacta a [tu-email@ejemplo.com](carlos.hb@culiacan.tecnm.mx).

---

¡Gracias por utilizar el Generador Automático de Videos para TikTok! Esperamos que esta herramienta te ayude a crear contenido atractivo y de alta calidad para tus redes sociales.
