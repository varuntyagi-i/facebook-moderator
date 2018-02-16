from api_key import *
from classifier import *
import requests
from termcolor import colored

base_url = "https://graph.facebook.com/v2.11/"


# this function is use to fetch all the recent post that user posted and will
# return the photo_id of the post that user select for moderation.
def return_photo_id():
    # get url1 to fetch recent post of user
    url1 = base_url + "me?fields=posts&access_token=" + access_token
    url2 = base_url + "me?fields=posts{link}&access_token=" + access_token
    
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    #   convert get data to json form so that we can easily manipulate it
    me = response1.json()
    post_link = response2.json()
    count = 1

    #   loop to print all the recent post of user
    for ele in me['posts']['data']:
        print colored(count, 'blue'),
        #   Created on
        print "     \nDate: %s" % (ele['created_time']),
        #   ID of post
        print "     ID: %s" % (ele['id'])
        #   Link of post
        print "     Link: ",
        if 'link' in post_link['posts']['data'][count-1]:
            print post_link['posts']['data'][count-1]['link']
            print
        count += 1

    while True:
        index = int(raw_input("\nEnter which post you want to fresh: "))
        if 0 < index <= count:
            break
        else:
            print colored("\nChoose from above given options",'red')

    while True:
        #   use above index to fetch that particular post that user wants to moderate
        print "Are you sure you want to refresh post: \nCreated on: %s \nPhoto id: %s "\
            % (me['posts']['data'][index-1]['created_time'], me['posts']['data'][index-1]['id'])
        print "Link: ",
        print post_link['posts']['data'][index-1]['link']
        temp = raw_input("Enter your choice(yes/no): ").upper()

        #   if user enter yes it will return the photo_id.
        if temp == "YES":
            return me['posts']['data'][index-1]['id']
            break
        elif temp == "NO":
            index = int(raw_input("\nEnter which post you want to fresh: "))
        else:
            print colored("\nEnter correct choice:", 'red')
            index = int(raw_input("\nEnter which post you want to fresh: "))


#   this function will take photo id as an argument and fetch all the comment that user has on his/her post
def fetch_comment(photo_id):
    #   get url1
    url1 = base_url + photo_id+"?fields=comments.order(reverse_chronological)&access_token=" + access_token
    response = requests.get(url1)
    #   change the data to json format
    me = response.json()
    #   check whether there is any comment on post or not
    if 'comments' in me:
        print colored("\nComments are: ", 'cyan')
        #   fetching comments from post
        for ele in me['comments']['data']:
            print
            print colored(ele['message'], 'green')
            #   we use classify_comment function to classify our comment whether it is negative or positive
            result = classify_comment(ele['message'])
            #   if result is negative it will delete the comment
            if result == 'negative':
                print colored("negative comment", 'blue'),
                choice = raw_input(colored("Are you sure to delete this comment(Y/N): ", 'yellow')).upper()
                if choice == 'Y':
                    delete_url = base_url + ele['id']+"?method=delete&access_token=" + access_token
                    requests.delete(delete_url)
                elif choice == 'N':
                    print
                    #   print "negative comment"
                    #   print ele['id']
            #   if result is positive it will print positive comment
            else:
                print colored("positive comment", 'blue'),
                print colored("Continue", 'yellow')

    else:
        print colored("\nThere is no comment on this post: ",'red')

    #   while loop to ask user whether he/she wants to continue or not
    while True:
        temp = raw_input("\nIf you want to refresh another post enter Y else N: ").upper()
        if temp == 'Y':
            photo_id = return_photo_id()
            fetch_comment(photo_id)
        elif temp == 'N':
            break


photoId = return_photo_id()
fetch_comment(photoId)
