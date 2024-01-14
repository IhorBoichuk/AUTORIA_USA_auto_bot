The client wants to buy a used car (Toyota Sequoia), which was imported from the USA to Ukraine. For searching, it uses the auto.ria.com resource and forms a query with search parameters
# Welcome! This project utilizes an API_KEY from https://developers.ria.com/account to access external services. To set up your development environment, follow the instructions below.

1. Create A Telegram Bot Using Telegram’s BotFather
Open your telegram app and search for BotFather. (A built-in Telegram bot that helps users create custom Telegram bots)
Type /newbot to create a new bot
Give your bot a name & a username
Copy your new Telegram bot’s token

2. You will also need to know your own telegram user ID, so the bot knows who to send messages to. Talk to @userinfobot to get this information. Once again, copy this information down somewhere.

in Docker-compose.yml file:  
set YOUR_API_KEY=API_KEY you get from https://developers.ria.com/account  
set CHAT_ID=your own telegram user ID  
set API_KEY=Telegram bot’s token  

 

# up container
docker-compose up --build --force-recreate  

# endpoints
http://127.0.0.1:8000/  
