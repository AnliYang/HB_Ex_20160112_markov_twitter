import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return " ".join(words)

def make_tweet(chains):
    """Takes dictionary of markov chains; returns tweet-ready random text
    less than 140 characters."""

    pass
    

def tweet(long_text):
    """Using previously generated markov string, truncate and post to account."""
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure they're correct
    # print api.VerifyCredentials()

    # truncate chains (text version, not dictionary) to be <= 140 char.
    # maybe add: cut off after FULL word (white space before chars 140), 
    # CONSIDER RFIND-ING PUNCTUATION INSTEAD OF LAST WHITESPACE
    # CONSIDER USING THE END OF THE LONG TEXT AS ANCHOR INSTEAD OF BEGINNING.
    initial_short_text = long_text[:138]
    index_last_whitespace = initial_short_text.rfind(" ")
    middle_short_text = initial_short_text[:index_last_whitespace]
    
    # enter into tweet body (as a variable)
    final_short_text = middle_short_text[0].upper() + middle_short_text[1:]

    # print final_short_text

    # Send a tweet
    status = api.PostUpdate(final_short_text)
    print status.text

if __name__ == "__main__":

# def tweet_markovs():
    """
       Repeat markov string generation and tweet until user presses 'q' to quit.
    """

    filenames = sys.argv[1:]
    text = open_and_read_file(filenames)
    chains = make_chains(text)
    user_input = None

    while True:
        if user_input == 'q':
            break
        else:
            # Generates random string
            random_text = make_text(chains)
        
            tweet(random_text)

            user_input = raw_input("Enter to tweet again [q to quit] > ")
    

# tweet_markovs()



# # Get the filenames from the user through a command line prompt, ex:
# # python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

# # Open the files and turn them into one long string
# text = open_and_read_file(filenames)

# # Get a Markov chain
# chains = make_chains(text)

# # Your task is to write a new function tweet, that will take chains as input
# # tweet(chains)

# long_text = make_text(chains)

# tweet(long_text)




