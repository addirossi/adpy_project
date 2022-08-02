import os

from dotenv import load_dotenv

from bot import VkBot


load_dotenv()


user_token = os.getenv('ACCESS_TOKEN')
group_token = os.getenv('GROUP_TOKEN')


bot = VkBot(user_token, group_token)
bot.start()