import os
import discord
from discord.ext import commands, tasks
import gspread
from google.oauth2 import service_account
from discord.ui import Button, View
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_FORMS_CHANNEL_ID = int(os.getenv('GOOGLE_FORMS_CHANNEL_ID'))
ROLE_CHANNEL_ID = int(os.getenv('ROLE_CHANNEL_ID'))
STAFF_SERVER_ID = int(os.getenv('STAFF_SERVER_ID'))

# Configuración del bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurar credenciales de Google
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

class StaffApplicationView(View):
    def __init__(self, application_id, discord_id):
        super().__init__(timeout=None)
        self.application_id = application_id
        self.discord_id = discord_id

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success, custom_id="accept_button")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        user = bot.get_user(int(self.discord_id))
        if not user:
            await interaction.response.send_message("Usuario no encontrado", ephemeral=True)
            return

        try:
            await user.send(
                "¡Felicidades! 🎉\n\n"
                "Has sido aceptado en el equipo de NextGen Studio.\n"
                f"Por favor, ingresa a nuestro servidor de staff (ID: {STAFF_SERVER_ID}) y ve al canal <#{ROLE_CHANNEL_ID}> "
                "para que te otorguemos los roles y ya puedas empezar a trabajar."
            )
        except:
            await interaction.response.send_message("No se pudo enviar el mensaje al usuario", ephemeral=True)
            return

        try:
            spreadsheet = client.open("Solicitudes Staff")
            worksheet = spreadsheet.worksheet("Respuestas")
            cell = worksheet.find(self.application_id)
            worksheet.update_cell(cell.row, cell.col + 10, "ACEPTADO")
            worksheet.update_cell(cell.row, cell.col + 11, str(interaction.user))
        except Exception as e:
            print(f"Error al actualizar Google Sheets: {e}")

        await interaction.response.send_message(f"Solicitud aceptada. Se notificó a {user.mention}")
        self.disable_all_items()
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger, custom_id="reject_button")
    async def reject_button(self, interaction: discord.Interaction, button: Button):
        user = bot.get_user(int(self.discord_id))
        if not user:
            await interaction.response.send_message("Usuario no encontrado", ephemeral=True)
            return

        try:
            await user.send(
                "Lamentamos informarte que tu solicitud para unirte al equipo de Alcraft Studio "
                "ha sido rechazada en esta ocasión.\n\nAgradecemos tu interés y te animamos "
                "a intentarlo nuevamente en el futuro."
            )
        except:
            await interaction.response.send_message("No se pudo enviar el mensaje al usuario", ephemeral=True)
            return

        try:
            spreadsheet = client.open("Solicitudes Staff")
            worksheet = spreadsheet.worksheet("Respuestas")
            cell = worksheet.find(self.application_id)
            worksheet.update_cell(cell.row, cell.col + 10, "RECHAZADO")
            worksheet.update_cell(cell.row, cell.col + 11, str(interaction.user))
        except Exception as e:
            print(f"Error al actualizar Google Sheets: {e}")

        await interaction.response.send_message(f"Solicitud rechazada. Se notificó a {user.mention}")
        self.disable_all_items()
        await interaction.message.edit(view=self)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    check_new_applications.start()
    await bot.tree.sync()

@bot.command()
async def setup(ctx):
    """Configura el sistema de solicitudes de staff"""
    await ctx.send("✅ Sistema de solicitudes de staff configurado correctamente!")

@bot.command()
async def ver_formulario(ctx, application_id: str):
    """Muestra una solicitud específica con botones de acción"""
    try:
        spreadsheet = client.open("Solicitudes Staff")
        worksheet = spreadsheet.worksheet("Respuestas")
        cell = worksheet.find(application_id)
        row = worksheet.row_values(cell.row)
        
        discord_id = row[2] if len(row) > 2 else "No proporcionado"
        
        embed = discord.Embed(title=f"Solicitud de Staff - ID: {application_id}", color=0x00ff00)
        for i, respuesta in enumerate(row):
            embed.add_field(name=f"Pregunta {i+1}", value=respuesta[:1000], inline=False)
        
        view = StaffApplicationView(application_id, discord_id)
        await ctx.send(embed=embed, view=view)
        
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@tasks.loop(hours=1)
async def check_new_applications():
    channel = bot.get_channel(GOOGLE_FORMS_CHANNEL_ID)
    try:
        spreadsheet = client.open("Solicitudes Staff")
        worksheet = spreadsheet.worksheet("Respuestas")
        records = worksheet.get_all_records()
        
        # Asumimos que la columna 'Estado' existe y que tenemos una columna 'ID' y 'ID Discord'
        for idx, record in enumerate(records, start=2):  # start=2 porque la fila 1 es el encabezado
            app_id = record.get('ID', '')
            status = record.get('Estado', 'Pendiente')
            
            if status == 'Pendiente':
                discord_id = record.get('ID Discord', '')
                if not app_id or not discord_id:
                    continue
                
                view = StaffApplicationView(app_id, discord_id)
                embed = discord.Embed(title=f"📄 Nueva Solicitud de Staff - ID: {app_id}", color=0xff9900)
                for key, value in record.items():
                    embed.add_field(name=key, value=str(value)[:256], inline=False)
                
                await channel.send(embed=embed, view=view)
                # Actualizar el estado a 'En revisión' en la hoja
                worksheet.update_cell(idx, worksheet.find("Estado").col, 'En revisión')
                
    except Exception as e:
        print(f"Error al verificar nuevas solicitudes: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)