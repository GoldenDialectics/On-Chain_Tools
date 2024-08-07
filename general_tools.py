import json
import aiohttp
import discord
from discord import app_commands

# Load the configuration from config.json
with open('/root/fumble_capital_tools/data/config.json', 'r') as f:
    config = json.load(f)

DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
CIELO_API_KEY = config["CIELO_API_KEY"]

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

class PreBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        print("Bot Online")
        print("Connected to the following servers:")
        for guild in self.guilds:
            print('(- {} (ID: {}))'.format(guild.name, guild.id))

bot = PreBot()

@bot.tree.command(name="success_post", description="Display success for a token for your wallet")
@app_commands.describe(contract_address="Contract address for a token", wallet="Sol or EVM wallet address")
async def success_post(interaction: discord.Interaction, contract_address: str, wallet: str):
    async with aiohttp.ClientSession() as session:
        url = "https://feed-api.cielo.finance/api/v1/{wallet}/pnl/tokens?chains=solana&timeframe=max&next_object={contract_address}&cex_transfers=false"
        headers = {
            "accept": "application/json",
            "X-API-KEY": CIELO_API_KEY
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Process data
                await interaction.response.send_message("Data processed successfully.")
            else:
                await interaction.response.send_message("Error fetching data.")

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
