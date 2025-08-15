# Discord Staff Application Bot
Un bot de Discord que gestiona solicitudes de staff mediante Google Forms, permitiendo revisar, aceptar o rechazar aplicaciones directamente desde Discord con notificaciones automáticas a los solicitantes.
## Características principales
- ✅ **Integración con Google Forms**: Recibe solicitudes en tiempo real
- 📊 **Visualización en Discord**: Muestra aplicaciones completas con embeds
- ✨ **Botones interactivos**: Aceptar/Rechazar con un clic
- 📩 **Notificaciones automáticas**: Mensajes directos a solicitantes
- 📝 **Registro en Google Sheets**: Actualización automática del estado
## Prerrequisitos
1. **Cuentas necesarias:**
   - [Discord Developer Portal](https://discord.com/developers/applications)
   - [Google Cloud Console](https://console.cloud.google.com/)
   - Cuenta de Google con acceso a Google Forms y Sheets
2. **Recursos:**
   - Servidor de Discord para staff
   - Canal dedicado para solicitudes
   - Formulario de Google para aplicaciones
## Configuración
### Paso 1: Configurar Google Cloud
1. Crea un nuevo proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Activa **Google Sheets API** y **Google Drive API**
3. Crea una cuenta de servicio con rol **Editor**
4. Descarga el archivo JSON de credenciales
5. Comparte tu hoja de cálculo con el email de la cuenta de servicio
### Paso 2: Crear el bot de Discord
1. Ve al [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. En la sección "Bot", crea un bot y copia el token
4. Habilita estos intents:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
   - PRESENCE INTENT
### Paso 3: Configurar el formulario de Google
Tu formulario debe incluir al menos estos campos:
1. Nombre completo
2. Correo electrónico
3. ID de Discord
4. Experiencia relevante
5. Por qué quieres unirte al staff
## Instalación
1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/staff-application-bot.git
cd staff-application-bot
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```
3. Coloca tu archivo de credenciales de Google en la carpeta del proyecto (como `credentials.json`)
## Uso
### Comandos disponibles
| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `!setup` | Configura inicialmente el sistema | `!setup` |
| `!ver_formulario <ID>` | Muestra una solicitud específica | `!ver_formulario ABC123` |
| `!solicitud <n°> <respuesta>` | Registra respuesta adicional | `!solicitud 5 Tengo experiencia moderando` |
## Personalización
### Mensajes de notificación
Para modificar los mensajes enviados a los solicitantes, edita estas secciones del código:
**Mensaje de aceptación:**
```python
await user.send("¡Felicidades! 🎉\n\nHas sido aceptado en el equipo...")
```
**Mensaje de rechazo:**
```python
await user.send("Lamentamos informarte que tu solicitud...")
```
### Configuración de Google Sheets
Para cambiar la estructura de la hoja, actualiza:
```python
# En StaffApplicationView
worksheet.update_cell(cell.row, cell.col + 10, "ACEPTADO")
worksheet.update_cell(cell.row, cell.col + 11, str(interaction.user))
```
## Estructura del proyecto
```
staff-application-bot/
├── main.py              # Código principal del bot
├── credentials.json     # Credenciales de Google (ignorado en .gitignore)
├── .env                 # Variables de entorno
├── requirements.txt     # Dependencias
├── README.md            # Este archivo
└── .gitignore           # Archivos a ignorar en Git
```
## Licencia
Este proyecto está bajo la licencia [GNU AGPL V3.0](LICENSE).
