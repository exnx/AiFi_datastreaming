# AiFi_datastreaming

To test this solution, run the streamer.py file.

The streamer.py file creates a stream of messages, and uses a MessageHandler object from the handler.py
file to synchronize messages.  The MessageHandler will return a SynchedMessages at certain time
intervals (after 5 seconds or more), or if a maximum number of messages have been streamed.  Otherwise
it will return None.  To accommodate a message streaming rate, the key parameters to adjust are
the time interval and max number of messages before returning a SynchedMessages.


Analysis of solution:

Questions:  "What are the caveats of your particular implementation? Assuming an incoming message rate,
what is the worse case and best case scenario for your implementation?"

Answer:  for testing, I assumed a random incoming message rate between 0.2 to 2 secs.

The best case scenario for my solution is that the sources of the messages are all random and have a large range
of possible sources.  If they're random, then most of the messages streamed will be included in the SynchedMessages.

A worse case scenario is that if most of the messages are from one source, then
many of the messages will not be included in the SynchedMessages.  In this case, changing the assumed
parameters would help alleviate this by changing the max amount of time to allow before sending a
SynchedMessages back, ie, send a SynchedMessages more often.