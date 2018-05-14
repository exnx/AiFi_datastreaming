import time
import random
import aifi

class Test:

    def __init__(self):
        print('Test initialized...')

    def create_messages(self):
        print('Creating messages...')
        messages = []  # declare a stream of messages for testing
        max_messages = random.randint(8, 14)  # create random number of messages
        msg_counter = 0  # current message number
        N = 10  # number of different sources

        while (msg_counter < max_messages):
            # create a message at random intervals
            source = random.randint(0, N)
            body = 'this is the body of the message, all the same'
            timestamp = time.time()  # in seconds, float
            # create a single message
            message = aifi.Message(timestamp, body, source)
            messages.append(message)  # append to list
            msg_counter += 1  # increment message counter
            print('message {} created at time {} from source {}'.format(msg_counter, message.timestamp,message.source))
            # sleep sporadic time between .1 and 2 second
            rand_int = random.randint(100, 2000)
            time.sleep(rand_int / 1000)
        return messages

def main():
    test_obj = Test()  # create test
    msg_handler = aifi.Message_handler()  # create a Message_handler
    messages = test_obj.create_messages()  # create messages

    # feed in messages to handler
    for message in messages:
        msg_handler.read_message(message)

    # get timestamp of middle message
    middle = len(messages)//2
    print('middle index is: ',middle)
    mid_time = messages[middle].timestamp
    delta = 5 # second

    # get messages using a timestamp and delta
    synched_messages = msg_handler.get_messages(mid_time,delta)

    print('number of synched messages: ', len(synched_messages.delta_messages))

    for index,message in enumerate(synched_messages.delta_messages):
        print('message {}, message timestamp {}'.format(index, message.timestamp))

if __name__ == "__main__":
    main()