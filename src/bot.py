from utils import *
from time import sleep
import sys
import telebot

from sources import cryptopanic

config = parse_config(DEFAULT_CONFIG_PATH)
bot = telebot.TeleBot(config["bot token"], parse_mode="html")


bot_dat_separator = "::"
# if service name = 'enabled' then this won't work
enabled = [option for option in config if config[option] == "enabled"]

# Telegram
channel_id = None
channel_title = None

#Cryptopanic
latest_cryptopanic_date = None

if not file_exists(BOT_DATA_PATH):
    create_file(BOT_DATA_PATH)
else:
    bot_dat = [i.strip() for i in read_file(BOT_DATA_PATH).split(bot_dat_separator)]
    if len(bot_dat) >= 2:
        channel_id = bot_dat[0]
        channel_title = bot_dat[1]
    if len(bot_dat) >= 3:
        latest_cryptopanic_date = bot_dat[2]



def get_bot_info(bot_object):
    info = ""
    for key, item in vars(bot_object.get_me()).items():
        info += f"{key} = {item}\n"
    return info


print("\n\t Bot Information: ")
print(get_bot_info(bot))

if channel_id:
    print(f"\tRunning in {channel_title} ({channel_id})")
else:
    print(f"\
        \tPlease configure the bot by adding it to a channel\n\
        \tand running '/start' in the channel, to which the bot will\n\
        \trespond. Restart the bot after.\n\n")


@bot.channel_post_handler(commands=["start"])
def send_confirmation(message):
    # telegram message syntax https://core.telegram.org/bots/api#formatting-options
    bot.reply_to(message, "<b>Bot initialised, channel saved.</b>")
    channel_id = message.chat.id
    channel_title = message.chat.title
    write_file(BOT_DATA_PATH, str(channel_id) + bot_dat_separator + channel_title)
    # update to not overwrite other configurations
    print(f"\tRunning in {channel_title} ({channel_id})\n\tChannel saved.")
    print("\n\n\t RESTART THE SCRIPT")


# Avoiding the usage of global variables
if channel_id is None:
    bot.infinity_polling()
    sys.exit()

cryptopanic = cryptopanic.Cryptopanic()

# Full messages for telegram channel
# https://github.com/eternnoir/pyTelegramBotAPI/issues/873
post_queue = []

while True:
    try:
        if "cryptopanic" in enabled:
            temp_crp = cryptopanic.get_new_rss(latest_cryptopanic_date)

            if len(temp_crp) > 0:
                crp = [f"Source: cryptopanic\nDate: {item[0]}\nPost: <a href='{item[2]}\'>{item[1]}</a>" for item in temp_crp]
                latest_cryptopanic_date = temp_crp[-1][0]
                temp_bot_dat = read_file(BOT_DATA_PATH).split(bot_dat_separator)
                if len(temp_bot_dat) > 2:
                    temp_bot_dat[2] = latest_cryptopanic_date
                else:
                    temp_bot_dat.append(latest_cryptopanic_date)
                temp_bot_dat = bot_dat_separator.join(temp_bot_dat)
                write_file(BOT_DATA_PATH, temp_bot_dat)
                post_queue += crp

        for post in post_queue:
            bot.send_message(channel_id, post, disable_web_page_preview=True)
            print(f"Posted: {post}")
            sleep(4)  # don't overflow rate limit

        post_queue = []
        
        sleep(180) # crashes after few hours if below <15

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt, quitting")
        sys.exit()
