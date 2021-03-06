import datetime
import user
import documents
import queue
import collections
import heapq
import database as db

qu = []


def order_book(usr, document):
    if not usr.has_book(document.get_title()):
        if not document.is_reference():
            init_date = datetime.date.toordinal(
                datetime.date.today())
            exp_date = datetime.datetime.fromordinal(
                init_date + distr(usr, document))
            if len(document.get_queue()) == 0:
                return give_on_hands(usr, document, exp_date)
            elif len(document.get_queue()) > 0:
                return add_to_waiting_list(usr, document)
        else:
            return reference
    else:
        text = renew(usr, document)
        return text


def order_av(usr, document):
    if not usr.has_book(document.get_title()):
        init_date = datetime.date.toordinal(
            datetime.date.today())
        exp_date = datetime.datetime.fromordinal(
            init_date + distr(usr, document))
        if len(document.get_queue()) == 0:
            return give_on_hands(usr, document, exp_date)
        elif len(document.get_queue()) > 0:
            return add_to_waiting_list(usr, document)
    else:
        return renew(usr, document)


def order_article(usr, document):
    if not usr.has_book(document.get_title()):
        init_date = datetime.date.toordinal(
            datetime.date.today())
        exp_date = datetime.datetime.fromordinal(
            init_date + distr(usr, document))
        if len(document.get_queue()) == 0:
            return give_on_hands(usr, document, exp_date)
        elif len(document.get_queue()) > 0:
            return add_to_waiting_list(usr, document)
    else:
        return renew(usr, document)


def booking(usr, document, code):
    if code == "Reserve":
        if document.summary()["type"] == "Book":
            return order_book(usr, document)

        elif document.summary()["type"] == "AV":
            return order_av(usr, document)

        elif document.summary()["type"] == "Article":
            return order_article(usr, document)
    elif code == "To waiting list":
        return add_to_waiting_list(usr, document)
    elif code == "Renew":
        return renew(usr, document)


def add_to_queue(usr, document):
    q = document.get_queue()
    print("This is q " + str(q))
    heapq.heappush(document.get_queue(), (usr.get_prior(), usr.get_id()))
    db.update(title=document.get_title(), queue=document.get_queue())
    return document.get_queue()


def pop_from_queue(qu):
    heapq.heappop(qu)
    return qu


def add_to_waiting_list(user, document):
    queue = add_to_queue(user, document)
    number = [queue[i][1] for i in range(0, len(queue))]
    return waiting_list + str(number.index(user.get_id()) + 1)


def give_on_hands(usr, document, exp_date):
    copy = document.pop_copy()
    print("asdasd")
    usr.add_document(document.get_title(), str(exp_date.date()))
    return success + " " + str(exp_date)


def renew(usr, document):
    copy = document.get_title()
    if usr.is_renew_possible(copy) or usr.get_type() == "VP":
        ini_date = datetime.date.toordinal(datetime.date.today())
        exp_date = datetime.date.fromordinal(ini_date + 7)
        usr.add_document(copy, str(exp_date))
        print("Good. Doc was renewed")
        return renew_nail + str(exp_date)
    else:
        print("ERR. Doc can not be renewed")
        return renew_fail


def distr(usr, document):
    if document.get_type() == "Book":
        return distribute(usr, document.is_bestseller())
    else:
        return distribute(usr, False)


def distribute(usr, bestseller):
    if usr.get_type() in faculty:
        return 28
    elif usr.get_type() == vp:
        return 7
    elif usr.get_type() == student:
        if bestseller:
            return 14
        else:
            return 21


now = datetime.datetime.now()
today_format1 = now.strftime("%H:%d:%m:%Y")
second_id = now.second
userqueue = []

faculty = ["Professor", "TA", "Instructor"]
vp = "VP"
student = "Student"


success = "Congratulations! You have been successfully ordered a book until: "
fail = "Unfortunately this doc is not yet available..."
reference = "Unfortunately, You are trying to book a reference material which is unavailable. "
max_renew_alert = "You have reached maximum amount of renews. :( "
no_copies = "No copies of current book were found."
renew_fail = "You can not renew this book again"
renew_nail = "You renewed this book until "
waiting_list = "You have been added to the waiting list of this book. Your number is "

"""
student = user.Student("stud", "Student", "name.surname@innopolis.ru", "1234567", "@student", "Innopolis City")
prof = user.Faculty("prof", "Professor", "name.surname1@innopolis.ru", "1234568", "@professor", "Innopolis City")
vp = user.VP("pidor", "VP", "dqdewfe.surname@innopolis.ru", "1231241", "@vp", "Inno")
student_pidor = user.Student("Ramil", "Ramil", "name.surname@innopolis.ru", "1234567", "@student", "Innopolis City")
student_jopaenota = user.Student("Nikita", "Nikita", "name.surname@innopolis.ru", "1234567", "@jopaenota",
                                 "Innopolis City")
# instructor = user.Instructors("129313213", "Instructor", "name.surname11@innopolis.ru", "212314", "@pidor", "Inno")
ta = user.TA("986543", "TA", "name.surname11@innopolis.ru", "212314", "@pidor", "Inno")

book1 = documents.Book("Book1", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "false", "false")
book2 = documents.Book("Book5", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "true", "false")
book3 = documents.Book("Reference", "Author Uknown", "Innopolis", "2018", "1st", "Reference", "Url", "false", "true")

article1 = documents.Article("Article", "Blogger", "InnoTimes", "2018", "Inno", "URL")
av_file1 = documents.AV_Materials("Title", "JimmyHendrix", "200$", "URL")

add_to_queue(student)
add_to_queue(prof)
add_to_queue(vp)
add_to_queue(student_jopaenota)
add_to_queue(student_pidor)
add_to_queue(ta)
# print(qu)
pop_from_queue(qu)

# print(qu)

# print()
# print(ta.summary())
# booking(student, book1)

# print(second_id)
"""
