import logging
from subprocess import (PIPE, Popen)

def add_new_user(db, username, chatId):
    """ add a new user to database for broadcasting."""
    new_user = {
        'id': chatId, 'username': username, 'state': 0,
        'report': {'finglish_msg': "", 'farsi_msg': ""}
    }

    if not db.users.find_one({"id" : new_user["id"]}):
        logging.critical("db: " + str(new_user) + " added.")
        db.users.insert_one(new_user)
    else:
        logging.critical("db: " + str(new_user) + " : " + "user exists!")

def transliterate_to_farsi(message):
    """ transliterate finglish messages to farsi, returns farsi text """
    text = message.text
    user_id = message.from_user.id
    logging.critical(str(user_id) + " : " + text)
    if text:
        if text[0] == '/':
            text = text[1:]

        text = text.replace("@TransliterateBot", "")
        text = text.split()
        # defallahi(text)
        # irregularHandle(text)
        shcommand = ['php', './behnevis.php']
        shcommand.extend(text)
        pipe = Popen(shcommand, stdout=PIPE, stderr=PIPE)
        text, err = pipe.communicate()
        if err:
            logging.critical("PHP ERR: " + err)
        logging.critical("res : " + str(user_id) + " : " + text)
        return text

def add_report_request(db, message):
    """Add a report request to the database"""
    uid = message.from_user.id
    farsi_msg = db.users.find_one({'id': uid})['report']['farsi_msg']
    finglish_msg = db.users.find_one({'id': uid})['report']['finglish_msg']
    corrected_msg = message.text
    new_report_instance = {'finglish': finglish_msg,
                           'farsi': farsi_msg,
                           'corrected': corrected_msg}
    db.reports.insert_one(new_report_instance)
    logging.critical("A new report record added: "+ str(new_report_instance))
    db.users.update({'id': message.from_user.id}, {'$set': {'state': 0}})
