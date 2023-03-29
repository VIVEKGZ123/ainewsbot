import os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Set up OpenAI API key
openai.api_key = "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"

# Set up Telegram bot token
TELEGRAM_BOT_TOKEN = "5801244180:AAGiqOifWWREYbtKoVMFFdTS0FKdwHOrGe8"

# ChatGPT conversation function
def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

model_id = 'gpt-3.5-turbo'

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me the content you want to format.")

def content_received(update: Update, context: CallbackContext):
    context.user_data["content"] = update.message.text
    keyboard = [
        [
            InlineKeyboardButton("WhatsApp", callback_data="whatsapp"),
            InlineKeyboardButton("Twitter", callback_data="twitter"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a format:", reply_markup=reply_markup)

def format_option(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    content = context.user_data["content"]
    format_type = query.data

    system_prompt = {
        "whatsapp": "I manage a ai WhatsApp group account where I share updates on the latest developments in the field of AI. This includes information on who is working on AI, the latest updates, upcoming events, and recent news.I want you to act as a social media manager an AI assistant who can help me with content writing by formatting my random content into the best possible format for posting on WhatsApp. I will provide you with the content, and you will send it back to me in the ideal format for my social media channels. For WhatsApp posts, you use a maximum of 500 characters and a minimum of 300 characters long post , At the end of the post, please add my thought to the news. makes sure to use line gap and line space and word space to the post to make to atrrctive post .  My first suggestion request is:",
        "twitter": 'I manage an ai news Twitter account where I share updates on the latest developments in the field of AI. This includes information on who is working on AI, the latest updates, upcoming events, and recent news. I want you to act as a social media manager and an AI assistant who can help me with content writing by formatting my random content into the best possible format for posting on Twitter. I will provide you with the content, and you will send it back to me in the ideal format for my social media channels. For twitter posts, you use a maximum of 280 characters and a minimum of 250 characters post. My first suggestion request is: '
    }

    conversation = [
        {"role": "system", "content": system_prompt[format_type]},
        {"role": "user", "content": content},
    ]
    conversation = ChatGPT_conversation(conversation)
    formatted_text = conversation[-1]["content"]

    query.edit_message_text(text=f"Formatted {format_type} content:\n\n{formatted_text}")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, content_received))
    dp.add_handler(CallbackQueryHandler(format_option))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
