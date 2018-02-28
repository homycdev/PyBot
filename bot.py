import types

import config
from telebot import *
import telegraph
import datetime as date
import database as db
import utilities as u
import verification as veri
import booking as b

bot = TeleBot(config.token2)
ph = telegraph.Telegraph()



"""
    Usage of Telegraph api. Integration of telegraph api for "about" features. SCRATCH FOR FUTURE FEATURES
"""
ph.create_account(short_name='InnoLib')
response = ph.create_page('Bruce Eckels Thinking in Java',
                          html_content="<p> Thinking in Java should be read cover to cover by every Java programmer, "
                                       "then kept close at hand for frequent reference. The exercises are challenging,"
                                       " and the chapter on Collections is superb!"
                                       " Not only did this book help me to pass the Sun Certified Java Programmer exam;"
                                       " it’s also the first book I turn to whenever I have a Java question. </p>")


@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id, u.greeting)


""" #######                Authentication functions                 ####### """

userEmail = ""
userName = ""
userSurname = ""
userNumber = ""


@bot.message_handler(commands=["setup"])
def authentication(email):
    msg = bot.send_message(email.chat.id, u.step0)
    bot.register_next_step_handler(msg, auth)


def auth(msg):
    if msg.text[-13:] != u.domain:
        bot.send_message(msg.chat.id, u.err_mail)

    else:
        pin = veri.pin_generator()
        veri.pin_sender(msg.text, pin)
        u.tempData['userId'] = pin
        userEmail = msg.text
        print(userEmail)
        m = bot.send_message(msg.chat.id, u.pin_enter)
        bot.register_next_step_handler(m, auth_1)


def auth_1(pin):
    if verification(pin):
        m = bot.send_message(pin.chat.id, u.step1)
        print(userEmail)
        bot.register_next_step_handler(m, auth_2)


def auth_2(msg):
    userName = msg.text
    reply = bot.send_message(msg.chat.id, u.step2)
    bot.register_next_step_handler(reply, auth3)


def auth3(message):
    userSurname = message.text
    print(userSurname)
    reply = bot.send_message(message.chat.id, u.step3)
    bot.register_next_step_handler(reply, auth4)


def auth4(message):
    userNumber = message.text
    print(userNumber)
    db.insert_user(message.chat.id, db.dict_for_user(userEmail, userName, userSurname, userNumber))
    bot.send_message(message.chat.id, u.step4)


def verification(pin):
    if pin.text == u.tempData['userId']:
        bot.send_message(pin.chat.id, u.verification_succeed)
        return True
    else:
        m = bot.send_message(pin.chat.id, u.verification_failed)
        bot.register_next_step_handler(m, verification)
        return False


@bot.message_handler(regexp='help')
def help_func(message):
    bot.reply_to(message, "Help func is currently unavailable")


"""     #######                 GUI elements         #######                """


@bot.message_handler(commands=["options"])
def keyboard(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=u.reply)


@bot.message_handler(regexp='Back')
def back(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=u.reply)


@bot.message_handler(regexp='Docs')
def genres(message):
    reply = types.ReplyKeyboardMarkup(True, False, True, 1)
    book_btn = types.KeyboardButton(text="Books")
    magaz_btn = types.KeyboardButton(text="Magazines",)
    avf_btn = types.KeyboardButton(text="AVFiles")
    back_btn = types.KeyboardButton(text="Back")
    reply.add(book_btn, magaz_btn, avf_btn, back_btn)
    bot.send_message(message.chat.id, "Choose category", reply_markup=reply)


"""     #######                  Telegraph API              #######         """

'http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th-editon-01-29'
@bot.message_handler(regexp="Books")
def telegraph_func(message):
    bot.send_message(message.chat.id, u.list_of_books[0].get_title(),
                     reply_markup=u.markup)


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def to_right(call):
    u.number=(u.number+1)%u.max-1
    # if u.number+1<u.max:
    #     u.number+=1
    # else:
    #     u.number=0
    bot.send_message(call.message.chat.id, db.list_of_all_books()[u.number], reply_markup=u.markup)


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def to_right(call):
    u.number=(u.number-1)%u.max-1
    # if u.number==0:
    #     u.number=u.max-1
    # else:
    #     u.number-=1
    bot.send_message(call.message.chat.id, db.list_of_all_books()[u.number], reply_markup=u.markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Book')
def booking(call):
    bot.send_message(call.message.chat.id, b.book_doc(b.user1, u.list_of_books[0]))

# @bot.callback_query_handler(func=lambda call: call.data == 'next')
# def next(call):
#     bot.edit_message_text()


# @bot.message_handler(regexp='jopaenota')
# def printAllUsersInBot(message):
#     db.print_all_users()


@bot.message_handler(regexp='author')
def author(message):
    bot.send_message(message.chat.id, "Enter author's name")
    @bot.message_handler(content_types=["text"])
    def get_author(message):
        book_exist = False
        for i in range(len(u.list_of_books)):
            if u.list_of_books[i].get_author() == message.text:
                book_exist = True
                bot.send_message(message.chat.id, "Book {} of author {} exist".format(u.list_of_books[i].get_title(),
                                                                                      u.list_of_books[i].get_author()))
        if not book_exist:
            bot.send_message(message.chat.id, "There is no book with this author")









if __name__ == '__main__':
    bot.polling(none_stop=True)