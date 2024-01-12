# Task Description
## What?
A Telegram bot for playing the "GeoGuesser" game.
## Why?
To enable users to play a simple game with the bot.
## Bot Capabilities
1. Generate a random country's place from map.
2. Maintain the user's state ("in-game," "not in-game").
3. Track the user's remaining number of attempts.
4. Give a description of user's place, despite of user's answer.
## Additional Functionality
1. The bot can display game statistics for users upon request.
## User Interaction Description
1. The user sends the command /start to the bot (or starts it by finding it in the search).
2. The bot greets the user and suggests playing the "GeoGuesser" game, as well as offers the user to read detailed rules by sending the command /help.
3. At this stage, the user can take 5 actions:
   - Agree to play the game with the bot by sending "Yes," "Let's play," or similar.
   - Decline to play by sending "No," "I don't want to," or similar.
   - Send the command /help to the chat.
   - Send the command /stat to the chat.
   - Send any other message to the chat.
4. The user agrees to play the game:
   - The bot informs the user that it's excited to play and sends a random map.
   - The bot saves information that the user is in the "in-game" state.
   - The bot sets the user's attempt counter to the default value.
   - At this stage, the user can take 3 actions:
     - Send their guess about what place is in map to the chat.
     - Send the command /cancel to the chat.
5. The user sends a guess about what place is in map to the chat:
   - The bot compares the user's name sent with the right name of place.
   - If the names match:
     - The bot congratulates the user on winning and send another place.
     - The bot increases the user's game counter by 1.
   - If the user's name is wrong:
     - The bot decreases the user's attempt counter by one.
     - The bot gives the right answer to the user.
     - The bot sends another place to guess.
6. The user sends the command /cancel to the chat while in the "in-game" state:
   - The bot changes the state from "in-game" to "not in-game."
   - The bot sends a message to the chat indicating that the game has ended.
   - If the current counter of canceled game is higher than user's max counter, then the bot saves canceled game's counter as max counter.
   - The bot sends a message to the chat instructing the user to send a message "Play" or "Let's play" if they want to play again.
7. While in the "in-game" state, the user sends anything other than a proposed answer or the command /cancel:
   - The bot sends a message to the user stating that according to game rules, they can only use proposed answers or the command /cancel to the chat.
8. If the user runs out of attempts:
   - The bot informs the user that they have lost.
   - The bot informs the user of maximum right guessed answers of total amount.
   - The bot changes the state from "in-game" to "not in-game."
   - The bot increases the user's game counter by 1.
   - If the current score is maximum for user's statistic, the the bot sets one as maximum user's score.
   - The bot sends a message to the user inviting them to play again.
9. The user declines to play:
   - The bot sends a message to the user, e.g., "Too bad :(" and provides instructions on what to do if they still want to play.
10. The user sends the command /help:
    - The bot sends the game rules and command description to the user.
11. The user sends the command /stat:
    - The bot sends game statistics (total games played and total games won by the user, maximum score of guessed answers per one game) to the user.
    - The bot sends a message inviting the user to play.
12. The user sends any other message:
    - The bot informs that it doesn't understand and invites them to play again.
