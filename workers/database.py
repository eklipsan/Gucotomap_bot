from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config_data.config import load_config
from pymongo.collection import Collection
from workers.logset import logger


def create_connection() -> Collection:
    """
    This function establishes a connection to the MongoDB database and returns the 'users' collection.

    Returns:
        A Collection object representing the 'users' collection in the MongoDB database.
    """

    # Load the database configuration from the config file
    mongo_config = load_config()
    mongo_config = mongo_config.DatabaseConfig

    # Extract the MongoDB username, password, and cluster from the config
    USERNAME = mongo_config.mongodb_name
    PASSWORD = mongo_config.mongodb_password
    CLUSTER = mongo_config.mongodb_cluster

    # Construct the MongoDB connection URI
    uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}.udm4ii6.mongodb.net/?retryWrites=true&w=majority"

    # Create a new MongoClient and connect to the MongoDB server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to the MongoDB server to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinging MongoDB successfully")
    except Exception:
        logger.exception("Fail to ping MongoDB")

    # Get the 'user_db' database and the 'users' collection
    user_db = client.user_db
    user_collection = user_db.users

    # Return the 'users' collection
    return user_collection


def init_user(user_collection: Collection, user_id: int, ATTEMPTS: int = 5) -> None:
    """
    Initializes a new user in the MongoDB database.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
        ATTEMPTS: The maximum number of attempts allowed for each game.
    """

    # Check if the user already exists in the database
    if user_collection.find_one(filter={"user_id": user_id}, ) is None:
        # Create a new user document
        new_user = {
            'user_id': user_id,
            'game': False,
            'attempts': ATTEMPTS,
            'score': 0,
            'max_score': 0,
            'played_games': 0,
            'town_name': '',
            'town_values': dict(),
            'map_url': '',
            'countries': list()
        }

        # Insert the new user document into the database
        user_collection.insert_one(new_user)
        logger.info(f"Creating a new user id {user_id}")
    updates = {'$set': {
        'game': False,
        'attempts': ATTEMPTS,
        'score': 0,
        'town_name': '',
        'town_values': dict(),
        'map_url': '',
        'countries': list()

    }}
    user_collection.update_one(filter={"user_id": user_id}, update=updates)
    logger.debug(f"Setting default game state for user id {user_id}")


def setup_user_question(user_collection: Collection, user_id: int, town_name: str, town_values: dict, map_url: str, countries: tuple) -> None:
    """
    Initializes a user question. It is adjacent function with setup_quiz.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
        town_name: The name of the place of shown country on the map.
        town_values: The dictionary with other information about the town.
        map_url: API-url from Static Yandex Map, that returns a map photo.
        countries: Set of unique countries, where is one right answer.
    """
    updates = {'$set': {
        'town_name': town_name,
        'town_values': town_values,
        'map_url': map_url,
        'countries': countries
    }}
    user_collection.update_one(filter={"user_id": user_id}, update=updates)
    logger.debug(f"Initializing a user question for user id {user_id}")


def start_user_game(user_collection: Collection, user_id: int) -> None:
    """
    Starts a new game for the specified user.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
    """

    # Set the 'game' field to True and reset the 'score' field to 0 for the specified user
    updates = {'$set': {'game': True, 'score': 0}}
    user_collection.update_one({"user_id": user_id}, update=updates)
    logger.debug(f"Starting a new game for user id {user_id}")


def check_user_game_status(user_collection: Collection, user_id: int) -> bool:
    """
    Checks if the specified user is currently in a game.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.

    Returns:
        True if the user is currently in a game, False otherwise.
    """

    # Retrieve the user document from the database
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Check the value of the 'game' field in the user document
    logger.debug(f"Checking if user id {user_id} is in a game")
    return user_dict['game']


def increase_user_score(user_collection: Collection, user_id: int) -> None:
    """
    Increments the score of the specified user by 1.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
    """

    # Increment the 'score' field of the specified user by 1
    updates = {'$inc': {'score': 1}}
    user_collection.update_one({"user_id": user_id}, update=updates)
    logger.debug(f"Incrementing the game score of user id {user_id}")


def check_positive_attempts(user_collection: Collection, user_id: int) -> bool:
    """
    Checks if the specified user has any attempts left.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.

    Returns:
        True if the user has at least 1 attempt left, False otherwise.
    """

    # Retrieve the user document from the database
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Check the value of the 'attempts' field in the user document
    logger.debug(f"Checking if user id {user_id} has any attempts left")
    return user_dict['attempts'] > 1


def decrease_user_attempts(user_collection: Collection, user_id: int) -> None:
    """
    Decrements the number of attempts left for the specified user by 1.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
    """

    # Decrement the 'attempts' field of the specified user by 1
    updates = {'$inc': {'attempts': -1}}
    user_collection.update_one({"user_id": user_id}, update=updates)
    logger.debug(f"Decrementing the number of attempts for user id {user_id}")


def finish_user_game(user_collection: Collection, user_id: int, ATTEMPTS: int) -> None:
    """
    Ends the current game for the specified user and updates their statistics.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
        ATTEMPTS: The maximum number of attempts allowed for each game.
    """

    # Retrieve the user document from the database
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Update the user's statistics
    updates = {'$inc': {'played_games': 1}, '$set': {
        'game': False, 'attempts': ATTEMPTS, 'score': 0}}
    if user_dict['score'] > user_dict['max_score']:
        updates['$set']['max_score'] = user_dict['score']
    # Apply the updates to the user document
    user_collection.update_one({"user_id": user_id}, update=updates)
    logger.debug(f"Ending the game for user id {user_id} and updating their stats")


def get_user_info(user_collection: Collection, user_id: int) -> dict:
    """
    Retrieves the current information for the specified user.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.

    Returns:
        A user info dictionary with keys:
        user_id - int,
        game - bool,
        attempts - int,
        score - int,
        max_score - int,
        played_games - int,
        town_name - str,
        town_values - dict,
        map_url - str,
        countries - list
    """

    # Retrieve the user document from the database
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Return the user's current score and number of attempts
    logger.debug(f"Retrieving MongoDB values for user id {user_id}")
    return user_dict
