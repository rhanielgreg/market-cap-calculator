# ?? Market Cap Bot

Este � um bot que monitora o **Market Cap** de um token e envia atualiza��es autom�ticas para **Telegram** e **Discord**, incluindo um gr�fico visual das �ltimas varia��es.

## ?? Funcionalidades
? Obt�m o Market Cap e pre�o do token via API
? Gera um gr�fico de hist�rico do Market Cap
? Envia atualiza��es autom�ticas no Telegram e Discord
? Implementa tentativas autom�ticas em caso de falha no envio
? Usa compress�o de imagem para otimizar envios

## ?? Configura��o
Antes de rodar o bot, configure os seguintes valores no c�digo:

- **DISCORD_TOKEN**: Token do bot do Discord
- **DISCORD_CHANNEL_ID**: ID do canal onde o bot enviar� as mensagens
- **TOKEN**: Token do bot do Telegram
- **CHAT_ID**: ID do chat ou grupo onde o bot enviar� as mensagens
- **API_URL**: URL da API que fornece os dados do token
- **PURCHASE_MARKET_CAP**: Valor do Market Cap na compra (usado para calcular a varia��o percentual)

## ?? Instala��o

1. Clone o reposit�rio:
   ```bash
   git clone https://github.com/rhanielgreg/market-cap-calculator.git
   cd market-cap-bot
   ```
2. Instale as depend�ncias necess�rias:
   ```bash
   pip install -r requirements.txt
   ```

## ? Como Usar
Execute o bot com o comando:
```bash
python market_cap_bot.py
```

O bot atualizar� os dados a cada **5 minutos** e enviar� automaticamente as informa��es ao **Telegram e Discord**.

## ?? Depend�ncias
- `requests`
- `telegram`
- `discord`
- `matplotlib`
- `PIL` (Pillow)
- `asyncio`
- `logging`

Instale todas as depend�ncias com:
```bash
pip install requests python-telegram-bot discord matplotlib pillow
```

## ?? Contribui��o
Sinta-se � vontade para abrir **issues** ou **pull requests** para melhorias!

## ?? Cr�ditos
Desenvolvido por **@memeboomcomunidade** ??
