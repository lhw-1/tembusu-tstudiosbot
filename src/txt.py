import tstudios_contacts as tcontacts

# Texts
space = "\n"
dspace = "\n\n"
start1 = "Welcome to tStudiosBot! This bot will help you to loan equipment from tStudios.\n\n"
start2 = "To view the list of contacts for tStudios' AY21/22 EXCO: /contacts\n\n"
start3 = "To apply for an equipment loan from tStudios: /loan\n\n"
start4 = "To check the current status of your equipment loan: /check\n\n"
start5 = "To wake the bot up: /boop\n\n"
query = "For further queries regarding the bot or its usage, please contact @leehws. Thank you!"
start = start1 + start2 + start3 + start4 + start5 + query
wip = "This feature is still a work in progress." + space + "Please directly message the development team at @leehws or tStudios EXCO members. Thank you!"
loan_txt = "Please note that all loan requests must be made at least 1 week in advance, and for a maximum of 3 consecutive days. The loan request can only be made within the 2 weeks window starting from one week after today. For additional queries, please contact " + tcontacts.head_handle + ".\n\n"
request_process = "We are currently processing your request. In the meantime, you can use the command /check to check the current progress on your loan request.\n\n" + query
