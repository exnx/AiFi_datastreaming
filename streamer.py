import time
import random
import handler

'''
Description:

This file contains the Stream class to create a stream of messages, and accept synchronized messages
from the MessageHandler in streamer.py file.

'''

class Stream:
    '''

    This class allows you to create and stream messages (at random intervals)
    and output a synchronized message (grouped together) based on a window of time.

    It uses classes a MessageHandler from the handler.py file to read the stream of messages,
    which will return a synchronized message object (at spaced time intervals).

    '''

    def __init__(self):
        print('Test initialized...')
        self.synched_list = []  # saves the synched messages in a list

    def stream_messages(self):
        '''
        This function creates a stream of messages at different
        intervals (for testing), and sends them to a message handler.
        The message handler will return (by being called) sychronized
        messages when enough time has passed, or if the max number of
        messages have been streamed.

        This function will create a message handler object to read and
        save synched messages.  It will then call helper functions
        to save and display the synched messages.

        :return: nothing
        '''

        print('Creating stream of messages...')  # for testing

        # Assumed parameters for testing
        N = 10  # number of possible different sources for the messages
        time_interval = 5  # secs, criteria for when to send synchronized messages back
        delta = time_interval/2  # seconds, window of messages to capture
        max_messages = 6  #  also limit number of messages streamed before getting a syched message back

        # variables for when to synchronize messages
        msg_handler = handler.MessageHandler(delta, time_interval, max_messages)  # create a Message_handler
        current_msg = 0  # counter

        # infinite loop to create a stream of messages, and also when to synchronize messages
        while(True):
            # create a message (will be made at random intervals)
            source = random.randint(0, N)  # assign random source
            body = 'This is the body of the message, all the same'
            timestamp = time.time()  # in seconds, float
            message = handler.Message(timestamp, body, source)  # create a message obj
            current_msg += 1  # update number of messages

            # for visualization
            print("Raw message {} created at time {}".format(current_msg, message.timestamp))

            #  send message to msg_handler
            sync_msg = msg_handler.read_stream(message)

            # if response returned, save and display
            if sync_msg:
                self.synched_list.append(sync_msg)
                self.display_synched_messages(sync_msg)

            # sleep sporadic time between .1 and 2 seconds (to create a stream of random intervals as inputs)
            rand_int = random.randint(100, 2000)
            time.sleep(rand_int / 1000)

    def display_synched_messages(self,synched_messages):
        '''

        This function displays the messages in the synched object

        :param synched_messages: Synched_messages

        '''

        print('Synchronized bundle at time: ',synched_messages.timestamp)
        print('Number of messages in synched object = ', len(synched_messages.delta_messages))
        print('Printing all messages in synched object...')
        for index,sync_msg in enumerate(synched_messages.delta_messages):
            print('Single sync message {}, at time {}'.format(index,sync_msg.timestamp))
        print('\n')

def main():
    stream1 = Stream()  # create Stream object
    stream1.stream_messages()  # create and synchronize messages

if __name__ == "__main__":
    main()