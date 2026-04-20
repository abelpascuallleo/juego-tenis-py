# 🎾 Tenis PY

¡Bienvenido a **Tenis PY**! Una versión moderna y altamente optimizada del clásico juego de Pong, construida con Python y Pygame. 

Esta versión ha sido refactorizada para ofrecer una experiencia fluida e independiente de la tasa de frames (Delta Time), una arquitectura modular y efectos visuales mejorados.

---

## ✨ Características

- 🚀 **Delta Time:** Jugabilidad fluida a cualquier FPS.
- 🏗️ **Arquitectura Modular:** Código limpio dividido en `settings`, `entities` y `ui`.
- 🎮 **3 Niveles de Dificultad:** Fácil, Medio y Difícil.
- 🎨 **Efectos Visuales:** Sistema de partículas en colisiones y estela de movimiento para la bola.
- ⌨️ **Controles Intuitivos:** Usa las flechas del teclado para dominar la pista.

---

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/a921-h/juego-tenis-py.git
   cd juego-tenis-py
   ```

2. **Instalar dependencias:**
   Se recomienda usar Python 3.11 o superior.
   ```bash
   pip install -r requirements.txt
   ```
   *Nota: Si usas Python 3.14+, se recomienda `pip install pygame-ce`.*

3. **Ejecutar el juego:**
   ```bash
   python main.py
   ```

---

## 🎮 Cómo Jugar

| Acción | Tecla |
| :--- | :--- |
| **Mover Arriba** | `↑` (Flecha Arriba) |
| **Mover Abajo** | `↓` (Flecha Abajo) |
| **Salir al Menú** | `X` |
| **Pausar** | `P` |

---

## 📁 Estructura del Proyecto

- `main.py`: Punto de entrada y bucle principal del juego.
- `settings.py`: Constantes, colores y configuraciones.
- `entities.py`: Lógica de Sprites (Bola, Palas y Partículas).
- `ui.py`: Gestión de menús y pantallas de estado.
- `assets/`: Recursos gráficos y sonidos.

---

## 📝 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
*Desarrollado con ❤️ por Abel.*
