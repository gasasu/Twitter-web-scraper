"""Visualizing Twitter Topics Across America"""

from data import load_tweets
from datetime import datetime
from geo import us_states, us_state_pop, geo_distance, make_position, longitude, latitude
from maps import draw_state, wait
import random


################################
# Phase 1: Working With Tweets #
################################

#create a tweet dictionary
def make_tweet(text, time, lat, lon):

    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):

    return tweet["text"]


def tweet_time(tweet):

    return tweet["time"]

def tweet_location(tweet):

    def latitude(tweet):
        return tweet["latitude"]
    def longitude(tweet):
        return tweet["longitude"]

    return tweet["latitude"], tweet["longitude"]

def tweet_string(tweet):

    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)


#################################
# Phase 2: The Geometry of Maps #
#################################
def check_intersect(point, segstart, segend):

    px, py = point
    sx, sy = segstart
    ex, ey = segend



    if py >= max(sy,ey) or py <= min(sy,ey):

#check if the point is outside the area enclosed by y = sy and y = ey
        return False

    else:

#check if it's a straight line
        if sx == ex:

            if sx >= px:
                return True
            else:
                return False

        else:

#find the equation of the line, find the point of intersection of the ray and the line
#Iy = py = z * ix + sy - sx*z

            z = (sy - ey)/(sx - ex)
            ix = (py + sx * z - sy)/z
#if the slope is greater than or less than 0

            if z > 0 or z < 0:
                if ix > px:
                    return True

                else:
                    return False
            else:
                return False

def is_in_state(point, state):


    total=0
    for polygon in us_states[state]:
        #which polygon (island) of the state we are in? we should check each polyon
        i = 0
        while i < len(polygon)-1:
            #inside each polygon, see if the ray intersect the sides of the polygon
            if check_intersect(point,polygon[i], polygon[i+1]):
                total += 1
                #add one point if you find it

            i +=1
            #iterate

    if total%2 != 0:
        return True
        #if the number is odd, bingo, the point is in.

    return False
    #the point is not inside


#####################################
# Phase 3: The Tweets of the Nation #
#####################################

def count_tweets_by_state(tweets):

    #create a dictionary containing the count of tweets at the beginning

    names = us_state_pop.keys()
    state_tweets = dict.fromkeys(names, 0)



    for tweet in tweets:
    #now for the tweets you're given, check each tweet
        for state in us_states:
        #for each tweet, run it through all states to find which one it's in

            if is_in_state(tweet_location(tweet), state) == True:
                state_tweets[state] += 1

    for state in state_tweets:

        #now find per capita tweets
        state_tweets[state] = state_tweets[state]/us_state_pop[state]

    most_grossed_state = max(state_tweets.values())
    #find the state with highest per capita


#normalize compared to the highest grossed state
    if most_grossed_state == 0:

        for state in state_tweets:
            state_tweets[state] = 0

        return state_tweets

    else:

        for state in state_tweets:
            state_tweets[state] = state_tweets[state]/most_grossed_state


        return state_tweets

####################
# Phase 4: Queries #
####################

def canada_query(text):

    if "canada" in text.casefold():
        return True
    else:
        return False


def make_searcher(term):

#'text' is the tweet that we check if 'term' is inside

    def advanced(text):
    #go through each consecutive block of the size of 'term'
    #make sure to stop before you go out of the range, b/c you are checking multiple blocks at a time

        for i in range(0 ,len(text)-len(term)+1):
            if text[i:i+len(term)].casefold() == term:
                return True

        return False


    return advanced



def mexico_query(text):

    if "mexico" in text.casefold():
        if "new" not in text.casefold():
            return True
    else:
        return False

#########################
# Map Drawing Functions #
#########################

def draw_state_frequencies(state_frequencies):

    for name, shapes in us_states.items():
        frequency = state_frequencies.get(name, None)
        draw_state(shapes, frequency)

def draw_map_for_query(test, new_file_name=None):
    if new_file_name == None:
        random.seed()
        new_file_name = str(random.randint(0, 1000000000))

    tweets = load_tweets(make_tweet, test, new_file_name)
    tweets_by_state = count_tweets_by_state(tweets)
    draw_state_frequencies(tweets_by_state)
    wait()



#################################
# Phase 5: Use what you've done #
#################################

def trump(text):

    if "trump" in text.casefold():
        if "donald" not in text.casefold():
            return True
    else:
        return False

#i want to see in full bloom, that's it.
