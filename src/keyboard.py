from pytz import timezone
from telegram import *
from telegram.ext import *
import datetime

################################################################################################################################
# Keyboards
################################################################################################################################

singaporetime = timezone('Asia/Singapore')
timenow = datetime.datetime.now(singaporetime)

# Initial Choice
key_init = InlineKeyboardMarkup([
    [InlineKeyboardButton("Camera", callback_data="c")],
    [InlineKeyboardButton("Light", callback_data="l")],
    [InlineKeyboardButton("Accessories", callback_data="a")],
    [InlineKeyboardButton("I don't know!", callback_data="idk")],
    [InlineKeyboardButton("Cancel", callback_data="cancel")]
])

# Keyboard generator for any item list.
def key_items(list_items, index):
    # list will be a list of strings that correspond to equipment names.
    # Index will be the equipment index. (First item on the list has an index of 2)
    key_len = len(list_items) + 1
    keylist_items = [None] * (key_len)
    for i in range(key_len):
        if i == key_len - 1:
            # If i is currently pointing to the last index of keylist_items, add the Back button
            keylist_items[i] = [InlineKeyboardButton("Back", callback_data="b")]
        else:
            keylist_items[i] = [InlineKeyboardButton(list_items[i], callback_data="e" + format(i + index, '02d'))]
    items = InlineKeyboardMarkup(keylist_items)
    return items

# Accessory Types
def key_type(list_type):
    # list_type will be a list of strings that correspond to equipment types under "Accessories" category.
    key_len = len(list_type) + 1
    keylist_type = [None] * (key_len)
    for i in range(key_len):
        if i == key_len - 1:
            # If i is currently pointing to the last index of keylist_camera, add the Back button
            keylist_type[i] = [InlineKeyboardButton("Back", callback_data="b")]
        else:
            keylist_type[i] = [InlineKeyboardButton(list_type[i], callback_data="a" + str(i))]
    types = InlineKeyboardMarkup(keylist_type)
    return types

# Loan Period Start Date
def key_start():
    global timenow
    timenow_delta = datetime.date(timenow.year, timenow.month, timenow.day)
    timeweek_delta = timenow_delta + datetime.timedelta(weeks=1)
    keylist_startday = [None] * 13
    for i in range(13):
        i_time = timeweek_delta + datetime.timedelta(days=i)
        i_time_day = str(i_time)[8:]
        i_time_month_str = str(i_time)[5:7]
        i_time_month = datetime.datetime.strptime(str(int(i_time_month_str)), "%m").strftime("%B")
        keylist_startday[i] = [InlineKeyboardButton(str(int(i_time_day)) + " " + i_time_month, callback_data="s" + i_time_month_str + i_time_day)]
    startday = InlineKeyboardMarkup(keylist_startday)
    return startday

# Loan Period End Date
def key_end(mmdd):
    global timenow
    timestart_delta = datetime.date(timenow.year, int(mmdd[0:2]), int(mmdd[2:]))
    timestart_month = datetime.datetime.strptime(str(int(mmdd[0:2])), "%m").strftime("%B")
    keylist_endday = [None] * 3
    keylist_endday[0] = [InlineKeyboardButton(str(int(mmdd[2:])) + " " + timestart_month, callback_data="n" + mmdd[0:2] + mmdd[2:])]
    for j in range(2):
        j_time = timestart_delta + datetime.timedelta(days=j + 1)
        j_time_day = str(j_time)[8:]
        j_time_month_str = str(j_time)[5:7]
        j_time_month = datetime.datetime.strptime(str(int(j_time_month_str)), "%m").strftime("%B")
        keylist_endday[j + 1] = [InlineKeyboardButton(str(int(j_time_day)) + " " + j_time_month, callback_data="n" + j_time_month_str + j_time_day)]
    endday = InlineKeyboardMarkup(keylist_endday)
    return endday

# Purpose
key_purpose = InlineKeyboardMarkup([
    [InlineKeyboardButton("CSC", callback_data="pCSC Event")],
    [InlineKeyboardButton("Arts Council", callback_data="pArts Council Event")],
    [InlineKeyboardButton("House Event", callback_data="hHouse Event: ")],
    [InlineKeyboardButton("IG Activities", callback_data="tIG Activities: ")],
    [InlineKeyboardButton("Student-led Initiative", callback_data="tStudent-led Initiative: ")]
])

key_house = InlineKeyboardMarkup([
    [InlineKeyboardButton("Shan", callback_data="xShan House Event")],
    [InlineKeyboardButton("Ora", callback_data="xOra House Event")],
    [InlineKeyboardButton("Gaja", callback_data="xGaja House Event")],
    [InlineKeyboardButton("Tancho", callback_data="xTancho House Event")],
    [InlineKeyboardButton("Ponya", callback_data="xPonya House Event")]
])
