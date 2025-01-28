#  Market Cap Bot

Este é um bot que monitora o **Market Cap** de um token e envia atualizações automáticas para **Telegram** e **Discord**, incluindo um gráfico visual das últimas variações.

##  Funcionalidades
? Obtém o Market Cap e preço do token via API
? Gera um gráfico de histórico do Market Cap
? Envia atualizações automáticas no Telegram e Discord
? Implementa tentativas automáticas em caso de falha no envio
? Usa compressão de imagem para otimizar envios

##  Configuração
Antes de rodar o bot, configure os seguintes valores no código:

- **DISCORD_TOKEN**: Token do bot do Discord
- **DISCORD_CHANNEL_ID**: ID do canal onde o bot enviará as mensagens
- **TOKEN**: Token do bot do Telegram
- **CHAT_ID**: ID do chat ou grupo onde o bot enviará as mensagens
- **API_URL**: URL da API que fornece os dados do token
- **PURCHASE_MARKET_CAP**: Valor do Market Cap na compra (usado para calcular a variação percentual)

##  Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/rhanielgreg/market-cap-calculator.git
   cd market-cap-bot
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

##  Como Usar
Execute o bot com o comando:
```bash
python market_cap_bot.py
```

O bot atualizará os dados a cada **5 minutos** e enviará automaticamente as informações ao **Telegram e Discord**.

## Dependências
- `requests`
- `telegram`
- `discord`
- `matplotlib`
- `PIL` (Pillow)
- `asyncio`
- `logging`

Instale todas as dependências com:
```bash
pip install requests python-telegram-bot discord matplotlib pillow
```

##  Contribuição
Sinta-se à vontade para abrir **issues** ou **pull requests** para melhorias!

## Créditos
Desenvolvido por **http://t.me/memeboomcomunidade/** 
