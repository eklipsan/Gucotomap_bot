from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config_data.config import load_config
from pymongo.collection import Collection
from workers.logset import logger
from typing import Literal


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
            'countries': list(),
            'map_lang': 'en_US',
            'map_scale': 1,
            'map_size': 11
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


def setup_user_question(
        user_collection: Collection,
        user_id: int,
        town_name: str,
        town_values: dict,
        map_url: str,
        map_invalid_response: bool,
        countries: tuple
        ) -> None:
    """
    Initializes a user question. It is adjacent function with setup_quiz.

    Args:
        user_collection: A Collection object representing the 'users' collection in the MongoDB database.
        user_id: The unique identifier of the user.
        town_name: The name of the place of shown country on the map.
        town_values: The dictionary with other information about the town.
        map_url: API-url from Static Yandex Map, that returns a map photo.
        map_invalid_response: Boolean value if loading the map is not successful
        countries: Set of unique countries, where is one right answer.
    """
    updates = {'$set': {
        'town_name': town_name,
        'town_values': town_values,
        'map_url': map_url,
        'map_invalid_response': map_invalid_response,
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


def finish_user_game(user_collection: Collection, user_id: int, ATTEMPTS: int, map_error: bool = False) -> None:
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
    updates = {'$set': {
        'game': False, 'attempts': ATTEMPTS, 'score': 0}}
    if map_error is False:
        updates['$inc'] = {'played_games': 1}
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
        countries - list,
        map_lang - str (default is 'en_US'),
        map_scale - int (default is 1),
        map_size - int (default is 11)
    """

    # Retrieve the user document from the database
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Return the user's current score and number of attempts
    logger.debug(f"Retrieving MongoDB values for user id {user_id}")
    return user_dict


def set_user_parameter_state(
        user_collection: Collection,
        user_id: int,
        map_option: Literal['', 'lang', 'scale', 'size']
        ) -> None:
    """
    Update the parameter state of a user in the user_collection.

    Parameters:
    - user_collection (Collection): The collection where user information is stored.
    - user_id (int): The unique identifier of the user.
    - map_option (Literal['', 'lang', 'scale', 'size']): The option to update the user's parameter state.

    If the map_option is valid (empty string, 'lang', 'scale', or 'size'), the function updates the user's parameter state
    in the user_collection and logs the update. If the map_option is invalid, an error is logged.

    """
    # Check if map_option is valid
    if map_option in ['', 'lang', 'scale', 'size']:
        # Prepare update
        updates = {'$set': {
            'parameter_state': map_option
        }}
        # Update user's parameter state
        user_collection.update_one(filter={"user_id": user_id}, update=updates)
        # Log the update
        logger.debug(f"User id {user_id} updates his parameter state to option {map_option}")
    else:
        # Log error for invalid map_option
        logger.error(f"User id {user_id} tries to update his parameter state to wrong option {map_option}")


def set_user_map_language(
        user_collection: Collection,
        user_id: int,
        map_language: str
        ) -> bool:
    """
    Sets the map language for a specific user in the user_collection.

    Parameters:
    - user_collection (Collection): The collection where user documents are stored.
    - user_id (int): The unique identifier of the user.
    - map_language (str): The new map language to set for the user.

    If the user's parameter state is 'lang', the function updates the user's map language to the specified value.
    If the user's parameter state is not 'lang', an error is logged, and the function returns False.
    The function logs the successful setting of the map language option.
    """
    # Find the user document in the collection
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Get the existing map language and parameter state from the user document
    ex_map_lang = user_dict['map_lang']
    state = user_dict['parameter_state']

    # Check if the parameter state is 'lang'
    if state == 'lang':
        # Prepare the updates to be applied to the user document
        updates = {'$set': {
            'parameter_state': '',
            'map_lang': map_language
        }}

        # Apply the updates to the user document
        user_collection.update_one({"user_id": user_id}, update=updates)
    else:
        # Log an error if user tries to change map language with an invalid state
        logger.error(f"User id {user_id} tries to change map language with state {state}")
        return False

    # Log the successful setting of map language option
    logger.debug(f"Setting map language option for user id {user_id} from {ex_map_lang} to {map_language}")
    return True


def set_user_map_scale(
        user_collection: Collection,
        user_id: int,
        map_scale: float
        ) -> bool:
    """
    Sets the map scale for a specific user in the user_collection.

    Parameters:
    - user_collection (Collection): The collection where user documents are stored.
    - user_id (int): The unique identifier of the user.
    - map_scale (float): The new map scale to set for the user.

    If the user's parameter state is 'scale', the function updates the user's map scale to the specified value.
    If the user's parameter state is not 'scale', an error is logged, and the function returns False.
    The function logs the successful setting of the map scale option.
    """
    # Find the user document in the collection
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Get the existing map scale and parameter state from the user document
    ex_map_scale = user_dict['map_scale']
    state = user_dict['parameter_state']

    # Check if the parameter state is 'scale'
    if state == 'scale':
        # Prepare the updates to be applied to the user document
        updates = {'$set': {
            'parameter_state': '',
            'map_scale': map_scale
        }}

        # Apply the updates to the user document
        user_collection.update_one({"user_id": user_id}, update=updates)
    else:
        # Log an error if user tries to change map scale with an invalid state
        logger.error(f"User id {user_id} tries to change map scale with state {state}")
        return False

    # Log the successful setting of map scale option
    logger.debug(f"Setting map scale option for user id {user_id} from {ex_map_scale} to {map_scale}")
    return True


def set_user_map_size(
        user_collection: Collection,
        user_id: int,
        map_size: int
        ) -> bool:
    """
    Sets the map size for a specific user in the user_collection.

    Parameters:
    - user_collection (Collection): The collection where user documents are stored.
    - user_id (int): The unique identifier of the user.
    - map_size (int): The new map size to set for the user.

    If the user's parameter state is 'size', the function updates the user's map size to the specified value.
    If the user's parameter state is not 'size', an error is logged, and the function returns False.
    The function logs the successful setting of the map size option.
    """
    # Find the user document in the collection
    user_dict = user_collection.find_one(filter={"user_id": user_id})

    # Get the existing map scale and parameter state from the user document
    ex_map_size = user_dict['map_size']
    state = user_dict['parameter_state']

    # Check if the parameter state is 'size'
    if state == 'size':
        # Prepare the updates to be applied to the user document
        updates = {'$set': {
            'parameter_state': '',
            'map_size': map_size
        }}

        # Apply the updates to the user document
        user_collection.update_one({"user_id": user_id}, update=updates)
    else:
        # Log an error if user tries to change map size with an invalid state
        logger.error(f"User id {user_id} tries to change map size with state {state}")
        return False

    # Log the successful setting of map scale option
    logger.debug(f"Setting map size option for user id {user_id} from {ex_map_size} to {map_size}")
    return True