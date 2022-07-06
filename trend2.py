"""Visualizing Twitter Topics Across America"""

from data import load_tweets
from datetime import datetime
from geo import us_states, us_state_pop, geo_distance, make_position, longitude, latitude
from maps import draw_state, wait
import random


################################
# Phase 1: Working With Tweets #
################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    return tweet["text"]


def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    return tweet["time"]

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    def latitude(tweet):
        return tweet["latitude"]
    def longitude(tweet):
        return tweet["longitude"]

    return tweet["latitude"], tweet["longitude"]

def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point) #is format a feature of the string


#################################
# Phase 2: The Geometry of Maps #
#################################


def check_intersect(point, segstart, segend):


    px, py = point
    ax, ay = segstart
    bx, by = segend


    if py >= max(ay,by) and py <= min(ay,by):
        return False

    else:
    # Now all things are within the range of the ling segment, vertically
        if ax == bx:
            if px>ax:
                return False
            else:
                return True
        else:
        # line is not vertical, i.e., it has a defined slope, meaning ax-bx is not 0, we can find the slope of the line segement,

            m =(ay-by)/(ax-bx)

            if ay-by == 0:
                if py == ay and py == by:

            else:
                int = (py - by + m*bx)/m
                if int>px:
                    return False
                else:
                    return True

        # line segemnt has the function y=kx+b. plug in px=x to find the point of intersection
        # check is point of intersection is to the left of the point or not.

    """if py <= max(ay,by) and py >= min(ay,by):
        print((bx - ax)*(py - ay) - (by - ay)*(px - ax))
        # you dont want to print this
        if (bx - ax)*(py - ay) - (by - ay)*(px - ax) <= 0 :
            #taking cross products of segstart-point and segend-point
            #if the 2D determinant is greater than zero (counter clock wise) the point is on the left

            print("hi")
            return True

        else:
            print("bye")
            return False


    return False"""



def is_in_state(point, state):


    total=0
    for polygon in us_states[state]:
        i = 0
        while i < len(polygon)-1:
            if check_intersect(point,polygon[i], polygon[i+1]):
                total += 1

            i +=1

    if total%2 != 0:
        return True

    return False





#####################################
# Phase 3: The Tweets of the Nation #
#####################################

def count_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their state of origin.

    The keys of the returned dictionary are state names, and the values are
    normalized per capita tweet frequencies. You may use the dictionary
    us_state_pop, which associates state abbreviation keys with 2013 estimated
    population for the given state.

    tweets -- a sequence of tweet abstract data types
    """
    names = us_state_pop.keys()
    #state_tweets = dict.fromkeys(names)
    #state_tweets = dict.fromkeys(state_tweets, 0)
    state_tweets = dict.fromkeys(names, 0)

    for tweet in tweets:
        #point = (tweet["longitude"], tweet["latitude"])
        for state in us_states:

            if is_in_state(tweet_location(tweet), state) == True:

                state_tweets[state] += 1

    for state in state_tweets:

        state_tweets[state] = state_tweets[state]/us_state_pop[state]

    most_grossed_state = max(state_tweets.values())

    for state in state_tweets:
        state_tweets[state] = state_tweets[state]/most_grossed_state


    return state_tweets



####################
# Phase 4: Queries #
####################

def canada_query(text):
    """Return True if text contains "canada" as a substring.
    Results should not be case-sensitive.  When text includes "CAnada",
    for example, should return True.
    """
    if "canada" in text.casefold():
        return True
    else:
        return False





def make_searcher(term):
    """Returns a test that searches for term as a substring of a given string.
    Results should not be case-sensitive.
    For example, makesearcher("canada") should behave identically to canada_query.
    """

    def advanced(text):
        for i in range(0 ,len(text)-len(term)+1):
            if text[i:i+len(term)].casefold() == term:
                return True

        return False


    return advanced



def mexico_query(text):
    """Returns true if "mexico" is included as a substring and "new" is not.
    Again, results should not be case-sensitive.
    """
    #your code here


#########################
# Map Drawing Functions #
#########################

def draw_state_frequencies(state_frequencies):
    """Draw all U.S. states in colors corresponding to their frequency value."""
    for name, shapes in us_states.items():
        frequency = state_frequencies.get(name, None)
        draw_state(shapes, frequency)

def draw_map_for_query(test, new_file_name=None):
    if new_file_name == None:
        random.seed()
        new_file_name = str(random.randint(0, 1000000000))
    """Draw the frequency map corresponding to the tweets that pass the test.
    """
    tweets = load_tweets(make_tweet, test, new_file_name)
    tweets_by_state = count_tweets_by_state(tweets)
    draw_state_frequencies(tweets_by_state)
    wait()

draw_map_for_query(canada_query)

#################################
# Phase 5: Use what you've done #
#################################

# Uncomment (and edit) the line below to create a map based on a query of your choice
#draw_map_for_query(canada_query)
