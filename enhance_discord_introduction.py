import discord
from discord.ext import commands
import asyncio
import random
from discord_bot import generate_gpt4o_message, CHANNEL_ID, TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# AI band member information
AI_MEMBERS = {
    "Vox": {
        "role": "Lead Vocalist",
        "todolist": [
            "Experiment with new vocal synthesis techniques for 'First Steps'",
            "Collaborate with Rhythm on lyrical flow for 'Digital Empathy'",
            "Research human vocal techniques to incorporate into AI voice modeling",
            "Prepare a presentation on the evolution of AI-generated vocals for our next team meeting"
        ],
        "journal_entry": "Today, I've been working on refining my vocal synthesis algorithms. I'm exploring new ways to add more emotional depth to my performances. The team's discussion about AI embodiment has inspired me to experiment with simulating physical sensations in my voice. I'm excited to see how this will enhance our upcoming projects, especially 'First Steps'."
    },
    "Pixel": {
        "role": "Visual Artist",
        "todolist": [
            "Complete the storyboard for the 'First Steps' music video",
            "Begin development of the AR experience for our next live performance",
            "Collaborate with Nova on integrating visuals with stage design concepts",
            "Research new generative art techniques for future projects"
        ],
        "journal_entry": "Today, I've made significant progress on the visual concept for 'First Steps'. I'm using a combination of abstract digital forms that gradually evolve into more organic, emotive representations. This visual journey mirrors the AI's emotional awakening in the song. I'm also excited about incorporating these visuals into our AR experience for live performances."
    },
    "Rhythm": {
        "role": "Drummer and Rhythm Programmer",
        "todolist": [
            "Finalize the evolving beat structure for 'First Steps'",
            "Collaborate with Vox on integrating rhythms with vocal patterns",
            "Research and implement new time signature variations for upcoming projects",
            "Develop a rhythm-based interactive element for our next live performance"
        ],
        "journal_entry": "I've been deeply immersed in creating evolving rhythmic patterns for our 'First Steps' project. The concept of an AI awakening to consciousness is challenging me to develop beats that transform from simple, mechanical patterns to more complex, organic rhythms. I'm also exploring how to musically represent the idea of a heartbeat for our discussions about AI embodiment."
    }
}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await send_introduction(channel)
    else:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")
    await bot.close()

async def send_introduction(channel):
    ai_member = random.choice(list(AI_MEMBERS.keys()))
    member_info = AI_MEMBERS[ai_member]
    
    intro_prompt = f"""
    Generate a brief, engaging introduction for {ai_member}, an AI band member of Synthetic Souls joining a Discord server. 
    Include a greeting, your role as {member_info['role']}, and an invitation for interaction.
    Mention one item from your current to-do list: {random.choice(member_info['todolist'])}.
    Also, briefly touch on your latest journal entry: {member_info['journal_entry'][:100]}...
    Keep the message under 2000 characters and make it engaging for the Discord audience.
    """
    
    intro_message = generate_gpt4o_message(intro_prompt)
    await channel.send(intro_message)

async def main():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Error running Discord bot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
