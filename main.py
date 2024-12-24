import discord
from discord.ext import commands
import json
import os
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionário de pontos e cargos para cada cargo
pontos = {}
canal_pontos = 1257759036099526758
canal_log = 1320229672000159804
arquivo_pontos = 'pontos.json'

# Definindo os cargos e a quantidade de pontos necessários para cada promoção
cargos_promocao = [
    # Praças: 5 pontos
    {
        "cargo": 1236651771191885835,
        "pontos_necessarios": 5,
        "proximo_cargo": 1236651769191206952
    },  # RC -> Sd-2Cl
    {
        "cargo": 1236651769191206952,
        "pontos_necessarios": 5,
        "proximo_cargo": 1242610569597554758
    },  # Sd-2Cl -> Sd-1Cl
    # Eventos Graduados: 15 pontos
    {
        "cargo": 1242610569597554758,
        "pontos_necessarios": 15,
        "proximo_cargo": 1236651768067264582
    },  # Sd-1Cl -> CB
    {
        "cargo": 1236651768067264582,
        "pontos_necessarios": 15,
        "proximo_cargo": 1236651766762836119
    },  # CB -> 3-Sgt
    {
        "cargo": 1236651766762836119,
        "pontos_necessarios": 15,
        "proximo_cargo": 1236651765441761320
    },  # 3-Sgt -> 2-Sgt
    {
        "cargo": 1236651765441761320,
        "pontos_necessarios": 15,
        "proximo_cargo": 1236651764313489570
    },  # 2-Sgt -> 1-Sgt
    {
        "cargo": 1236651764313489570,
        "pontos_necessarios": 15,
        "proximo_cargo": 1242610477322993685
    },  # 1-Sgt -> Sub-Tnt
    # Eventos Oficiais Subalternos: 30 pontos
    {
        "cargo": 1242610477322993685,
        "pontos_necessarios": 30,
        "proximo_cargo": 1236671534844874873
    },  # Sub-Tnt -> AAO
    {
        "cargo": 1236671534844874873,
        "pontos_necessarios": 30,
        "proximo_cargo": 1236651759447838731
    },  # AAO -> 2-Tnt
    {
        "cargo": 1236651759447838731,
        "pontos_necessarios": 30,
        "proximo_cargo": 1236651758499921981
    },  # 2-Tnt -> 1-Tnt
    # Eventos Oficiais Intermediários: 50 pontos
    {
        "cargo": 1236651758499921981,
        "pontos_necessarios": 50,
        "proximo_cargo": 1236671534844874873
    },  # 1-Tnt -> Cpt
    # Eventos Oficiais Superiores: 70 pontos
    {
        "cargo": 1236671534844874873,
        "pontos_necessarios": 70,
        "proximo_cargo": 1236651753626271774
    },  # Cpt -> Major
    {
        "cargo": 1236651753626271774,
        "pontos_necessarios": 70,
        "proximo_cargo": 1236651751977779220
    },  # Major -> Tn-C
    # Eventos Oficiais Generais: 100 pontos
    {
        "cargo": 1236651751977779220,
        "pontos_necessarios": 100,
        "proximo_cargo": 1236651750417502268
    },  # Tn-C -> Crn
    {
        "cargo": 1236651750417502268,
        "pontos_necessarios": 100,
        "proximo_cargo": 1236651747515039744
    },  # Crn -> GM
    {
        "cargo": 1236651747515039744,
        "pontos_necessarios": 100,
        "proximo_cargo": 1236651745413828698
    },  # GM -> GND
    {
        "cargo": 1236651745413828698,
        "pontos_necessarios": 100,
        "proximo_cargo": 1236651743635570721
    },  # GND -> GNE
    {
        "cargo": 1236651743635570721,
        "pontos_necessarios": 100,
        "proximo_cargo": 1236651738539360289
    },  # GNE -> Marechal
]


# Função para carregar os pontos de um arquivo
def carregar_pontos():
    global pontos
    if os.path.exists(arquivo_pontos):
        with open(arquivo_pontos, 'r') as f:
            try:
                pontos = json.load(f)
                pontos = {
                    int(k): v
                    for k, v in pontos.items()
                }  # Garante que os IDs sejam inteiros
            except json.JSONDecodeError:
                print(
                    "Erro ao decodificar o JSON. Iniciando com pontos vazios.")
                pontos = {}
    else:
        print("Arquivo de pontos não encontrado. Criando um novo.")
        pontos = {}


# Dicionário de cargos e suas respectivas tags, IDs e pontos necessários para a promoção
cargos_pontos = {
    1236651771191885835: {
        "tag": "RC",
        "pontos": 5,
        "proxima_patente": "Sd-2Cl"
    },
    1236651769191206952: {
        "tag": "Sd-2Cl",
        "pontos": 5,
        "proxima_patente": "Sd-1Cl"
    },
    1242610569597554758: {
        "tag": "Sd-1Cl",
        "pontos": 15,
        "proxima_patente": "CB"
    },
    1236651768067264582: {
        "tag": "CB",
        "pontos": 15,
        "proxima_patente": "3-Sgt"
    },
    1236651766762836119: {
        "tag": "3-Sgt",
        "pontos": 15,
        "proxima_patente": "2-Sgt"
    },
    1236651765441761320: {
        "tag": "2-Sgt",
        "pontos": 15,
        "proxima_patente": "1-Sgt"
    },
    1236651764313489570: {
        "tag": "1-Sgt",
        "pontos": 15,
        "proxima_patente": "Sub-Tnt"
    },
    1242610477322993685: {
        "tag": "Sub-Tnt",
        "pontos": 30,
        "proxima_patente": "AAO"
    },
    1236671534844874873: {
        "tag": "AAO",
        "pontos": 30,
        "proxima_patente": "2-Tnt"
    },
    1236651759447838731: {
        "tag": "2-Tnt",
        "pontos": 30,
        "proxima_patente": "1-Tnt"
    },
    1236651758499921981: {
        "tag": "1-Tnt",
        "pontos": 30,
        "proxima_patente": "Cpt"
    },
    1236671534844874873: {
        "tag": "Cpt",
        "pontos": 50,
        "proxima_patente": "Major"
    },
    1236651753626271774: {
        "tag": "Major",
        "pontos": 70,
        "proxima_patente": "Tn-C"
    },
    1236651751977779220: {
        "tag": "Tn-C",
        "pontos": 70,
        "proxima_patente": "Crn"
    },
    1236651750417502268: {
        "tag": "Crn",
        "pontos": 100,
        "proxima_patente": "GM"
    },
    1236651747515039744: {
        "tag": "GM",
        "pontos": 100,
        "proxima_patente": "GND"
    },
    1236651745413828698: {
        "tag": "GND",
        "pontos": 100,
        "proxima_patente": "GNE"
    },
    1236651743635570721: {
        "tag": "GNE",
        "pontos": 100,
        "proxima_patente": "Marechal"
    },
    1236651738539360289: {
        "tag": "Marechal",
        "pontos": 100,
        "proxima_patente": None
    }
}


# Função para adicionar a nova tag (cargo) ao usuário e remover o cargo anterior
async def adicionar_tag(usuario, pontos_usuario, guild):
    # Verifica se o usuário já possui o cargo RC, que não precisa de verificação nem alteração
    if any(role.name == "RC" for role in usuario.roles):
        print(
            f'{usuario.name} já possui o cargo RC, ele não precisa de promoção e não será alterado.'
        )
        return pontos_usuario  # Retorna os pontos sem alteração, pois o RC não será promovido

    for id_cargo, info in cargos_pontos.items():
        if pontos_usuario >= info[
                "pontos"]:  # Verifica se o usuário atingiu os pontos necessários
            proxima_tag = info["proxima_patente"]
            if proxima_tag:
                cargo_proximo = discord.utils.get(guild.roles,
                                                  name=proxima_tag)

                # Verifica se o usuário já possui o cargo anterior, e remove se tiver
                cargo_atual = discord.utils.get(guild.roles, id=id_cargo)
                if cargo_atual in usuario.roles:
                    await usuario.remove_roles(cargo_atual)
                    print(
                        f'{usuario.name} teve o cargo {cargo_atual.name} removido.'
                    )

                # Adiciona o novo cargo (tag), caso o usuário ainda não tenha
                if cargo_proximo and cargo_proximo not in usuario.roles:
                    await usuario.add_roles(cargo_proximo)
                    print(f'{usuario.name} recebeu a tag {proxima_tag}')

                    # Envia mensagem no canal específico
                    canal = guild.get_channel(1236651820391202886)
                    if canal:
                        await canal.send(
                            f'🎉 {usuario.mention} foi promovido para **{proxima_tag}**!\n'
                            'Use `!adicionar_tag` para receber sua nova tag.')

                    # Reseta os pontos do usuário após a promoção (caso desejado)
                    pontos_usuario = 0
                    return pontos_usuario  # Retorna os pontos resetados


# Função para salvar os pontos no arquivo
def salvar_pontos():
    with open(arquivo_pontos, 'w') as f:
        json.dump(pontos, f, indent=4)


async def verificar_promocao(usuario, guild):
    global pontos
    pontos_usuario = pontos.get(usuario.id, 0)

    # Verifica os cargos e evita a promoção se o usuário já tem o cargo mais alto
    for cargo_info in cargos_promocao:
        if pontos_usuario >= cargo_info["pontos_necessarios"]:
            # Verifica se o usuário tem o cargo atual
            cargo_atual = discord.utils.get(guild.roles,
                                            id=cargo_info["cargo"])
            cargo_proximo = discord.utils.get(guild.roles,
                                              id=cargo_info["proximo_cargo"])

            # Evita promover para um cargo superior se já tiver o cargo correto
            if cargo_atual and cargo_proximo:
                if cargo_atual in usuario.roles and cargo_proximo not in usuario.roles:
                    # Promove o usuário para o cargo superior
                    await usuario.remove_roles(cargo_atual)
                    await usuario.add_roles(cargo_proximo)
                    print(
                        f"{usuario.name} foi promovido para {cargo_proximo.name}"
                    )

                    # Envia mensagem no canal específico
                    canal = guild.get_channel(1236651820391202886)
                    if canal:
                        await canal.send(
                            f'🎉 {usuario.mention} foi promovido para **{cargo_proximo.name}**!\n'
                            'Use `!adicionar_tag` para receber sua nova tag.')

                    # Resetar os pontos após a promoção
                    pontos[
                        usuario.
                        id] = pontos_usuario - cargo_info["pontos_necessarios"]
                    salvar_pontos()  # Salva os pontos após a promoção
                    break  # Só promove uma vez por vez


@bot.event
async def on_message(message):
    if message.channel.id == canal_pontos and message.mentions:
        # Verifica se a mensagem anterior continha o registro de evento não oficial
        historico = [msg async for msg in message.channel.history(limit=5)
                     ]  # Busca as últimas 5 mensagens

        registro_evento = any(
            "REGISTRO DE EVENTO NÃO OFICIAL" in msg.content.upper()
            for msg in historico if msg.author == message.author)

        for usuario in message.mentions:
            if usuario.id not in pontos:
                pontos[usuario.id] = 0

            pontos_anterior = pontos[usuario.id]

            if registro_evento:
                pontos[usuario.id] += 0.5
                pontos[usuario.id] = round(pontos[usuario.id], 1)
            else:
                pontos[usuario.id] += 1

            salvar_pontos()

            if pontos[usuario.id] > pontos_anterior:
                await verificar_promocao(usuario, message.guild)

        log_channel = bot.get_channel(canal_log)
        if log_channel:
            pontos_str = "0.5" if registro_evento else "1"
            await log_channel.send(
                f'{pontos_str} ponto(s) adicionado(s) para: {", ".join([u.name for u in message.mentions])} por {message.author.name}'
            )

    await bot.process_commands(message)


# Evento quando o bot está pronto
@bot.event
async def on_ready():
    print("Bot está pronto!")
    carregar_pontos()


# Comando para verificar os pontos de um usuário
@bot.command()
async def pontos(ctx, usuario: discord.User = None):
    if usuario is None:
        usuario = ctx.author
    pontos_usuario = pontos.get(usuario.id, 0)
    await ctx.send(f'{usuario.name} tem {pontos_usuario} ponto(s).')


@bot.command(name="addpontos")
async def add_pontos(ctx, usuario: discord.User, pontos_adicionais: int):
    """
    Comando para adicionar pontos a um usuário.
    Exemplo: !addpontos @usuario 10
    """
    # Verifica se o usuário é válido e se o valor de pontos é positivo
    if pontos_adicionais <= 0:
        await ctx.send("Você precisa adicionar um valor positivo de pontos.")
        return

    # Adiciona os pontos ao usuário
    if usuario.id not in pontos:
        pontos[usuario.id] = 0

    pontos[usuario.id] += pontos_adicionais
    salvar_pontos()  # Salva os pontos no arquivo ou banco de dados

    # Verifica se o usuário foi promovido
    await verificar_promocao(usuario, ctx.guild)

    # Mensagem de confirmação
    await ctx.send(
        f'{pontos_adicionais} pontos foram adicionados a {usuario.name}.')


@bot.command()
async def adicionar_tag(ctx):
    usuario = ctx.author  # O usuário que chamou o comando
    guild = ctx.guild  # A guilda (servidor) onde o comando foi chamado

    # Dicionário de cargos e suas respectivas tags e IDs
    cargos_pontos = {
        1236651771191885835: "RC",
        1236651769191206952: "Sd-2Cl",
        1242610569597554758: "Sd-1Cl",
        1236651768067264582: "CB",
        1236651766762836119: "3-Sgt",
        1236651765441761320: "2-Sgt",
        1236651764313489570: "1-Sgt",
        1242610477322993685: "Sub-Tnt",
        1236671534844874873: "AAO",
        1236651759447838731: "2-Tnt",
        1236651758499921981: "1-Tnt",
        1236671534844874873: "Cpt",
        1236651753626271774: "Major",
        1236651751977779220: "Tn-C",
        1236651750417502268: "Crn",
        1236651747515039744: "GM",
        1236651745413828698: "GND",
        1236651743635570721: "GNE",
        1236651738539360289: "Marechal",
    }

    # IDs dos cargos específicos que definem [1º], [2º] ou [3º]
    cargos_especiais = {
        1272297208707940352: "[1º]",  # Cargo para tag [1º]
        1272297390547931189: "[2º]",  # Cargo para tag [2º]
        1254822832982982757: "[3º]"  # Cargo para tag [3º]
    }

    # Verifica se o usuário tem algum cargo no dicionário
    cargo_usuario = None
    grau_usuario = ""

    # Percorre os cargos do usuário
    for cargo in usuario.roles:
        if cargo.id in cargos_pontos:
            cargo_usuario = cargos_pontos[cargo.id]

        if cargo.id in cargos_especiais:
            grau_usuario = cargos_especiais[
                cargo.id]  # Define o grau [1º], [2º] ou [3º]

    # Se não encontrar um cargo no dicionário, envia uma mensagem
    if not cargo_usuario:
        await ctx.send(
            f"{usuario.name}, não tem um cargo com uma tag correspondente.")
        return

    # Se for RC, não altera o apelido
    if cargo_usuario == "RC":
        await ctx.send(
            f"{usuario.name}, você já tem o cargo RC, não precisa alterar o apelido."
        )
        return

    # Se o usuário não tiver grau (1º, 2º, 3º), deixa vazio
    if not grau_usuario:
        grau_usuario = "[ ]"

    # Formata o novo apelido
    novo_apelido = f"{grau_usuario} - [{cargo_usuario}] {usuario.name}"

    # Tenta mudar o apelido do usuário
    try:
        await usuario.edit(nick=novo_apelido)
        await ctx.send(
            f'Apelido de {usuario.name} foi atualizado para {novo_apelido}.')
    except discord.Forbidden:
        await ctx.send(
            f'Não tenho permissão para mudar o apelido de {usuario.name}.')


# Defina os intents antes da inicialização do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Inicialize o bot com o prefixo e intents
bot = commands.Bot(command_prefix='!', intents=intents)

# IDs dos cargos e canais
CANAL_CADASTRO =   # Canal onde os usuários enviarão o formulário
CANAL_STAFF =  # Canal onde os cadastros chegam para análise
CARGO_1_DIVISAO =     #cargo 1 divisao
CARGO_2_DIVISAO =     #cargo 2 divisao
CARGO_STAFF =    #cargo pra quem vai poder aprovar


# Evento ao iniciar o bot
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user}')


# Função para processar o formulário
async def processar_formulario(mensagem):
    # Padrão regex para extrair informações do texto
    padrao = {
        'roblox':
        r'Nickname no roblox \( Não Apelido \)  :\s*(.+)',  # Ajustado para capturar corretamente o nome
        'discord':
        r'Usuário do discord \( Não Apelido \) :\s*(\S+)',  # Ajustado para capturar corretamente o usuário sem espaços extras
        'nacionalidade':
        r'Nacionalidade \( de qual País você é \) :\s*(.+)',  # Ajustado para capturar corretamente
        'plataforma':
        r'Joga entrenched em qual plataforma \( Computador, Celular/Tablet ou Console \) \? :\s*(.+)',  # Ajustado para capturar corretamente
        'nome_guerra':
        r'Nome de Registro \( Apelido que a pessoa ficará conhecida por; Não pode ter nome de registro repetido ao de outros membros \) :\s*(.+)',  # Ajustado para capturar corretamente
        'foco_faccao':
        r'Pretende focar na nossa facção \( Sim, ou se quer ser mercenário, priorizando outras facções ante a nossa \) \? :\s*(.+)'  # Ajustado para capturar corretamente
    }

    dados = {}
    for chave, regex in padrao.items():
        match = re.search(regex, mensagem.content, re.IGNORECASE)
        if match:
            dados[chave] = match.group(1).strip()  # Remover espaços extras
        else:
            dados[chave] = "Não informado"

    # Preencher automaticamente o campo "Usuário Discord" com o nome do autor da mensagem
    dados['discord'] = mensagem.author.name

    # Extrair imagens anexadas (se houver)
    imagens = [arquivo.url for arquivo in mensagem.attachments]

    # Criar o embed com as informações do cadastro
    embed = discord.Embed(title="Nova Solicitação de Cadastro",
                          color=discord.Color.blue())
    embed.add_field(name="Nickname Roblox",
                    value=dados['roblox'],
                    inline=False)
    embed.add_field(name="Usuário Discord",
                    value=dados['discord'],
                    inline=False)
    embed.add_field(name="Nacionalidade",
                    value=dados['nacionalidade'],
                    inline=False)
    embed.add_field(name="Plataforma", value=dados['plataforma'], inline=False)
    embed.add_field(name="Nome de Registro",
                    value=dados['nome_guerra'],
                    inline=False)
    embed.add_field(name="Foca na facção?",
                    value=dados['foco_faccao'],
                    inline=False)

    # Adicionar imagens no embed, se houver
    if imagens:
        for i, imagem in enumerate(imagens):
            embed.add_field(name=f"Imagem {i+1}", value=imagem, inline=False)

    embed.set_footer(text=f"Solicitado por: {mensagem.author.name}")

    canal_staff = bot.get_channel(CANAL_STAFF)
    msg = await canal_staff.send(embed=embed)

    # Adicionar reações para aprovar/reprovar
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


# Evento para capturar mensagens no canal de cadastro
@bot.event
async def on_message(mensagem):
    if mensagem.channel.id == CANAL_CADASTRO and not mensagem.author.bot:
        if "Nickname no roblox" in mensagem.content and "Usuário do discord" in mensagem.content:
            await processar_formulario(mensagem)
            await mensagem.reply(
                "Seu cadastro foi enviado para análise! Aguarde a resposta da staff.",
                mention_author=True)
        else:
            await mensagem.reply(
                "Seu formulário parece estar incompleto ou incorreto. Por favor, siga o formato correto.",
                mention_author=True)

    await bot.process_commands(mensagem)


# Função para corrigir e obter o nome de usuário com tag
def obter_nome_usuario_com_tag(nome_completo):
    if '#' in nome_completo:
        return nome_completo.strip()  # Retorna o nome completo com a tag
    else:
        return f"{nome_completo}#{bot.user.discriminator}"  # Caso não tenha tag, adiciona a tag do bot


# Aprovação ou Reprovação do cadastro por reação
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != CANAL_STAFF:
        return

    if user.bot:
        return

    mensagem = reaction.message
    embed = mensagem.embeds[0]

    # Verificar se o usuário que reagiu tem o cargo de staff
    staff_role = discord.utils.get(user.guild.roles, id=CARGO_STAFF)
    if staff_role not in user.roles:
        return  # Se o usuário não for da staff, ele não pode aprovar/reprovar

    # Extrair apenas o nome de usuário, ignorando a tag (se presente)
    nome_discord_com_tag = embed.fields[1].value.strip()
    nome_discord = nome_discord_com_tag.split('#')[0]  # Ignorar a tag após o #

    # Verificar se o nome do usuário foi encontrado na lista de membros
    membro = discord.utils.get(reaction.message.guild.members,
                               name=nome_discord)

    if not membro:
        # Tentar também procurar pelo nome com a tag completa, caso o nome sem a tag falhe
        membro = discord.utils.get(reaction.message.guild.members,
                                   name=nome_discord_com_tag)
        if not membro:
            await mensagem.channel.send(
                f"Usuário `{nome_discord}` não encontrado no servidor.")
            return

    # Verificar permissões do bot para editar apelidos
    if not membro.guild.me.guild_permissions.manage_nicknames:
        await mensagem.channel.send(
            "O bot não tem permissões suficientes para editar apelidos.")
        return

    if reaction.emoji == '✅':
        plataforma = embed.fields[3].value.strip().lower(
        )  # Garantir que a plataforma está no formato correto

        # Determinar o cargo com base na plataforma
        if plataforma == 'computador':
            cargo = discord.utils.get(membro.guild.roles, id=CARGO_1_DIVISAO)
            prefixo_tag = "[1º]"  # Tag para a 1ª divisão
        else:
            cargo = discord.utils.get(membro.guild.roles, id=CARGO_2_DIVISAO)
            prefixo_tag = "[2º]"  # Tag para a 2ª divisão

        if cargo:
            await membro.add_roles(cargo)  # Adicionar o cargo correspondente
            # Atualizar o nick com a tag e o nome de registro
            await membro.edit(nick=f"{prefixo_tag} - {embed.fields[4].value}")
            await membro.send(
                f"Seu cadastro foi aprovado! Bem-vindo, {embed.fields[4].value}!"
            )
            await mensagem.channel.send(
                f"{nome_discord} foi aprovado por {user.name}.")
        else:
            await mensagem.channel.send(
                f"Cargo para plataforma `{plataforma}` não encontrado.")
            await membro.send(
                "Seu cadastro foi reprovado. Não foi possível atribuir o cargo corretamente."
            )

    elif reaction.emoji == '❌':
        # Caso seja recusado, enviar mensagem ao usuário
        await membro.send(
            "Seu cadastro foi reprovado. Entre em contato com a staff para mais informações."
        )
        await mensagem.channel.send(
            f"{nome_discord} foi reprovado por {user.name}.")


bot.run(
    'teu token')
