import telebot 
import random 
import re
 
token  =  '8081347183:AAHdrE1x-fYE4CTkt8FT71PXyz2Zbhch2_Y' 
IMAGE_PATH  = 'C:/Users/USER/Downloads/download.png' 
bot  = telebot.TeleBot(token) 
 
afk_users = {} 
 
# Command: /afk 
@bot.message_handler(commands=['afk']) 
def set_afk(message): 
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
 
    # Get the reason for going AFK (if any) 
    afk_reason = message.text[5:].strip()  # Remove '/afk' from the message 
 
    # Set AFK status 
    if afk_reason: 
        afk_users[user_id] = afk_reason 
        bot.reply_to(message, f"{user_name} is now AFK. Reason: {afk_reason}") 
    else: 
        afk_users[user_id] = "No reason provided." 
        bot.reply_to(message, f"{user_name} is now AFK.") 
 
# Handle messages sent to AFK users 
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id in afk_users) 
def notify_afk(message): 
    afk_user_id = message.reply_to_message.from_user.id 
    afk_reason = afk_users.get(afk_user_id, "No reason provided.") 
    bot.reply_to(message, f"The user is currently AFK. Reason: {afk_reason}") 
 
# Handle messages from AFK users to mark them as active 
@bot.message_handler(func=lambda message: message.from_user.id in afk_users) 
def auto_back_from_afk(message): 
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
 
    # Remove AFK status and notify 
    del afk_users[user_id] 
    bot.reply_to(message, f"Welcome back, {user_name}! You're no longer AFK.") 
 
# Polling 
@bot.message_handler(['judge']) 
def judge(message): 
    if message.reply_to_message: 
        repiled_text = message.reply_to_message.text 
        result = random.choice(["Truth", "Lie"]) 
        bot.reply_to(message, f'The statement: "{repiled_text}" is a {result}.') 
    else: 
        bot.reply_to(message, "Reply to a message to judge it as Truth or Lie.") 
 
@bot.message_handler(['start']) 
def handle_start(message): 
    try: 
        # Get user profile photos 
        user_photos = bot.get_user_profile_photos(message.from_user.id) 
         
        if user_photos.total_count > 0: 
            # Get the file_id of the first photo 
            file_id = user_photos.photos[0][-1].file_id 
             
            # Send the user's profile photo 
            bot.send_photo( 
                message.chat.id,  
                file_id,  
                caption=f"✨ Hey, {message.from_user.first_name} ✨\n\n" 
        f"🎉 Welcome to the bot!\n" 
        f"📚 Here, I will help you learn and use the\"Naruto Bot\" 🌀\n\n" 
        f"🌟 Hope you enjoy this journey!🚀\n\n" 
         
        f"🆔 User ID:{message.from_user.id}\n" 
        f"🔰 Name:{message.from_user.first_name} {message.from_user.last_name or ''}\n" 
        f"👤 Username:@{message.from_user.username}\n\n" 
        f"🔥 Let's get started! Type /help to see what I can do,." 
                 
            ) 
        else: 
            bot.reply_to(message, "You don't have a profile photo.") 
    except Exception as e: 
        bot.reply_to(message, "An error occurred: " + str(e)) 
 
# def usernme(message): 
    # username = message.from_user.username 
 
# def welcome(message): 
#     user_id = message.from_user.id 
#     user_name = message.from_user.first_name 
@bot.message_handler(['help']) 
 
def help(message): 
    bot.reply_to(message, "✨ *I can help you with the following commands:* ✨\n\n" 
                          "🔹 /start - Welcome message and profile photo\n" 
                          "🔹 /help - List of available commands\n" 
                          "🔹 /info - Get to know the person who have created this bot\n" 
                          "🔹 /d - Get a random number from 1-9\n" 
                          "🔹 /afk - Set your status as AFK (Away From Keyboard)\n"
                          "🔹 /judge - Judge a statement as Truth or Lie\n" 
                          "🔹 /wish - to see how much you wish can be true\n\n" 
                          "💡 *Tip:* Use these commands to interact with the bot and explore its features!", 
                           
                          parse_mode='Markdown' 
                          ) 
 
 
@bot.message_handler(['d']) 
def dg(message): 
    bot.reply_to(message, "🎲 Your random number is: " + str(random.randint(1, 9)) + "\n\n 💭 Maybe this is your destiny... to rise to unimaginable wealth and power 💰👑, or to face a fall so devastating 🌪️📉 that you'll wish you'd never asked. The number I've chosen holds secrets 🔮—secrets that could change everything... or nothing at all. 😨 Are you ready to face it? 🎲") 
 
 
# Regex to detect mathematical expressions like 4x2, 3+5, etc.
EXPRESSION_PATTERN = re.compile(r'^(\d+)([\+\-\*/x])(\d+)$')


@bot.message_handler(commands=['flip'])
def flip_coin(message):
    result = random.choice(["Heads", "Tails"])
    bot.reply_to(message, f"🪙 The coin landed on: {result}")
    
    
@bot.message_handler(commands=['dice'])
def roll_dice(message):
    bot.send_dice(message.chat.id)  # Sends a real Telegram dice 🎲
        
@bot.message_handler(func=lambda message: True)
def calculate_expression(message):
    match = EXPRESSION_PATTERN.match(message.text.replace(" ", ""))  # Remove spaces
    if match:
        num1, operator, num2 = match.groups()
        
        # Convert numbers to integers
        num1, num2 = int(num1), int(num2)
        
        # Replace 'x' with '*' for multiplication
        if operator == 'x':
            operator = '*'

        try:
            # Evaluate the expression safely
            result = eval(f"{num1} {operator} {num2}")
            bot.reply_to(message, f"🧮 Result: {result}")
        except:
            pass  # Ignore errors (bot stays silent)
    # bot.reply_to(message, "Sorry, I don't understand that command. Type /help to see what I can do.") 
 
 
 
# Command: /wishly_to(message, "🌠 Make a wish and I will tell you how likely it is to come true! 🌠\n\n") 
     
bot.polling()
