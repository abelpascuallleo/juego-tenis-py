# Tenis con Pygame

Un clásico juego de Pong implementado en Python utilizando la librería Pygame. Este proyecto ha sido desarrollado con un enfoque en la claridad del código, la modularidad y la inclusión de características modernas como efectos de partículas y un sistema de menús.

![Captura del Juego](./assets/juego%20tenis.png)

---

## Características Implementadas

A lo largo del desarrollo, se han implementado las siguientes funcionalidades:

- **Jugabilidad Clásica**: Modo de un jugador contra una pala controlada por la IA.
- **Sistema de Dificultad**: Tres niveles de dificultad (Fácil, Medio, Difícil) que ajustan la velocidad de la IA y de la bola.
- **Menús Interactivos**:
  - Menú principal para iniciar el juego.
  - Menú de selección de dificultad.
  - Pantalla de fin de partida con opciones para "Volver a Jugar" o ir al "Menú Principal".
- **Controles por Teclado**: La pala del jugador se controla con las flechas de arriba y abajo (↑/↓).
- **Efectos Visuales**:
  - **Partículas**: Una explosión de partículas se genera cada vez que la bola golpea una pala, añadiendo un feedback visual dinámico.
  - **Estela de la Bola**: La bola deja una estela que se desvanece para dar una mejor sensación de movimiento y velocidad.
- **Sistema de Puntuación**: El primer jugador en alcanzar los 5 puntos gana la partida.
- **Pausa**: El juego se puede pausar en cualquier momento presionando la tecla 'P'.
- **Código Optimizado y Estructurado**:
  - **Programación Orientada a Objetos (POO)**: El juego está dividido en clases (`Ball`, `Paddle`, `Particle`) para una mejor organización.
  - **Carga Eficiente de Recursos**: Las fuentes se cargan una sola vez al inicio para mejorar el rendimiento.
  - **Lógica de Juego sin Bloqueos**: Se usan temporizadores no bloqueantes para los reinicios de la bola, permitiendo que el juego siga siendo responsivo.
- **Empaquetado para Distribución**: El código está preparado para ser empaquetado en un archivo `.exe` con PyInstaller.
- **Pruebas Automatizadas**: Se ha configurado `pytest` con una suite de pruebas inicial para verificar la lógica principal del juego (movimiento, colisiones, etc.).

---

## Instalación y Ejecución

### Opción 1: Ejecutable para Windows

Para usuarios de Windows, la forma más sencilla es descargar el archivo ejecutable. No se necesita instalar Python ni ninguna librería.

**Descargar el ejecutable**
    [Descargar el ejecutable aquí](./dist/main.exe)

### Opción 2: Desde el Código Fuente

Si tienes Python instalado y quieres ejecutar el juego desde el código, sigue estos pasos.

**Requisitos:**

- Python 3.8 o superior
- `pip` (el gestor de paquetes de Python)

**Pasos:**

1. **Clona o descarga el repositorio:**

    ```bash
    # Si usas git
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. **Crea un entorno virtual (recomendado):**

    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    ```

3. **Instala las dependencias:**

    ```bash
    pip install pygame
    ```

4. **Ejecuta el juego:**

    ```bash
    python main.py
    ```

---

## Controles

- **Mover la pala**: Flecha Arriba (↑) / Flecha Abajo (↓)
- **Pausar / Reanudar**: Tecla `P`
- **Salir al Menú Principal**: Tecla `X` (durante una partida)

---

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
