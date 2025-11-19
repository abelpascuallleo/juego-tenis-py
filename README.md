# Tenis con Pygame

Un juego clásico de Tenis (Pong) desarrollado en Python utilizando la librería Pygame.

![Gameplay del Juego](./Demo%20TenisPY.mp4)

## Características

*   **Modos de Juego**: Juega solo contra la IA o desafía a un amigo en el modo de 2 jugadores.
*   **Niveles de Dificultad**: Elige entre Fácil, Medio y Difícil para ajustar la velocidad de la IA y de la pelota.
*   **Física Mejorada**: El ángulo de rebote de la pelota depende de dónde golpea la pala.
*   **Dificultad Progresiva**: La velocidad de la pelota aumenta con cada golpe durante un rally.
*   **Controles en Partida**: Pausa el juego con la tecla 'P' o sal al menú principal con la tecla 'X'.
*   **Efectos Visuales y Sonoros**: Incluye efectos de sonido para los rebotes y puntos, y un efecto de estela para la pelota.

---

## 🎮 Para Jugadores

### Windows

La forma más sencilla de jugar es descargar el archivo ejecutable (`.exe`) desde nuestra última versión.

1.  Ve a la sección de **Releases**.
2.  Descarga el archivo `Tenis.zip`.
3.  Descomprime el archivo y ejecuta `Tenis.exe`.

### Linux

Para jugar en Linux, necesitarás tener Python y Pygame instalados.

1.  **Instala las dependencias** abriendo una terminal y ejecutando:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    pip3 install pygame
    ```

2.  **Descarga y ejecuta el juego**:
    ```bash
    # Clona el repositorio (necesitas git)
    git clone https://github.com/makinatetanos/juego-tenis-py.git
    cd juego-tenis-py
    python3 main.py
    ```

---

## 👨‍💻 Para Desarrolladores

Si quieres contribuir, modificar o simplemente probar el código, sigue estos pasos.

### Prerrequisitos

*   Python 3
*   Git

### Instalación

1.  **Clona el repositorio** en tu máquina local:
    ```bash
    git clone https://github.com/makinatetanos/juego-tenis-py.git
    cd juego-tenis-py
    ```

2.  **Crea un entorno virtual** (recomendado) y actívalo:
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias** del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta el juego**:
    ```bash
    python main.py
    ```

### Compilar tu propio ejecutable

Puedes generar tu propio archivo `.exe` para Windows usando PyInstaller. Asegúrate de tener los archivos de sonido (`pong.ogg`, `score.ogg`) y el icono (`icon.ico`) en la carpeta raíz.

```bash
pyinstaller --name "Tenis" --onefile --windowed --icon="icon.ico" --add-data "pong.ogg;." --add-data "score.ogg;." main.py
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.