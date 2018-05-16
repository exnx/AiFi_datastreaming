import time

'''
Description

This file will handle the stream of messages from the streamer.py file.  
This file contains the Message and SynchedMessages classes, as well as a Message_Handler.

'''

class Message:
    """
    A class containing a message body, timestamp, source

    """
    def __init__(self, timestamp, body, source):
        """
        :param timestamp: a float
        :param body: a string
        :param source: an int
        """
        self.timestamp = timestamp
        self.body = body
        self.source = source

class SynchedMessages:

    """
    A class that has synchronized messages within a given time window
    between timestamp-delta and timestamp+delta.  This class will be used
    by the get_messages function in the Message_handler class.  I created this
    class to match the output in the written challenge.

    """
    def __init__(self,timestamp, delta_messages):
        """
        :param timestamp: float
        :param delta_messages: list of messages
        """
        self.timestamp = timestamp
        self.delta_messages = delta_messages  # list of message in window delta


class MessageHandler:
    """
    A class that handles messages by reading and synchronizes (groups) messages based
    on a time window (timestamp-delta to timestamp+delta) and outputs a
    SynchedMessages object
    """
    def __init__(self, delta):
        """
        This constructor declares a raw list of bundled messages, ie,
        can be from multiple sources or in any window
        """
        self.raw_messages = []  # track all raw messages read
        # self.msg_counter = 0  # current message number
        # self.max_messages = 5  # max number of messages before sync
        self.delta = delta
        self.is_timer_on = False
        self.start_time = 0  # timer declared
        self.max_time = 5  # secs, criteria for when to send synchronized messages back

    def read_stream(self, message):
        """
        reads a message and appends to list

        :param message: Message object
        """

        self.raw_messages.append(message)  # append messages to list

        # if timer is off, start the timer
        if not self.is_timer_on:
            self.is_timer_on = True
            self.start_time = time.time()  # start the timer

        # if enough time passed, send the synchronized messages, if not, return None
        time_elapsed = time.time() - self.start_time

        if time_elapsed > self.max_time:
            # get synched message in a delta time window
            t = time.time() - time_elapsed / 2  # time t (the middle point in how much time has passed)
            synched_msg = self.get_messages(t, self.delta)
            print('\n')
            print('Elapsed time since last synched_message output: {}'.format(time_elapsed))
            start_time = time.time()  # reset clock
            self.is_timer_on = False  # turn off timer
            return synched_msg
        else:
            return None


    def get_messages(self, timestamp, delta):
        """
        This function iterates through all the raw grouped messages and returns
        a SynchedMessages object that meets the criteria, which are if the
        message timestamp is in the desired window (timestamp-delta, timestamp+delta),
        and that only one message from each of the N sources is included.

        :param timestamp: float
        :param delta: float
        :return: Synched_messages
        """
        used_sources = []  # track which sources used
        delta_messages = []  # list of all valid messages in delta window

        # loop through all the bundled messages
        for message in self.raw_messages:
            if message.source not in used_sources:  # check unused source
                used_sources.append(message.source)  # add source to used list
                # check if timestamp in delta window
                if message.timestamp < timestamp + delta and \
                    message.timestamp > timestamp - delta:
                    delta_messages.append(message)  # add message to list
        # create a synched_message object, return it
        self.raw_messages = []
        return SynchedMessages(timestamp, delta_messages)