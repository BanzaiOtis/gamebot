import os
import time
from slackclient import SlackClient

from links import links # contains links to pictures

# gamebot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    # default response if command is not recognized by logic
    # in main behavior block
    default_response = "What the hell are you talking about? :hear_no_evil:"

    ### Main behavior block ###
    if 'morgan so clueless' in command:
        response = "Because he's dumb. :eggplant:"
    elif command.startswith('set_status'):
        status = command.split('set_status')[1].strip()
        with open('./current_status.txt', 'w') as f:
            f.write(status)
        response = "Done!"
    elif command.startswith('get_status'):
        with open('./current_status.txt', 'r') as f:
            response = f.readlines()[0]
    elif command.startswith('show'):
        try:
            item = command.split(' ')[-1]
        except IndexError:
            break
        response = links[item]
    else:
        # Default response
        response = default_response
    
    #adding a comment here to test how this works

    ### End main behavior block ###

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    max_inactive_time = 29 * 60 # 29 minutes in seconds
    last_call_time = time.time()

    if slack_client.rtm_connect():
        # Bot notifies #bot_testing channel when it is redeployed.
        slack_client.api_call("chat.postMessage", channel='C7412E935',
                              text="Redeployed: I'm awake!", as_user=True)
        # creates fresh game status file if it doesn't exists
        # which it shouldn't because storage is ephemeral and disappears
        # when the app shuts down.
        with open('./current_status.txt', 'w') as f:
            pass
        # Creates new
        print("gamebot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
                last_call_time = time.time()

            # Setting up a timer to ping Slack with a frivolous call if
            # command hasn't been a meaningful call within the given
            # inactive time. This should keep the Heroku dyno awake.
            current_time = time.time()
            if (current_time - last_call_time) > max_inactive_time:
                junk_call = slack_client.api_call("users.list")
                last_call_time = current_time

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
