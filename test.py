import time
import random
import aifi

class Stream:
    '''

    This class allows you to create and stream messages (at random intervals)
    and output a synchronized message (grouped together) based on a window of time.

    It uses classes in the aifi.py to process a stream of messages
    and get a synchronized message object.

    '''

    def __init__(self):
        print('Test initialized...')
        self.synched_list = []  # saves the synched messages in a list

    def stream_messages(self):
        '''
        This function creates a stream of messages at different
        intervals (for testing), and sends them to a message handler.
        The message handler will return (by being called) sychronized
        messages when enough time has passed.

        This function will create a message handler object to read and
        save synched messages.  It will then call helper functions
        to save and display the synched messages.

        :return: nothing
        '''

        print('Creating messages...')  # for testing

        # assumed parameters for testing
        N = 10  # number of possible different sources for the messages
        delta = 2.5  # seconds, window of messages to capture

        # variables for when to synchronize messages
        msg_handler = aifi.MessageHandler(delta)  # create a Message_handler
        current_msg = 0  # counter
        start_time = time.time()  # start the timer
        max_time = 5  # criteria for when to get synchronized messages

        # infinite loop to create a stream of messages, and also when to synchronize messages
        while(True):
            # create a message (will be made at random intervals)
            source = random.randint(0, N)  # assign random source
            body = 'This is the body of the message, all the same'
            timestamp = time.time()  # in seconds, float
            message = aifi.Message(timestamp, body, source)  # create a message obj
            current_msg += 1  # update number of messages

            # for debugging
            print("Raw message {} created at time {}".format(current_msg, message.timestamp))

            #  send message to msg_handler
            msg_handler.read_stream(message)

            # if enough time passed, get the synchronized messages
            time_elapsed = time.time() - start_time
            if time_elapsed > max_time:

                # get synched message in a delta time window
                t = time.time() - time_elapsed/2  # time t (the middle point in how much time has passed)
                synched_msg = msg_handler.get_messages(t, delta)
                print('Elapsed time since last output: {}'.format(time_elapsed))
                start_time = time.time()  # reset clock

                # save synched_messages and display
                self.synched_list.append(synched_msg)
                self.display_synched_messages(synched_msg)

            # sleep sporadic time between .1 and 2 seconds (to create a stream of random intervals)
            rand_int = random.randint(100, 2000)
            time.sleep(rand_int / 1000)

    def display_synched_messages(self,synched_messages):
        '''

        This function displays the messages in the synched object

        :param synched_messages: Synched_messages

        '''

        print('Synchronized bundle at time: ',synched_messages.timestamp)
        print('Number of synched message = ', len(synched_messages.delta_messages))
        print('Printing all messages in synched object...')
        for index,sync_msg in enumerate(synched_messages.delta_messages):
            print('Single sync message {}, at time {}'.format(index,sync_msg.timestamp))

def main():
    stream1 = Stream()  # create test
    stream1.stream_messages()  # create and synchronize messages

if __name__ == "__main__":
    main()