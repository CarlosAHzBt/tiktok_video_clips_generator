# Generador Automático de Videos para TikTok

## Descripción

Este proyecto es una aplicación orientada a objetos (POO) diseñada para generar automáticamente videos en formato TikTok. Utiliza la API de **GPT-4o-mini** para la generación de historias, **Text-to-Speech (TTS)** para la narración, y sincroniza estos elementos con clips de video y música de fondo para crear contenido atractivo y listo para publicar en TikTok.

## Ejemplos

Puedes ver ejemplos de los videos generados en [mi perfil de TikTok](https://www.tiktok.com/@reddit.cc0) 

## Características

- **Generación de Historias:** Utiliza la API de GPT-4o-mini para crear historias intrigantes y cautivadoras basadas en temas proporcionados.
- **Conversión de Texto a Voz (TTS):** Transforma las historias generadas en narraciones de alta calidad utilizando modelos de TTS con clonación de voz.
- **Selección y Edición de Clips de Video:** Selecciona y procesa clips de video existentes para ajustarlos a la duración de la narración.
- **Adición de Música de Fondo:** Incorpora música de fondo seleccionada aleatoriamente y ajusta su volumen para complementar la narración.
- **Exportación de Videos Finales:** Combina todos los elementos y exporta el video final en formato MP4, listo para ser publicado en TikTok.

## Tecnologías Utilizadas

- **Python 3.x**
- **GPT-4o-mini API** para generación de texto
- **TTS (Text-to-Speech)** para narración
- **MoviePy** para edición de video
- **Pydub** para manipulación de audio
- **ImageMagick** para procesamiento de imágenes
- **PyTorch** para procesamiento en GPU (opcional)

## Instalación

### Requisitos Previos

- **Python 3.10+** instalado en tu sistema.
- **ImageMagick:** Asegúrate de tener ImageMagick instalado y la ruta configurada correctamente en `main.py`.
- **FFPMEG** Asegurate de tener instalado FFPMEG en tu computadora y configura la ruta en tus variables de entorno.

### Pasos de Instalación

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu-usuario/generador-videos-tiktok.git
    cd generador-videos-tiktok
    ```

2. **Crea un entorno virtual (opcional pero recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configura las variables de entorno:**

    - Renombra `config.py.example` a `config.py` y actualiza las rutas y claves API según tu configuración.

5. **Verifica la instalación de ImageMagick:**

    Asegúrate de que la ruta a `magick.exe` en `main.py` es correcta.

## Uso

1. **Ejecuta el script principal:**

    ```bash
    python main.py
    ```

2. **Sigue las instrucciones en pantalla:**

    - Introduce el número de videos que deseas generar.
    - Proporciona los temas para cada historia de Reddit.

3. **Resultado:**

    Los videos generados se guardarán en la ubicación especificada en `config.py` con nombres únicos como `final_video_1.mp4`, `final_video_2.mp4`, etc.

## Roadmap

### Próximas Mejoras

1. **Agregar Módulo de Text Overlay:**
    - Implementar una funcionalidad para superponer texto en los videos, permitiendo resaltar partes clave de la narración o añadir títulos y subtítulos.

2. **Soporte para Más Voces en TTS:**
    - Integrar múltiples voces y opciones de idioma para diversificar las narraciones y adaptarse a diferentes audiencias.

3. **Mejoras Generales:**
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

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para cualquier consulta o sugerencia, por favor contacta a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com).

---

¡Gracias por utilizar el Generador Automático de Videos para TikTok! Esperamos que esta herramienta te ayude a crear contenido atractivo y de alta calidad para tus redes sociales.
