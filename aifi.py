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

class Synched_messages:

    """
    A class that has synchronized messages within a given time window
    between timestamp-delta and timestamp+delta.  This class will be used
    by the get_messages function in the Message_handler class.  I created this
    class to match the output in the written challenge.

    """
    def __init__(self,timestamp,delta_messages):
        """
        :param timestamp: float
        :param delta_messages: list of messages
        """
        self.timestamp = timestamp
        self.delta_messages = delta_messages

class Message_handler:
    """
    A class that handles messages by reading and synchronizes (groups) messages based
    on a time window (timestamp-delta to timestamp+delta) and outputs a
    Synched_messages object
    """
    def __init__(self):
        """
        This constructor declares a raw list of bundled messages, ie,
        can be from multiple sources or in any window
        """
        self.raw_messages = []

    def read_message(self,message):
        """
        reads a message and appends to list

        :param message: Message (type)
        """
        self.raw_messages.append(message)

    # output messages within time frame
    def get_messages(self,timestamp,delta):
        """
        This function iterates through all the raw grouped messages and returns
        a Synched_messages object that meet the criteria, which are if the
        message timestamp is in the desired window (timestamp-delta, timestamp+delta),
        and that only one message from each source is included.

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
        return Synched_messages(timestamp,delta_messages)