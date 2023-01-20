"""
        This is the file that contains utility methods for dealing with interactions between the Discord bot and MongoDB
        @author Kory Stennett
"""

import random

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
            "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabetUpper = ["A","B","C","D","E","F","G","H","I","J","K",
                 "L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


async def updateAttackID(bot,_id):
    db = bot.mongoConnect["DiscordBot"]
    collection = db["Economy"]
    data = await collection.find_one({"_id": _id})
    attackID = scrambleAttackID(_id)
    data["attackID"] = attackID
    await collection.replace_one({"_id": _id}, data)

async def scrambleAttackID(_id):
    """
    Creates a random ID using the Discord user ID combined with random letters from the alphabet and then scrambled.
    :param _id: Discord user ID
    :return: a randomized ID to attack players with
    """
    idStr = str(_id)
    encryptionLength = 6
    for x in range(0,encryptionLength):
        idStr += random.choice(alphabet)
    for x in range(0, encryptionLength):
        idStr += random.choice(alphabet)
    l = list(idStr)
    random.shuffle(l)
    result = ''.join(l)

    return result

async def findByAttackID(bot, attackID : str):
    """
    Finds a player to attack by targeting their attack ID
    :param bot: the Discord bot from main.py
    :param attackID: string
    :return: player data document from MongoDB
    """
    db = bot.mongoConnect["DiscordBot"]
    collection = db["Economy"]
    data = await collection.find_one({"attackID": attackID})

    return data


async def fetchData(bot, _id):
    """
    The main way to get information about a user, and gather the entire user profile collection
        If a user doesn't get found by ID, they're created automatically.
    :param bot: discord bot
    :param _id: user ID to search for
    :return: userData, collection
    """
    db = bot.mongoConnect["DiscordBot"]
    attackID = await scrambleAttackID(_id)
    collection = db["Economy"]
    # BIG NOTE: This should definitely not exist on a massive scale, it would blow up the database. It's just here
    # while I figure out which variables I want to track on my profiles. It is a hacky way to put new variables on every
    # user profile in the database
    """
    More info on this method:
        It uses a pipeline to do something to a set of documents in a collection.
        In my case, the first parameter is query and it is blank because we're searching for everything 
        The second parameter is what we're actually doing with the documents, which is set a new variable to something
        The final parameter is necessary for update_many and doesn't really influence our situation 
    """

    #await collection.update_many(
        #{},
        #{"$set": {"position": {"horizontal": 0, "vertical": 0}}},

        #upsert=False

    #)

    if await collection.find_one({"_id": _id}) == None:
        newData = {
            "_id": _id,
            "coins": 0,
            "bank":0,
            "cups": 0,
            "boxes":1,
            "cardboard":0,
            "picUrl":"",
            "attackID": attackID
        }
        await collection.insert_one(newData)
    return await collection.find_one({"_id": _id}), collection


async def removeAccount(bot, _id):
    """
    A quick and dirty way to remove account and allow users to reset their profiles.
        It deletes the document if it exists, but the user can only delete their own account.
    :param bot: discord bot
    :param _id: user ID
    :return: Nothing
    """
    db = bot.mongoConnect["DiscordBot"]
    collection = db["Economy"]
    query = {"_id": _id}
    collection.delete_one(query)


async def removeMeme(bot, url):
    """
    Removes memes from the reactions collection on MongoDB
    :param bot: discord bot
    :param url: image URL
    :return: Nothing
    """
    db = bot.mongoConnect["DiscordBot"]
    #   automatically creates genre if not present
    collection = db["reactions"]
    query = {"_id": url}
    collection.delete_one(query)

async def addMeme(bot, genre, url):
    """
    Add meme to the database (it is checked for authenticity beforehand)
        It follows the data scheme of { "_id": url, "genre": genre }
        That means the same image can only be uploaded once because it would recognize that URL
        and we are only accepting images and gifs from links/URLs.
    :param bot: discord bot
    :param genre: str
    :param url: str
    :return: Nothing
    """
    db = bot.mongoConnect["DiscordBot"]
    #   automatically creates genre if not present
    collection = db["reactions"]
    data = {
        "_id": url,
        "genre": genre
    }
    await collection.insert_one(data)


async def fetchMeme(bot, genre):
    """
    Grab a random meme from the database based on genre (like confused, happy, sad)
    :param bot: discord bot
    :param genre: str
    :return: meme = {
        "_id": url,
        "genre": genre
    }
    """
    db = bot.mongoConnect["DiscordBot"]
    #   automatically creates genre if not present
    collection = db["reactions"]
    meme = "No meme found"
    async for doc in collection.aggregate([
        {"$match": {"genre": genre}},
         {"$sample": {"size": 1}}
    ]):
        meme = doc
    return meme
