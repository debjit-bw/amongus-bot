# Work with Python 3.6
import logging, re
import random
from gtts import gTTS
import asyncio

logging.basicConfig(level=logging.INFO)


import discord

country_list = {'A': ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Austrian Empire', 'Azerbaijan'],
				'B': ['Baden*', 'Bahamas, The', 'Bahrain', 'Bangladesh', 'Barbados', 'Bavaria*', 'Belarus', 'Belgium', 'Belize', 'Benin (Dahomey)', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Brunswick and LÃ¼neburg', 'Bulgaria', 'Burkina Faso (Upper Volta)', 'Burma', 'Burundi'],
				'C': ['Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands, The', 'Central African Republic', 'Central American Federation*', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo Free State, The', 'Costa Rica', 'Cote dâ€™Ivoire (Ivory Coast)', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Czechoslovakia'],
				'D': ['Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Duchy of Parma, The*'],
				'E': ['East Germany (German Democratic Republic)', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia'],
				'F': ['Fiji', 'Finland', 'France'],
				'G': ['Gabon', 'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Grand Duchy of Tuscany, The*', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana'],
				'H': ['Haiti', 'Hanover*', 'Hanseatic Republics*', 'Hawaii*', 'Hesse*', 'Holy See', 'Honduras', 'Hungary'],
				'I': ['Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy'],
				'J': ['Jamaica', 'Japan', 'Jordan'],
				'K': ['Kazakhstan', 'Kenya', 'Kingdom of Serbia/Yugoslavia*', 'Kiribati', 'Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan'],
				'L': ['Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Lew Chew (Loochoo)*', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg'],
				'M': ['Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mecklenburg-Schwerin*', 'Mecklenburg-Strelitz*', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique'],
				'N': ['Namibia', 'Nassau*', 'Nauru', 'Nepal', 'Netherlands, The', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North German Confederation*', 'North German Union*', 'North Macedonia', 'Norway'],
				'O': ['Oldenburg*', 'Oman', 'Orange Free State*'],
				'P': ['Pakistan', 'Palau', 'Panama', 'Papal States*', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Piedmont-Sardinia*', 'Poland', 'Portugal'],
				'Q': ['Qatar'],
				'R': ['Republic of Genoa*', 'Republic of Korea (South Korea)', 'Republic of the Congo', 'Romania', 'Russia', 'Rwanda'],
				'S': ['Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Schaumburg-Lippe*', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands, The', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria'],
				'T': ['Tajikistan', 'Tanzania', 'Texas*', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Two Sicilies*'],
				'U': ['Uganda', 'Ukraine', 'Union of Soviet Socialist Republics*', 'United Arab Emirates, The', 'United Kingdom, The', 'Uruguay', 'Uzbekistan'],
				'V': ['Vanuatu', 'Venezuela', 'Vietnam'],
				'W': ['Württemberg*'],
				'X': ['X'],
				'Y': ['Yemen'],
				'Z': ['Zambia', 'Zimbabwe']}


def textSave(text):
	build = ".  \n".join(text)
	text = build + ". I am repeating. " + build
	tts = gTTS(text, lang='en-in')
	tts.save("res.mp3")

def mes(text):
	vc = []
	if len(re.findall("^([A-Z|a-z]{5}[Q|q])", text))>0:
		res = 'Translating to Arion...'
		for c in re.findall("^([A-Z|a-z]{5}[Q|q])", text)[0].upper():
			country = random.choice(country_list[c])
			res += f"\n{c}: {country}"
			vc.append(country)
		return res,vc
	return None


TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	resp = mes(message.content)
	if resp != None:
		response,vcText = resp
		await message.channel.send(response)
		textSave(vcText)
		connected = message.author.voice
		if connected:
			await connected.channel.connect()
		vc = client.voice_clients[0]
		vc.play(discord.FFmpegPCMAudio('res.mp3'),
				after=lambda e: print(f"Finished playing: {e}"))
		while vc.is_playing():
			await asyncio.sleep(0.1)
		await vc.disconnect()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
