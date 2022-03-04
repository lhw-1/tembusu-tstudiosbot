from telegram.ext import *
import handler as handler
import logging as logging
import os as os
PORT = int(os.environ.get('PORT', 443))
TOKEN = os.environ.get('TOKEN')

# Sets up an Updater (which continuously updates the bot with messages) named updater. 
updater = Updater(TOKEN, use_context=True)

# Sets up a dispatcher (which dispatches commands to the Bot) named dispatcher.
dispatcher = updater.dispatcher

# TODO Securely store the token. Currently using token publicly since the github repo is private.

# Records logs, useful if you want to handle errors in the future.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Conversation Handler State variables
LOAN_1, LOAN_2, LOAN_3, LOAN_4, LOAN_5, LOAN_6, LOAN_7 = range(7)
ADD_1 = range(1)
APPROVE_1, APPROVE_2 = range(2)
RETURN_1, RETURN_2 = range(2)
OPENHOUSE_1, OPENHOUSE_2 = range(2)

# Conversation Handler for Loan
convhandler_loan = ConversationHandler(
    entry_points = [CommandHandler('loan', handler.loan)],
    states = {
        LOAN_1: [CallbackQueryHandler(handler.loan_name)],
        LOAN_2: [CallbackQueryHandler(handler.loan_num)],
        LOAN_3: [CallbackQueryHandler(handler.loan_start)],
        LOAN_4: [CallbackQueryHandler(handler.loan_end)],
        LOAN_5: [CallbackQueryHandler(handler.loan_purpose)],
        LOAN_6: [CallbackQueryHandler(handler.loan_purpose_house)],
        LOAN_7: [MessageHandler(Filters.text, handler.loan_purpose_text)]
    },
    fallbacks = [CommandHandler('loan', handler.loan)]
)

convhandler_add = ConversationHandler(
    entry_points = [CommandHandler('add', handler.add)],
    states = {
        ADD_1: [MessageHandler(Filters.text, handler.add_name)]
    },
    fallbacks = [CommandHandler('add', handler.add)]
)

convhandler_approve = ConversationHandler(
    entry_points = [CommandHandler('approve', handler.approve)],
    states = {
        APPROVE_1: [CallbackQueryHandler(handler.approve_choice)],
        APPROVE_2: [CallbackQueryHandler(handler.approve_result)]
    },
    fallbacks = [CommandHandler('approve', handler.approve)]
)

convhandler_return = ConversationHandler(
    entry_points = [CommandHandler('return', handler.return_loan)],
    states = {
        RETURN_1: [CallbackQueryHandler(handler.return_choice)],
        RETURN_2: [CallbackQueryHandler(handler.return_result)]
    },
    fallbacks = [CommandHandler('return', handler.return_loan)]
)

convhandler_openhouse = ConversationHandler(
    entry_points = [CommandHandler('openhouse22', handler.return_openhouse)],
    states = {
        OPENHOUSE_1: [CallbackQueryHandler(handler.openhouse_name)],
        OPENHOUSE_2: [CallbackQueryHandler(handler.openhouse_num)],
    },
    fallbacks = [CommandHandler('openhouse22', handler.openhouse)]
)

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler('start', handler.start))
dispatcher.add_handler(CommandHandler('boop', handler.boop))
dispatcher.add_handler(CommandHandler('contacts', handler.contacts))
dispatcher.add_handler(CommandHandler('check', handler.check))
dispatcher.add_handler(convhandler_loan)
dispatcher.add_handler(convhandler_add)
dispatcher.add_handler(convhandler_approve)
dispatcher.add_handler(convhandler_return)
dispatcher.add_handler(convhandler_openhouse)

# Start the webhook process
updater.start_webhook(listen = "0.0.0.0",
                          port = int(PORT),
                          url_path = TOKEN,
                          webhook_url = 'https://tembusu-tstudiosbot.herokuapp.com/' + TOKEN)
updater.idle()
