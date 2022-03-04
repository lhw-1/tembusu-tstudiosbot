from oauth2client.service_account import ServiceAccountCredentials
from telegram import *
from telegram.ext import *
import credentials as credentials
import keyboard as key
import txt as txt
import datetime
import gspread
import tstudios_contacts as tcontacts
import os as os

################################################################################################################################
# Google sheet variables
################################################################################################################################

# Service Account Access
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials.credentials_dict)
client = gspread.authorize(creds)
googlesheet_loan = client.open_by_url(os.environ.get('LOANSHEET'))
googlesheet_admin = client.open_by_url(os.environ.get('ADMINSHEET'))



################################################################################################################################
# Program variables
################################################################################################################################
username = 'N/A'
current_request = {} # Has id, quantity, start, end, purpose
LOAN_1, LOAN_2, LOAN_3, LOAN_4, LOAN_5, LOAN_6, LOAN_7 = range(7)
OPENHOUSE_1, OPENHOUSE_2 = range(2)
ADD_1 = range(1)
APPROVE_1, APPROVE_2 = range(2)
RETURN_1, RETURN_2 = range(2)
list_equipment = googlesheet_loan.worksheet("tStudios Equipment List").col_values(2)
list_cat_types = googlesheet_loan.worksheet("tStudios Equipment List").col_values(9)
list_cat_count = googlesheet_loan.worksheet("tStudios Equipment List").col_values(10)
list_cat_index = googlesheet_loan.worksheet("tStudios Equipment List").col_values(11)
list_types = [type[2:] for type in list_cat_types[3:]]



################################################################################################################################
# Basics
################################################################################################################################

# Function for /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt.start)

# Function for /boop
def boop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="... I wasn't sleeping! :(")

# Function for /contact
def contacts(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=tcontacts.contacts)

################################################################################################################################
# For Open House 22: Open house
################################################################################################################################

# Function for /loan
def openhouse(update, context):

    # Set username
    global username
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle

    # Initial message
    update.message.reply_text("Hey there! These are the equipment that are available for loan to all students " + "\U0001F601" + "\n\nYou can check how many of each equipment are available by clicking on the equipment name!", reply_markup=key.oh_init)

    # Set state
    return OPENHOUSE_1

def openhouse_name(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global list_equipment
    global list_cat_types
    global list_cat_count
    global list_cat_index
    global list_types

    # Change reply and keyboard markup according to the user's answer
    if choice == "c":
        list_index = int(list_cat_index[1])
        list_start = list_index - 1
        list_end = list_start + int(list_cat_count[1])
        list_items = list_equipment[list_start:list_end]
        query.message.edit_reply_markup(reply_markup=key.oh_items(list_items, list_index))
        return OPENHOUSE_1
    elif choice == "l":
        list_index = int(list_cat_index[2])
        list_start = list_index - 1
        list_end = list_start + int(list_cat_count[2])
        list_items = list_equipment[list_start:list_end]
        query.message.edit_reply_markup(reply_markup=key.oh_items(list_items, list_index))
        return OPENHOUSE_1
    elif choice[0] == "a":
        if len(choice) == 1:
            query.message.edit_reply_markup(reply_markup=key.oh_type(list_types))
            return OPENHOUSE_1
        else:
            type_index = int(choice[1]) + 3
            list_index = int(list_cat_index[type_index])
            list_start = list_index - 1
            list_end = list_start + int(list_cat_count[type_index])
            list_items = list_equipment[list_start:list_end]
            query.message.edit_reply_markup(reply_markup=key.oh_items(list_items, list_index))
            return OPENHOUSE_1
    elif choice[0] == "e":
        # Open the inventory sheet and get the available quantity
        invsheet = googlesheet_loan.worksheet("tStudios Equipment List")
        quantity = int(invsheet.cell(int(choice[1:]), 6).value)
        # Set message and keyboard markup according to quantity
        if quantity == 0:
            query.edit_message_text(text="Ye... all of this particular equipment is out on loan currently " + "\U0001F622")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="b")]]))
            return OPENHOUSE_2
        else:
            # limit = quantity if quantity < 2 else 2
            # Create the keyboard
            # keylist_quantity = [None] * (limit + 1)
            # for i in range(limit + 1):
            #     if i == limit:
            #         keylist_quantity[i] = [InlineKeyboardButton("Back", callback_data="b")]
            #     else:
            #         keylist_quantity[i] = [InlineKeyboardButton(str(i + 1), callback_data="0" + str(i + 1))]
            query.edit_message_text(text="We have " + str(quantity) + " available of those!")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="b")]]))
            return OPENHOUSE_2
    elif choice == "b":
        query.message.edit_reply_markup(reply_markup=key.oh_init)
        return OPENHOUSE_1
    elif choice == "cancel":
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="Alright, use /openhouse22 to have another look!")
        return ConversationHandler.END
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        return ConversationHandler.END

def openhouse_num(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data

    # Change reply and keyboard markup according to the user's answer
    if choice == "b":
        query.edit_message_text(text="Which other equipment do you wanna look at?")
        query.message.edit_reply_markup(reply_markup=key.key_init)
        return OPENHOUSE_1
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error... Please try /openhouse again, sorry!.")
        return ConversationHandler.END


################################################################################################################################
# Main Feature: Loan
################################################################################################################################

# Function for /loan
def loan(update, context):

    # Set username
    global username
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle

    usersheet = googlesheet_admin.worksheet("Users")
    cell_list_users = usersheet.findall(username)
    check = len(cell_list_users) > 0

    if check:
        # Initial message
        update.message.reply_text(txt.loan_txt + "Which kind of equipment would you like to request for?", reply_markup=key.key_init)

        # Set state
        return LOAN_1
    else:
        # Initial message
        update.message.reply_text("You are not authorised to perform this function.")

        # Set state
        return ConversationHandler.END

def loan_name(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request
    global list_equipment
    global list_cat_types
    global list_cat_count
    global list_cat_index
    global list_types

    # Change reply and keyboard markup according to the user's answer
    if choice == "c":
        list_index = int(list_cat_index[1])
        list_start = list_index - 1
        list_end = list_start + int(list_cat_count[1])
        list_items = list_equipment[list_start:list_end]
        query.message.edit_reply_markup(reply_markup=key.key_items(list_items, list_index))
        return LOAN_1
    elif choice == "l":
        list_index = int(list_cat_index[2])
        list_start = list_index - 1
        list_end = list_start + int(list_cat_count[2])
        list_items = list_equipment[list_start:list_end]
        query.message.edit_reply_markup(reply_markup=key.key_items(list_items, list_index))
        return LOAN_1
    elif choice[0] == "a":
        if len(choice) == 1:
            query.message.edit_reply_markup(reply_markup=key.key_type(list_types))
            return LOAN_1
        else:
            type_index = int(choice[1]) + 3
            list_index = int(list_cat_index[type_index])
            list_start = list_index - 1
            list_end = list_start + int(list_cat_count[type_index])
            list_items = list_equipment[list_start:list_end]
            query.message.edit_reply_markup(reply_markup=key.key_items(list_items, list_index))
            return LOAN_1
    elif choice[0] == "e":
        # Obtain the current equipment id
        current_request["id"] = int(choice[1:])
        # Open the inventory sheet and get the available quantity
        invsheet = googlesheet_loan.worksheet("tStudios Equipment List")
        quantity = int(invsheet.cell(int(choice[1:]), 6).value)
        # Set message and keyboard markup according to quantity
        if quantity == 0:
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
            query.edit_message_text(text="Sorry, the item you requested is not available. Use /loan to make another request!")
            current_request = {}
            return ConversationHandler.END
        else:
            limit = quantity if quantity < 2 else 2
            # Create the keyboard
            keylist_quantity = [None] * (limit + 1)
            for i in range(limit + 1):
                if i == limit:
                    keylist_quantity[i] = [InlineKeyboardButton("Back", callback_data="b")]
                else:
                    keylist_quantity[i] = [InlineKeyboardButton(str(i + 1), callback_data="0" + str(i + 1))]
            query.edit_message_text(text="We have " + str(quantity) + " available of those. How many would you like to request for loan?")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keylist_quantity))
            return LOAN_2
    elif choice == "b":
        query.message.edit_reply_markup(reply_markup=key.key_init)
        return LOAN_1
    elif choice == "idk":
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="We are currently in the process of implementing a user guide.\n\nUntil then, please ask " + tcontacts.head_name + " at " + tcontacts.head_handle + " what would be the best for you!")
        current_request = {}
        return ConversationHandler.END
    elif choice == "cancel":
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="Your request has been cancelled. Use /loan to make another request!")
        current_request = {}
        return ConversationHandler.END
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

def loan_num(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request

    # Change reply and keyboard markup according to the user's answer
    if choice == "b":
        query.edit_message_text(text=txt.loan_txt + "Which kind of equipment would you like to request for?")
        query.message.edit_reply_markup(reply_markup=key.key_init)
        return LOAN_1
    elif choice[0] == "0":
        current_request["quantity"] = int(choice[1:])
        query.edit_message_text(text="Alright, great.\n\n" + txt.loan_txt + "Please indicate the START of your requested loan period!")
        query.message.edit_reply_markup(reply_markup=key.key_start())
        return LOAN_3
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

def loan_start(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "s":
        current_request["start"] = choice[1:]
        query.edit_message_text(text="Alright, nice.\n\n" + txt.loan_txt + "Please indicate the END of your requested loan period!")
        query.message.edit_reply_markup(reply_markup=key.key_end(choice[1:]))
        return LOAN_4
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

def loan_end(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "n":
        current_request["end"] = choice[1:]
        query.edit_message_text(text="Alright! Finally, please tell us why you are requesting this loan.")
        query.message.edit_reply_markup(reply_markup=key.key_purpose)
        return LOAN_5
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

def loan_purpose(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request
    global username

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "p":
        # Set waiting message
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="Please wait while we process your request...")

        # Purpose is either CSC Event or Arts Council Event
        invsheet = googlesheet_loan.worksheet("tStudios Equipment List")
        loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

        # Set variables
        request_id = len(loansheet.col_values(1))
        request_user = username
        request_purpose = choice[1:]
        equipment_id = str(current_request["id"])
        equipment_quantity = str(current_request["quantity"])
        row = str(request_id + 1)

        # Set request period
        start_month = datetime.datetime.strptime(str(int(current_request["start"][0:2])), "%m").strftime("%B")
        start_day = str(int(current_request["start"][2:]))
        start = start_day + " " + start_month

        end_month = datetime.datetime.strptime(str(int(current_request["end"][0:2])), "%m").strftime("%B")
        end_day = str(int(current_request["end"][2:]))
        end = end_day + " " + end_month

        request_period = start + " - " + end

        # Update sheet
        loansheet.update('A' + row, request_id)
        loansheet.update('B' + row, "NO")
        loansheet.update('C' + row, "-")
        loansheet.update('D' + row, "NO")
        loansheet.update('E' + row, "-")
        loansheet.update('F' + row, request_user)
        loansheet.update('G' + row, request_purpose)
        loansheet.update('H' + row, request_period)
        loansheet.update('I' + row, equipment_quantity)
        loansheet.update('J' + row, equipment_id)
        
        # Set request confirmation message
        equipment_name = invsheet.cell(equipment_id, 2).value
        request_final = "You have requested for " + str(equipment_quantity) + " x " + equipment_name + ", to be loaned during the following period: " + request_period + ", for the following reasons: " + request_purpose + ".\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=request_final + txt.request_process)      

        # Set state
        current_request = {}
        return ConversationHandler.END

    elif choice[0] == "h":
        # Purpose is House Event
        current_request["purpose"] = choice[1:]
        query.edit_message_text(text="Alright. Which House are you requesting under?")
        query.message.edit_reply_markup(reply_markup=key.key_house)
        return LOAN_6
    elif choice[0] == "t":
        # Purpose is either IG Activities or Student-led Initiatives
        current_request["purpose"] = choice[1:]
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        if choice[1] == "I":
            query.edit_message_text(text="Alright. Please type in which IG you are from.")
        else:
            query.edit_message_text(text="Alright. Please type in details regarding your initiative.")
        return LOAN_7
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

def loan_purpose_house(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data
    global current_request
    global username

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "x":
        # Set waiting message
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="Please wait while we process your request...")

        # Purpose is House Event
        invsheet = googlesheet_loan.worksheet("tStudios Equipment List")
        loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

        # Set variables
        request_id = len(loansheet.col_values(1))
        request_user = username
        request_purpose = current_request["purpose"] + choice[1:]
        equipment_id = str(current_request["id"])
        equipment_quantity = str(current_request["quantity"])
        row = str(request_id + 1)

        # Set request period
        start_month = datetime.datetime.strptime(str(int(current_request["start"][0:2])), "%m").strftime("%B")
        start_day = str(int(current_request["start"][2:]))
        start = start_day + " " + start_month

        end_month = datetime.datetime.strptime(str(int(current_request["end"][0:2])), "%m").strftime("%B")
        end_day = str(int(current_request["end"][2:]))
        end = end_day + " " + end_month

        request_period = start + " - " + end

        # Update sheet
        loansheet.update('A' + row, request_id)
        loansheet.update('B' + row, "NO")
        loansheet.update('C' + row, "-")
        loansheet.update('D' + row, "NO")
        loansheet.update('E' + row, "-")
        loansheet.update('F' + row, request_user)
        loansheet.update('G' + row, request_purpose)
        loansheet.update('H' + row, request_period)
        loansheet.update('I' + row, equipment_quantity)
        loansheet.update('J' + row, equipment_id)
        
        # Set request confirmation message
        equipment_name = invsheet.cell(equipment_id, 2).value
        request_final = "You have requested for " + str(equipment_quantity) + " x " + equipment_name + ", to be loaned during the following period: " + request_period + ", for the following reasons: " + request_purpose + ".\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=request_final + txt.request_process)      

        # Set state
        current_request = {}
        return ConversationHandler.END

    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")
        current_request = {}
        return ConversationHandler.END

# Function for /loan to get loan period
def loan_purpose_text(update, context):

    # Retrieve the reply (in the form of message data) from user
    text = update.message.text
    global current_request
    global username

    # Purpose is given as message
    request_purpose = current_request["purpose"] + text

    # Set waiting message
    update.message.reply_text(text="Please wait while we process your request...")

    # Open sheets
    invsheet = googlesheet_loan.worksheet("tStudios Equipment List")
    loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

    # Set variables
    request_id = len(loansheet.col_values(1))
    request_user = username
    equipment_id = str(current_request["id"])
    equipment_quantity = str(current_request["quantity"])
    row = str(request_id + 1)

    # Set request period
    start_month = datetime.datetime.strptime(str(int(current_request["start"][0:2])), "%m").strftime("%B")
    start_day = str(int(current_request["start"][2:]))
    start = start_day + " " + start_month

    end_month = datetime.datetime.strptime(str(int(current_request["end"][0:2])), "%m").strftime("%B")
    end_day = str(int(current_request["end"][2:]))
    end = end_day + " " + end_month

    request_period = start + " - " + end

    # Update sheet
    loansheet.update('A' + row, request_id)
    loansheet.update('B' + row, "NO")
    loansheet.update('C' + row, "-")
    loansheet.update('D' + row, "NO")
    loansheet.update('E' + row, "-")
    loansheet.update('F' + row, request_user)
    loansheet.update('G' + row, request_purpose)
    loansheet.update('H' + row, request_period)
    loansheet.update('I' + row, equipment_quantity)
    loansheet.update('J' + row, equipment_id)
    
    # Set request confirmation message
    equipment_name = invsheet.cell(equipment_id, 2).value
    request_final = "You have requested for " + str(equipment_quantity) + " x " + equipment_name + ", to be loaned during the following period: " + request_period + ", for the following reasons: " + request_purpose + ".\n\n"
    update.message.reply_text(text=request_final + txt.request_process)

    # Set state
    current_request = {}
    return ConversationHandler.END



################################################################################################################################
# Feature: Check Loan
################################################################################################################################

# Function for /check
def check(update, context):

    # Set initial message
    context.bot.send_message(chat_id=update.effective_chat.id, text="Checking... Please wait.")

    # Set username
    global username
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle

    usersheet = googlesheet_admin.worksheet("Users")
    cell_list_users = usersheet.findall(username)
    check = len(cell_list_users) > 0

    if check:
        # Open and query google sheet
        loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

        # Check all requests that have not been approved yet
        req_cell_list_raw = loansheet.findall(username)

        # Filter out cells with "NO" not in Column 2
        def check_col_six(cell):
            if cell.col == 6:
                return True
            return False
        req_cell_list = list(filter(check_col_six, req_cell_list_raw))

        # Create message / keys accordingly
        rcl_len = len(req_cell_list)
        if rcl_len == 0:
            update.message.reply_text("Sorry, there aren't any requests under your name.\n\nIf there should be, please contact the development team. Thank you!")
        else:
            request_txt = ""
            for x in range(rcl_len):
                cell = req_cell_list[x]
                row = cell.row
                values_list = loansheet.row_values(row)
                request_txt = request_txt + "Request " + str(x + 1) + ": " + values_list[10] + " x " + values_list[8] + "\nLoan period: " + values_list[7] + "\nPurpose: " + values_list[6] + "\nRequest ID: " + values_list[0] + "\nApproved: " + values_list[1] + "\nReturned: " +  values_list[3] + "\n\n"
            update.message.reply_text(request_txt + "If there are any issues, please contact the development team with the relevant Request ID. Thank you!")
    
    else:
        update.message.reply_text("You are not authorised to perform this function.")



################################################################################################################################
# Feature: (ADMIN) Add User
################################################################################################################################

# Function for /add
def add(update, context):

    # Set username
    global username
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle
    
    # Open and query admin sheet
    adminsheet = googlesheet_admin.worksheet("Administrators")
    cell_list_admin = adminsheet.findall(username)

    # Check if user is admin
    if (len(cell_list_admin) > 0):
        # Show query message
        update.message.reply_text("Please type in the telegram handle of the user you wish to add.\n\nThe format should be: \"@HANDLE\".")
        
        # Change state
        return ADD_1
    else:
        # Show unauthorised message
        update.message.reply_text("You are not authorised to perform this function.")
        
        # Change state
        return ConversationHandler.END

def add_name(update, context):

    # Retrieve the reply (in the form of message data) from user
    text = update.message.text

    # Update the usersheet accordingly
    usersheet = googlesheet_admin.worksheet("Users")
    user_row = str(len(usersheet.col_values(1)) + 1)
    usersheet.update('A' + user_row, text)
    update.message.reply_text("The user " + text + " has been added as an approved user of tStudios Loan Bot!")

    # Change state
    return ConversationHandler.END



################################################################################################################################
# Feature: (ADMIN) Approve Loan
################################################################################################################################

# Function for /approve
def approve(update, context):
    
    # Send an initial message
    context.bot.send_message(chat_id=update.effective_chat.id, text="Checking... Please wait.")

    # Gets the global username variable
    global username

    # Sets the username variable to one with the @ + handle (If user has no handle, obtains their telegram name instead)
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle
    
    # Open and query admin sheet
    adminsheet = googlesheet_admin.worksheet("Administrators")
    cell_list_admin = adminsheet.findall(username)

    # Check if user is admin
    if (len(cell_list_admin) > 0):
        # Open the Equipment Loan Records worksheet
        loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

        # Check all requests that have not been approved yet
        req_cell_list_raw = loansheet.findall("NO")

        # Filter out cells with "NO" not in Column 2
        def check_col_two(cell):
            if cell.col == 2:
                return True
            return False
        req_cell_list = list(filter(check_col_two, req_cell_list_raw))

        # Create message / keys accordingly
        rcl_len = len(req_cell_list)
        if rcl_len == 0:
            update.message.reply_text("There are no outstanding loan requests.\n\nIf there should be, please contact the development team.")
        else:
            req_list = [None] * rcl_len
            for i in range(rcl_len):
                row = req_cell_list[i].row
                values_list = loansheet.row_values(row)
                req_list[i] = [InlineKeyboardButton("Request ID " + values_list[0] + ": \n" + values_list[10] + " x " + values_list[8], callback_data="R" + values_list[0])]
            req_key = InlineKeyboardMarkup(req_list)
            update.message.reply_text("Below are the outstanding loan requests yet to be approved:", reply_markup=req_key)
        
        # Change state
        return APPROVE_1
    else:
        # Show unauthorised message
        update.message.reply_text("You are not authorised to perform this function.", reply_markup=InlineKeyboardMarkup([]))
        
        # Change state
        return ConversationHandler.END

def approve_choice(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data

    # Open the Equipment Loan Records worksheet
    loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "R":
        req_app_id = int(choice[1:])
        row = req_app_id + 1
        values_list = loansheet.row_values(row)
        req_app_user = values_list[5]
        req_app_eq = values_list[10]
        req_app_qt = values_list[8]
        req_app_pd = values_list[7]
        req_app_pp = values_list[6]
        req_details = "Request ID: " + choice[1:] + "\nRequest from: " + req_app_user + "\nRequested Items: " + req_app_eq + " x " + req_app_qt + "\nRequested Period: " + req_app_pd + "\nRequest Reason: " + req_app_pp + "\n\nApprove this Request?"
        req_app = InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve", callback_data="A" + choice[1:])],
            [InlineKeyboardButton("Back", callback_data="C")]
        ])
        query.edit_message_text(text=req_details)
        query.message.edit_reply_markup(reply_markup=req_app)
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")

    # Change state
    return APPROVE_2

def approve_result(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data

    # Gets the global username variable
    global username

    # Open the Equipment Loan Records worksheet
    loansheet = googlesheet_loan.worksheet("Equipment Loan Records")
    invsheet = googlesheet_loan.worksheet("tStudios Equipment List")

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "A":

        # Get equipment id and quantity from loan request
        equipment_id = loansheet.acell('J' + str(int(choice[1:]) + 1)).value
        equipment_count = int(loansheet.acell('I' + str(int(choice[1:]) + 1)).value)

        # Get quantity (available and loaned) of equipment
        count_available = int(invsheet.acell('F' + equipment_id).value)
        count_loaned = int(invsheet.acell('G' + equipment_id).value)

        if (count_available == 0):

            # Warn that request could not be approved
            query.edit_message_text(text="Request ID " + choice[1:] + " could NOT be approved because the equipment requested for loan is no longer available.")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

        else:

            # Update quantity (available and loaned) of equipment
            invsheet.update('F' + equipment_id, count_available - equipment_count)
            invsheet.update('G' + equipment_id, count_loaned + equipment_count)

            # Mark as approved
            loansheet.update('B' + str(int(choice[1:]) + 1), "YES")
            loansheet.update('C' + str(int(choice[1:]) + 1), username)

            # Set markup and message
            query.edit_message_text(text="Request ID " + choice[1:] + " has been approved.\n\nYou can confirm the approval at:\n" + os.environ.get('LOANSHEET') + ".")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

    elif choice == "C":
        query.edit_message_text(text="Request Approval cancelled.\n\nPlease use /approve again if you want to approve another loan request.")
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")

    # Change state to END
    return ConversationHandler.END



################################################################################################################################
# Feature: (ADMIN) Return Loan
################################################################################################################################

# Function for /return
def return_loan(update, context):
    
    # Send an initial message
    context.bot.send_message(chat_id=update.effective_chat.id, text="Checking... Please wait.")

    # Gets the global username variable
    global username

    # Sets the username variable to one with the @ + handle (If user has no handle, obtains their telegram name instead)
    handle = update.message.chat.username
    if handle == '':
        username = update.message.chat.first_name + ' ' + update.message.chat.last_name
    else:
        username = "@" + handle
    
    # Open and query admin sheet
    adminsheet = googlesheet_admin.worksheet("Administrators")
    cell_list_admin = adminsheet.findall(username)

    # Check if user is admin
    if (len(cell_list_admin) > 0):
        # Open the Equipment Loan Records worksheet
        loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

        # Check all requests that have not been approved yet
        req_cell_list_raw = loansheet.findall("NO")

        # Filter out cells with "NO" not in Column 2
        def check_col_four(cell):
            if cell.col == 4:
                return True
            return False
        req_cell_list = list(filter(check_col_four, req_cell_list_raw))

        # Create message / keys accordingly
        rcl_len = len(req_cell_list)
        if rcl_len == 0:
            update.message.reply_text("There are no unreturned loans.\n\nIf there should be, please contact the development team.")
        else:
            req_list = [None] * rcl_len
            for i in range(rcl_len):
                row = req_cell_list[i].row
                values_list = loansheet.row_values(row)
                if values_list[1] == "NO":
                    req_list[i] = [InlineKeyboardButton("Request ID " + values_list[0] + ": \n" + values_list[10] + " x " + values_list[8] + "\n(Not Approved)", callback_data="N" + values_list[0])]
                else:
                    req_list[i] = [InlineKeyboardButton("Request ID " + values_list[0] + ": \n" + values_list[10] + " x " + values_list[8] + "\n(Approved)", callback_data="R" + values_list[0])]
            req_key = InlineKeyboardMarkup(req_list)
            update.message.reply_text("Below are the loans yet to be returned:", reply_markup=req_key)
        
        # Change state
        return RETURN_1
    else:
        # Show unauthorised message
        update.message.reply_text("You are not authorised to perform this function.", reply_markup=InlineKeyboardMarkup([]))
        
        # Change state
        return ConversationHandler.END

def return_choice(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data

    # Open the Equipment Loan Records worksheet
    loansheet = googlesheet_loan.worksheet("Equipment Loan Records")

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "R":
        req_app_id = int(choice[1:])
        row = req_app_id + 1
        values_list = loansheet.row_values(row)
        req_app_user = values_list[5]
        req_app_eq = values_list[10]
        req_app_qt = values_list[8]
        req_app_pd = values_list[7]
        req_app_pp = values_list[6]
        req_details = "Request ID: " + choice[1:] + "\nRequest from: " + req_app_user + "\nRequested Items: " + req_app_eq + " x " + req_app_qt + "\nRequested Period: " + req_app_pd + "\nRequest Reason: " + req_app_pp + "\n\nMark this loan as returned?"
        req_app = InlineKeyboardMarkup([
            [InlineKeyboardButton("Return", callback_data="A" + choice[1:])],
            [InlineKeyboardButton("Cancel", callback_data="C")]
        ])
        query.edit_message_text(text=req_details)
        query.message.edit_reply_markup(reply_markup=req_app)
    elif choice[0] == "N":
        req_app_id = int(choice[1:])
        row = req_app_id + 1
        values_list = loansheet.row_values(row)
        req_app_user = values_list[5]
        req_app_eq = values_list[10]
        req_app_qt = values_list[8]
        req_app_pd = values_list[7]
        req_app_pp = values_list[6]
        req_details = "Request ID: " + choice[1:] + "\nRequest from: " + req_app_user + "\nRequested Items: " + req_app_eq + " x " + req_app_qt + "\nRequested Period: " + req_app_pd + "\nRequest Reason: " + req_app_pp + "\n\nThis loan request has not been approved yet, and cannot be returned."
        req_app = InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel", callback_data="C")]
        ])
        query.edit_message_text(text=req_details)
        query.message.edit_reply_markup(reply_markup=req_app)
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")

    # Change state
    return RETURN_2

def return_result(update, context):

    # Retrieve the reply (in the form of query data) from user
    query = update.callback_query
    query.answer()
    choice = query.data

    # Gets the global username variable
    global username

    # Open the Equipment Loan Records worksheet
    loansheet = googlesheet_loan.worksheet("Equipment Loan Records")
    invsheet = googlesheet_loan.worksheet("tStudios Equipment List")

    # Change reply and keyboard markup according to the user's answer
    if choice[0] == "A":

        # Get equipment id and quantity from loan request
        equipment_id = loansheet.acell('J' + str(int(choice[1:]) + 1)).value
        equipment_count = int(loansheet.acell('I' + str(int(choice[1:]) + 1)).value)

        # Get quantity (available and loaned) of equipment
        count_available = int(invsheet.acell('F' + equipment_id).value)
        count_loaned = int(invsheet.acell('G' + equipment_id).value)

        if (count_loaned == 0):

            # Warn that request could not be approved
            query.edit_message_text(text="Request ID " + choice[1:] + " could NOT be approved because there was an error processing the request.\n\nPlease contact the developer for assistance. Thank you!")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

        else:

            # Update quantity (available and loaned) of equipment
            invsheet.update('F' + equipment_id, count_available + equipment_count)
            invsheet.update('G' + equipment_id, count_loaned - equipment_count)

            # Mark as returned
            loansheet.update('D' + str(int(choice[1:]) + 1), "YES")
            loansheet.update('E' + str(int(choice[1:]) + 1), username)

            # Set markup and message
            query.edit_message_text(text="Request ID " + choice[1:] + " has been returned.\n\nYou can confirm that the loan has been returned at:\n" + os.environ.get('LOANSHEET') + ".")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

    elif choice == "C":
        query.edit_message_text(text="Request Return cancelled.\n\nPlease use /return again if you want to mark another loan as returned.")
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    else:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        query.edit_message_text(text="There was an error processing your request. Please try again.")

    # Change state to END
    return ConversationHandler.END
