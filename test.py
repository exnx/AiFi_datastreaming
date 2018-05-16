import time
import random
import aifi

class Test:

    def __init__(self):
        print('Test initialized...')
        self.synched_list = []

    def stream_messages(self):
        '''
        This function creates a list of message objects at different
        intervals (for testing), and sends them to a message handler.
        The message handler will return synchronized messages when
        a condition is met.

        :return: a list of message objects
        '''

        print('Creating messages...')
        N = 10  # number of different sources
        delta = 2.5  # seconds, window of messages to capture
        msg_handler = aifi.Message_handler(delta)  # create a Message_handler
        current_msg = 0

        start_time = time.time()
        max_time = 5

        while(True):
            # create a message at random intervals
            source = random.randint(0, N)  # assign random source
            body = 'this is the body of the message, all the same'
            timestamp = time.time()  # in seconds, float
            message = aifi.Message(timestamp, body, source)  # create a message obj

            print("raw message {} created at time {}".format(current_msg, message.timestamp))
            current_msg += 1

            # read in message
            msg_handler.read_stream(message)

            # if enough time passed, get the synchronized messages
            time_elapsed = time.time() - start_time
            if time_elapsed > max_time:
                synched_msg = msg_handler.get_messages(time.time() - max_time/2, delta)
                print('elapsed time since last output: {}'.format(time_elapsed))
                start_time = time.time()  # reset clock

                # save synched_messages and display
                self.save_synched_messages(synched_msg)
                self.display_synched_messages(synched_msg)

            # sleep sporadic time between .1 and 2 second
            rand_int = random.randint(100, 2000)
            time.sleep(rand_int / 1000)

    def save_synched_messages(self,synched_messages):
        self.synched_list.append(synched_messages)

    def display_synched_messages(self,synched_messages):
        print('Synchronized bundle at ...',synched_messages.timestamp)
        print('size = ', len(synched_messages.delta_messages))
        for index,sync_msg in enumerate(synched_messages.delta_messages):
            print('single sync message {}, at time {}'.format(index,sync_msg.timestamp))


def main():
    test = Test()  # create test
    test.stream_messages()  # create messages

    # # get timestamp of middle message
    # middle = len(messages)//2
    # print('middle index is: ',middle)
    # mid_time = messages[middle].timestamp
    # delta = 5 # second
    #
    # # get messages using a timestamp and delta
    # synched_messages = msg_handler.get_messages(mid_time,delta)
    #
    # print('number of synched messages: ', len(synched_messages.delta_messages))
    #
    # for index,message in enumerate(synched_messages.delta_messages):
    #     print('message {}, message timestamp {}'.format(index, message.timestamp))

if __name__ == "__main__":
    main()