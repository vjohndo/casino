# Casino
This markdown outlines the technologies, approach taken, user instruction and unsolved problems of this tic-tac-toe simulator.

# To-do's
- Put commands in for the instructions below
- Udpate the postgreSQL db 
- Combine the player and user models into a single module and with the class, call the methods
- regarding the game states, any change in the database should involve a post, don't allow get methyod


## Techonologies used
---
### Python
- Used to build all models of games
- Pyscopg2 to hand database 
- Bcrypt to handle password hashing
- Pickling to handle game instance storage and access on database

### Flask
- Flask framework to control routes and sessions
- Jinja to handle templating of webpages

### Heroku
- Website is deployed on Heroku

### HTML
- Heavy use of forms for POSTS
- Semantic tags are used to seperate header, main, footer section

### CSS
- Imports google fonts for effects

### JS
- Minor use of JS to add event listeners to toggle classes and allow for routing via buttons

### PSQL
- At this stage 3 tables. Users, game_instances, game_types. 

### Deck of cards API
- Purely used to handle card image requests
- https://deckofcardsapi.com/

## Features
---
- Users and signup, login, logout
- Users can collect a daily currency bonus
- Users can play unique instances of blackjack and five-card poker
- Game instances are preserved and unique for each user, multiple people can make server requests
- Game logic is handled server side, users can not inspect the game and breach security

## Unsolved Problems
---
- CSS needs a refresh
- To implement an about page with instructions
- To implement a profile page, leaderboards and a shop to spend currency
- Add in a 'loading' symbol to smooth transitions
- Develop games into single page applications with async functionality
- Currently games are pickled into the database, to rewrite class construction based on saved JSON files

## Instructions for UI
---
- Login and signup are standards
- Collect your daily bonus cash
- Click on a game type
- Place your bets 
- Play the game


## Instructions for developing
---
- Clone the repo
- Create and activate python virtual environment
- Install requirements and technology 
- Create a database called casino
- Use the database_generation.sql file to create the required tables
- Run app.py

## References
---
- https://deckofcardsapi.com/
- https://en.wikipedia.org/wiki/Video_poker
