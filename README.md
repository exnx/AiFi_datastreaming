# AiFi_datastreaming

The streamer.py file creates a stream of messages, and uses a MessageHandler object from the handler.py
file to synchronize messages.  The MessageHandler will return a synchronized message at certain time
intervals (after 5 seconds or more), or None before then.