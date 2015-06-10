# Twitter-stream-gatherer
Streams a list of hashtags, saves it as txt in JSON format. 
Savefile names change based on the date, machinename and max filesize specified.

To Install:
* Have a working Python 2.7 installation.
* Install latest Tweepy library with your favorite package manager. eg on windows: python27\python\scripts\easy_install tweepy
* Copy this repository to your system (git clone git://github.com/JeffX89/Twitter-stream-gatherer or just copy it manually)
* Change the configuration file:
    - Enter your 4 api keys: https://apps.twitter.com -> Keys and Access Tokens
    - Enter a machine name, this will be included in the filename.
    - Enter a save path, curently saves to (location of script)/data
    - Enter the max filesize in MB. This way you wont accidentally have huge files. If you do not want to use this, set it to a very high value.
    - Enter the hashtags you wish to follow

Make sure you set write permission on the save path.
You should now be ready to run the script.
