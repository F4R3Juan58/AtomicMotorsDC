# 🤖 AtomicMotorsDC - Bot de Discord

**AtomicMotorsDC** es un bot de Discord desarrollado en **Python** que incorpora múltiples funcionalidades para la gestión de servidores y la interacción con la comunidad.

---

## 📌 Características
- ⚙️ Arquitectura modular mediante **cogs** (extensiones)
- 💾 Uso de ficheros **JSON** para almacenamiento de datos
- 🔧 Configuración sencilla mediante `config.py`
- 🤝 Comandos personalizables para la comunidad
- 🛠️ Código abierto y fácilmente extensible

---

## 📂 Estructura del proyecto

```
AtomicMotorsDC/
│── cogs/              # Extensiones (módulos) del bot
│── json/              # Archivos de configuración / persistencia
│── config.py          # Configuración del bot (token, prefijo, etc.)
│── main.py            # Punto de entrada principal del bot
```

---

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/F4R3Juan58/AtomicMotorsDC.git
   cd AtomicMotorsDC
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instala las dependencias necesarias (ejemplo con discord.py):
   ```bash
   pip install -r requirements.txt
   ```

4. Configura el archivo `config.py` con tu **token de Discord** y el prefijo de comandos.

5. Ejecuta el bot:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuración

En el archivo `config.py` deberás incluir:

```python
TOKEN = "TU_TOKEN_DE_DISCORD"
PREFIX = "!"
```

---

## 📜 Requisitos
- Python 3.9+
- Librería [discord.py](https://discordpy.readthedocs.io/en/stable/) o compatible
- Token de bot de Discord (desde el [Discord Developer Portal](https://discord.com/developers/applications))

---

## 👨‍💻 Autor
Desarrollado por **Juan Gabriel Gallardo Martín**  
🔗 [GitHub](https://github.com/F4R3Juan58) | [LinkedIn](https://www.linkedin.com/in/juan-gallardo-mart%C3%ADn-5469802a1/)

---
