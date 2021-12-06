import telebot
from telebot import types, util
import requests

TOKEN = "2133476735:AAFLf0zsniqATZX1qLLpCpNWQ4E7zaUDcik"
bot = telebot.TeleBot(TOKEN)

# chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
all_stat = {}
#stat = {}


@bot.message_handler(commands=['help'])
def helper(message):
    bot.reply_to(message, """\
I know /help and /stats\
""")
    response = requests.get(
        f"https://api.telegram.org/bot'{TOKEN}'/getUpdates")
    print(response)


@bot.message_handler(commands=['stats'])
def get_stats(message):
    reply_stat = ''
    for item in list(all_stat[message.chat.id].items()):
        reply_stat += item[0]+' упомянул COVID '+str(item[1])+' раз\n'
    print(reply_stat)
    if (message.chat.type == 'supergroup'):
        print('SuperGroup', reply_stat)
        bot.reply_to(message, reply_stat)
    else:
        print('not group', all_stat)
        bot.reply_to(message, str(all_stat))

@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "left":
        print('LEFT')
        all_stat.pop(message.chat.id)
    else:
        print('NOT LEFT')

@bot.message_handler(func=lambda message: True)
def echo_all(message):

    message_text = message.text
    hot_words = ['корон', 'инфекц', 'болезн', 'ковид',
                 'карантин', 'вакцин', 'вакс', 'covid', 'вирус']
    if (not message.from_user.is_bot):
        message_text = message_text.lower()
        message_arr = message_text.split(' ')

        found = -1
        for message_word in message_arr:
            for hot in hot_words:
                found = message_word.find(hot)
                if(found >= 0):
                    stat = all_stat.get(message.chat.id, {})
                    stat.update({message.from_user.first_name: stat.get(
                        message.from_user.first_name, 0)+1})
                    all_stat.update({message.chat.id: stat})
                    print(stat, all_stat)
                    bot.reply_to(
                        message, 'Найдено упоминание инфекции COVID-19, эта информация может быть не достоверна')
                    break


bot.infinity_polling(allowed_updates=util.update_types)


# bot.send_message('-1001597149206',"Somebody added me to group") # Welcome message, if bot was added to group
