# Solace
## What Is Solace?
Solace is a Discord bot that that acts as an education management tool used by both students and teachers. With the 
increasing popularity of Discord, Solace provides a way to integrate practical features in an easy-to-use and accessible way.

## Invite Link
To invite Solace to your own server:
https://discord.com/api/oauth2/authorize?client_id=1038482009540010098&permissions=8&scope=bot 

## Installation
To run the Solace on your local machine with your own bot token* , you must first install the following libraries by running these commands:\
```pip install discord.py```
```pip install twilio```
```pip install neuralintents```
NOTE: M1/M2 Mac users may run into issues with dependency conflicts. Follow the suggestions given in the error message 
to resolve this issue.
*Replace ```[TOKEN]``` in ```main.py``` with your own token.

## Commands
Set-Up (before usage):\
```!restart```: ADMIN CMD. Restart the bot before first use, or if bugs are encountered.\
```!set_announce <channel>```: ADMIN CMD. Sets the announcement channel.\
```!set_chat <channel>```: ADMIN CMD. Sets the chat with Solace channel.\
```!set_threads <channel>```: ADMIN CMD. Sets the threads post channel.\
```!set_mail <channel>```: ADMIN CMD. Sets the instructor mail channel.

Sending an SMS Announcement:\
```!announce <level> <message>```: ADMIN CMD. Send a text to the Announcement channel and/or registered phone numbers based on level (1, 2, 3). Message must be surrounded by "".\
```!text_list```: ADMIN CMD. Displays all registered users and numbers\
```!send_pm <user> <message>```: ADMIN CMD. Send a private text to a registered user. Message must be surrounded by "".
```!add_number <number>```: Add your phone number to the registered number list. Example: +10009998888
```!remove_number```: Removes your phone number from the registered number list.

Adding and Removing Breakout Rooms (Channels):\
```!new_text_channels <name> <num>```: ADMIN CMD. Create num number of text channels named name.\
```!new_voice_channels <name> <num>```: ADMIN CMD. Create num number of voice channels named name.\
```!delete_channels <name>```: ADMIN CMD. Delete all channels named <name>.

Discussion Posts:\
```!reply_threads <thread_id>```: Adds your reply to the chain of messages in the thread.\
```!view_thread <thread_id>```: Displays the thread given by <thread_id>\
```!new_thread```: Triggers the creation of a new discussion thread through message input and prompts.

General:\
```!enter_course_info```: Triggers the updating of course information embed with message input and prompts.\
```!command_list```: Produce this list of all solace-bot commands.


## Credits
https://youtube.com/playlist?list=PLJXEdhN0Tc3LRT716enS1LcY4OF8vg1VA 


