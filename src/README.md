# README for Collaborators

## Set-up

This bot is written in python, utilising the python-telegram-bot library.

To run this program locally on your device, make sure the following libraries are installed (using pip or otherwise):

- oauth2client
- gspread
- telegram
- python-telegram-bot

For installing python libraries on your system / CLI of choice, refer to online guides.

## Feature #0: Basic Commands

All commands under Feature #0 are available to ALL users, including the public.

- /start: Starts the bot for the user, and displays all available commands. The list of commands displayed is configurable under txt.py.

- /contacts: Displays the contact details for tStudios EXCO / administrators. The list of contacts displayed is configurable under tstudios_contacts.py.

- /boop: Boop.

## Feature #1: Equipment Loaning (User-end)

All commands under Feature #1 are only available to approved users and administrators.

- /loan: This starts the conversation handler that chains the loan functions together. Using two google spreadsheets as reference. (One for list of administrators / approved users, and one for loan request records) The relevant google spreadsheets will be available to you depending on your level of access. Please let the lead developer know if you need access to any particular spreadsheet.

- /check: This simply displays all the loan requests that the user has ever made. For users who are very active in and passionate about borrowing equipment from tStudios, the command might be slightly slower.

## Feature #2: Equipment Loaning (Admin-end)

All commands under Feature #2 are only available to administrators.

- /approve: This allows the administrator to approve any outstanding loan requests.

- /return: This allows the administrator to indicate a loan request as having been returned. Please note that this should be used AFTER the administrator has verified that the equipment has been returned - this is to ensure that the availability for each item on the list is correctly displayed.

- /add: This allows tha administrator to approve a user to be able to use the equipment loaning features.

## Possible Extensions

There are two main features currently being considered for the future, but for now, the application is complete. As a collaborator, feel free to continue developing more extensions for the bot... as long as you don't break the bot!

1. User guide

The user guide would help people to choose the item that is most suitable for them. However, this is not currently considered necessary, since it is assumed that approved users who are able to borrow equipment already know what they need to borrow. If not, they can redirect their questions to tStudios head.

2. Item Picture Display

Being able to display pictures of the equipment would be very nice. For the same reason as (1), it is currently not considered as necessary.
