import requests
from telegram import Bot, InputFile
import asyncio
import logging
import matplotlib.pyplot as plt
import io
import discord
from discord.ext import tasks, commands
from io import BytesIO
from collections import deque
from PIL import Image  # Added for image compression


# Configurações básicas de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações do Discord
DISCORD_TOKEN = "TOKE_DISCORD_BOT"
DISCORD_CHANNEL_ID = ID_DO_CANAL_DO_DISCORD  # ID do canal

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurações do Telegram e API
TOKEN = "TOKEN_TELEGRAM_BOT"
CHAT_ID = "CHAT_ID_TELEGRAM"
API_URL = "API DO TOKEN"
PURCHASE_MARKET_CAP = 30_000  # Market Cap na compra

# Usamos um deque para armazenar os últimos 10 valores de Market Cap
market_caps = deque(maxlen=10)

# Função para obter o Market Cap e o preço do token
def get_market_cap():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        price = float(data["asset"]["dex_usd_price"])
        supply = float(data.get("asset", {}).get("circulating_supply", SUPPLY_DO_TOKEN))  # Exemplo de obtenção dinâmica
        
        return price * supply, price  # Retorna o Market Cap e o preço do token
    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error(f"Erro ao obter Market Cap: {e}")
        return None, None

# Função para comprimir a imagem
def compress_image(image_bytes):
    img = Image.open(image_bytes)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG', optimize=True, quality=85)
    img_byte_arr.seek(0)
    return img_byte_arr

# Função para criar o gráfico
def plot_chart(market_caps):
    plt.figure(figsize=(10,5))
    plt.gca().set_facecolor('#98cc97')  #Troque o RGB pelo desejado
    
    colors = []
    for i in range(1, len(market_caps)):
        if market_caps[i] > market_caps[i-1]:
            colors.append('green')  # Valorização
        elif market_caps[i] == market_caps[i-1]:
            colors.append('blue')   # Estável
        else:
            colors.append('red')    # Queda
    
    for i in range(1, len(market_caps)):
        plt.plot([i-1, i], [market_caps[i-1], market_caps[i]], color=colors[i-1], linewidth=2, marker='o')

    plt.title('📊 Market Cap')
    plt.xlabel('Last updates')
    plt.ylabel('Market Cap (USD)')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)  # DPI REDUZIDO
    buf.seek(0)
    return compress_image(buf)  # COMPRIMIR IMAGEM

async def retry_send_photo(telegram_bot, chat_id, photo, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            await telegram_bot.send_photo(chat_id=chat_id, photo=InputFile(photo, filename='market_cap_chart.png'), caption=message, parse_mode="Markdown")
            return
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning(f"Tentativa {attempt + 1} falhou por timeout ou erro de conexão: {e}")
            if attempt == max_retries - 1:
                logger.error(f"Falha após {max_retries} tentativas.")
                raise
            await asyncio.sleep(5)  # ESPERA ANTES DE NOVA TENTATIVA

async def send_to_discord(discord_bot, message, chart):
    channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
        await channel.send(file=discord.File(fp=chart, filename='market_cap_chart.png'))
    else:
        logger.error("Canal do Discord não encontrado.")

async def main():
    telegram_bot = Bot(TOKEN)
    await bot.start(DISCORD_TOKEN)  # Inicia o bot do Discord

    while True:
        market_cap, token_price = get_market_cap()
        if market_cap is not None and token_price is not None:
            market_caps.append(market_cap)
            
            if len(market_caps) > 1:
                percentage_change = ((market_caps[-1] - market_caps[0]) / market_caps[0]) * 100
            else:
                percentage_change = ((market_cap - PURCHASE_MARKET_CAP) / PURCHASE_MARKET_CAP) * 100 if PURCHASE_MARKET_CAP != 0 else 0
            
            message = "🌍 **Market Cap**: ${:,.2f}\n".format(market_cap)
            message += "📈 **Percentage increase since the last update**: {:+.2f}%\n".format(percentage_change)
            message += "💰 **Token Price**: ${:.6f}\n".format(token_price)
            message += "**bot by @memeboomcomunidade**"
            
            if market_caps:  
                chart = plot_chart(list(market_caps))
            
                try:
                    await retry_send_photo(telegram_bot, CHAT_ID, chart, message)
                    await send_to_discord(bot, message, chart)
                except Exception as e:
                    logger.error(f"Erro ao enviar a foto: {e}")
                    await telegram_bot.send_message(chat_id=CHAT_ID, text="Erro ao enviar o gráfico. Por favor, tente novamente mais tarde.")
            else:
                await telegram_bot.send_message(chat_id=CHAT_ID, text="Ainda não há dados suficientes para o gráfico.")
        else:
            logger.warning("Market Cap ou Preço do Token não disponível.")

        await asyncio.sleep(300)  # A cada 5 minutos

if __name__ == "__main__":
    asyncio.run(main())