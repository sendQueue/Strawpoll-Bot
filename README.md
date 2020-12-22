# Strawpoll-Bot
A simple working (Nov. 2020) Strawpoll-Bot for .de and .me version

runtime parameters are <br />
id, poll-option, thread-delay, max-threads, thread-timeout(, multiple) <br />
for e.g.: <br />
fe8sa1y 1 -d 0.02 -mt 400 -to 10 (-m True) <br />
<br />
multiple is only for the .me version -> some polls support multiple answers which changes the post request, use -m True if so.
<br />
(see https://vinii.de/github/strawpoll/parameters.png).

<br />
If you are running windows you might need to change the proxies.txt path inside of the script: <br />
Change proxies.txt to a valid windows path with double \\ for e.g. C:\\Users\\myUsername\\Desktop\\Strawpoll-Bot\\de\\vinii\\proxies.txt 

## .de example:
- https://strawpoll.de/fe8sa1y (20k botted votes)
- https://vinii.de/github/strawpoll/botting.png
- https://vinii.de/github/strawpoll/console_log.png
