import aiohttp
import random
import discord
from discord.ext import commands

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = 100
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Nama Pokémon-mu: {self.name} (HP: {self.hp})"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['other']['showdown']['front_default']
                else:
                    return None

    def feed(self):
        self.hp += 20
        return f"Kamu memberi makan {self.name}! HP bertambah, sekarang HP: {self.hp}"


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name  # Dapatkan nama pengguna yang menggunakan perintah
    if author not in Pokemon.pokemons:  # Periksa apakah pengguna ini memiliki Pokémon 
        chance = random.randint(1, 3)  # Menghasilkan angka acak dari 1 hingga 3
        # Buat objek Pokémon tergantung pada nomor acak
        if chance == 1:
            pokemon = Pokemon(author)  # Membuat Pokémon standar
        elif chance == 2:
            pokemon = Wizard(author)  # Membuat Pokémon Wizard 
        elif chance == 3:
            pokemon = Fighter(author)  # Membuat Pokémon Fighter 
        await ctx.send(await pokemon.info())  # Mengirim informasi tentang Pokémon 
        image_url = await pokemon.show_img()  # Mendapatkan URL gambar Pokémon
        if image_url:
            embed = discord.Embed()  # Membuat pesan yang disematkan (embed)
            embed.set_image(url=image_url)  # Menyematkan gambar ke dalam pesan
            await ctx.send(embed=embed)  # Mengirim sematan dengan gambar
        else:
            await ctx.send("Gagal menampilkan gambar Pokémon.")  # Melaporkan kesalahan jika kami tidak dapat memuat gambar Pokémon 
    else:
        await ctx.send("Kamu berhasil mendapatkan Pokémon!")  # Menginformasikan kepada pengguna bahwa Pokémon telah dibuat

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mendapatkan pengguna yang disebutkan dalam pesan
    if target:  # Memeriksa apakah ada pengguna yang disebutkan
        # Memeriksa apakah yang diserang dan yang bertahan memiliki Pokémon 
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Mendapatkan Pokémon pemain bertahan
            attacker = Pokemon.pokemons[ctx.author.name]  # Mendapatkan Pokémon penyerang 
            result = await attacker.attack(enemy)  # Melakukan serangan dan mendapatkan hasilnya
            await ctx.send(result)  # Mengirimkan hasil serangan
        else:
            await ctx.send("Kedua player harus memiliki Pokémon untuk memulai pertempuran!")  # Mengumumkan bahwa setidaknya salah satu petarung tidak memiliki Pokémon 
    else:
        await ctx.send("Tentukan pengguna yang ingin Kalian serang dengan menyebut mereka.")  # Meminta untuk menyebutkan pengguna untuk menyerang

@bot.command()
async def info(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]
        result = await pok.info() # Melakukan serangan dan mendapatkan hasilnya
        await ctx.send(result)

bot.run('TOKEN') 