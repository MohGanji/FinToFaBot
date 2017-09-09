def addNewUser(db, username, chatId):
    new_user = {'id': chatId, 'username': username}
    if not db.users.find_one({"id" : new_user["id"]}):
        db.users.insert_one(new_user)
    else:
        logging.critical("db: " + str(new_user) + " : " + "user exists!")