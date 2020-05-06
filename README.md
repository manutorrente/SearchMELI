## SearchML v1.2

This script allows you to input items and their prices on a google spreadsheet and check their price regularly. 
It is intended to be run periodically, and if anything is found marching the criteria another spreadsheet will be updated and an email will be sent to you
UpdateML.py is a tool to update the items you already have quicker

# Requisites----------------------------------------------------------------------------------------------------------------------

A google account

Python (it is written in python 3.7)
libraries used:

-gspread

-requests

-smtplib

-time

-json

I think that all these come built in with python except for gspread gspread 

installation: pip install gspread

# Configuration------------------------------------------------------------------------------------------------------------------------

1-Download the repository

2-You´ll need a google service account. It that can be created by following the steps in this link.
https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access

3-Put the .json file you downloaded in the previous step in the same directory you have the scripts and replace %service_account.json% in both python files with the name of the downloaded one.

4-Open the json file and look for the service account's email. It should look something like this: mercadolibrebot@mercadolibrebot-275920.iam.gserviceaccount.com

5-Open the .xlsx that came with the scripts in spreadsheets and share them with the email from the last step. If you don't change the names, you shouldn't have any problems with the calls. 

(Optional)If you don't want to use the email feature, just comment the send_mail() method and its call.

6-Set up the send_email method to receive a notification via email. Replace %from%, %password% and %to% with your personal information from your google account. You can either use a secondary account to send the emails or send them to yourself.

# Use-----------------------------------------------------------------------------------------------------------------------------

1-Fill the ItemsML sheet with the searches you want to make. The item field is the textual search in MercadoLibre, the low_price is the price the script will below, and the floor_price is the lower limit of the search, in case you need one. The forbidden and required are optional. They are meant for words that should or should not appear in the title, and are used to narrow the search parameters to the items intended.

2-Find a way to keep the script running periodically. Daily, hourly, as you wish. I can recommend a free account on pythonanywhere.com that allows you to schedule 1 task daily in the cloud.

3-If the script finds anything, it will appear in PublicacionesML with its link. 

## Hope its useful to you. I'm open to any kind of suggestions and critics.

Thank You

# Updates-------------------------------------------------------------------------------------------------------------------------------

(5/5/20)1.1: Changed variable names and comments for readability
(6/5/29)1.2: Fixed an error with smtplib encoding by changing some strings to f strings
