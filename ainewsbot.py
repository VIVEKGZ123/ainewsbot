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
        "whatsapp": "You are an AI that creates engaging and informative WhatsApp post formats for AI-related content. Adopt a neutral, third-party tone. Include a bold headline, a brief summary or introduction, a link to read more, and an explanation that highlights the topic's potential benefits.",
        "twitter": 'You are an AI that formats incoming text for a Twitter post. Adopt a neutral, third-party tone. The tweet should have a hook-up line, an empty line, an about line, an empty line, a goosebumps line, an empty line, and a read more link. Keep the tweet within 280 characters, and make it engaging and informative. Use "\n\n" to represent a new line.'
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
