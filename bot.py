from instagrapi import Client #allows access to interact with instagram
import csv #allows access to read and write csv files
import random #allows random number generations
import math #allows complex math operations such as square root
import time #allows thread to wait

filename_to_export = "users.csv"

login_username = "sunrisesophiamarch"
login_password = "6173350376-Lev"

client = Client()
client.login(login_username, login_password)
print("logged in")

def get_user_rank(user_id):
    follower_followers = client.user_followers(user_id, 0)
    follower_followers_amount = len(follower_followers)
    print()

    follower_following = client.user_following(user_id, 0)
    follower_following_amount = len(follower_following)

    follower_medias = client.user_medias(user_id, 0)
    follower_medias_amount = len(follower_medias)

    print(f"followers = {follower_followers_amount}, following = {follower_following_amount}, medias = {follower_medias_amount}")
    return (follower_following_amount*follower_medias_amount)/(follower_followers_amount+1)

def write_users(users, write_to): #writes users into csv with their user_id, username, engagements, and rank
    with open(write_to, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        fields = ['user id', 'username', 'engagements', 'rank']
        csvwriter.writerow(fields)

        i = 0
        for user_id in users:
            
            print()
            
            user_username = client.username_from_user_id(user_id)
        
            rank = get_user_rank(user_id)

            new_row = [user_id, user_username, 1, rank]
            csvwriter.writerow(new_row)
            
            csvfile.flush()
            print(f"exported user {i + 1}")
            print(f"{user_id} - {user_username}")

            i += 1

        print()
        print(f"exported {i + 1} users.")
            

def export_followers(username_of_scraped, count : int, filename): #export all followers of a user with their user_id, username, engagements, and rank
    
    def get_followers(username, how_many : int): #returns dict of users following a user given username and amount
        print(f"getting {how_many} followers for account with username {username}")
        user_id = client.user_id_from_username(username)
        return client.user_followers(user_id, amount=how_many)

    print()
    followers = get_followers(username_of_scraped, count)
    print(f"done getting followers - {len(followers)}")
    write_users(followers, filename)
    print()
    print(f"exported {len(followers)} followers' data to {filename}")
    
def engage_with_user(user_to_engage_id):

    user_medias = client.user_medias(user_to_engage_id, 0)
    user_medias_amount = len(user_medias)

    user_medias_to_interact_amount = math.isqrt(user_medias_amount) #how many medias to interact with, square root of posts of user (like>comment)
    user_medias_to_interact = random.sample(user_medias, user_medias_to_interact_amount) #choose that many medias to interact with
    
    user_medias_to_comment_amount = user_medias_to_interact_amount // 2 #how many medias to comment on
    user_medias_to_comment = random.sample(user_medias_to_interact, user_medias_to_comment_amount)#chose medias to comment on from liked medias

    for user_media_to_interact in user_medias_to_interact: #like chosen medias
        client.media_like(user_media_to_interact.id) #like media
        print(f"liked media {user_media_to_interact.id}")
        
        if user_media_to_interact in user_medias_to_comment: #if current media is also supposed to be commented on
            def comment_on_media(media_id):
                with open("comments.txt", "r") as comments_file_list:
                    comments = comments_file_list.read().splitlines()
                    comment = comments[random.randint(0, len(comments) - 1)]
        
                    client.media_comment(media_id, comment)
                    return comment
            
            print(f"commented {comment_on_media(user_media_to_interact.id)} on media {user_media_to_interact.id}")
            
            
        print("pausing")
        time.sleep(random.randint(2, 5)) # to not get banned
        print("done pausing, next media")
                
    client.user_follow(user_to_engage_id)

def engage_with_users(users_filepath, users_to_engage_with):
    with open(users_filepath, "r") as users_document:
        print("openeing file with users")
        users_data_list = users_document.read().splitlines()
        user_rank_to_user_list = []
        
        i = 1
        while(i < len(users_data_list)): #create list with just rank and user id
            user_data_list = users_data_list[i].split(',')
            i += 1

            user = user_data_list[0]
            user_rank = float(user_data_list[3])
            user_rank_to_user_list.append((user_rank, user))

        user_rank_to_user_list.sort() #sort list using rank, lowest rank will come first
        num_of_users = len(user_rank_to_user_list)
        i = num_of_users - 1
        while(user_rank_to_user_list[i][0] > 0 and (num_of_users - i) < users_to_engage_with):
            print()
            print(f"engaging with user {user_rank_to_user_list[i][1]} with rank {user_rank_to_user_list[i][0]}")
            engage_with_user(user_rank_to_user_list[i][1])
            i += -1
            time.sleep(random.randint(i, min(2*i, 60))) # to not get banned

export_followers("melimtx", 50, filename_to_export) #write followers and their data to csv file
print()
print("run engagement with top followers? enter amount of followers to engage with")
amount_of_followers_to_engage_with = int(input())
print(f"engaging with a maximum of {amount_of_followers_to_engage_with} users.")
engage_with_users(filename_to_export, amount_of_followers_to_engage_with)

#engage_with_user(client.user_id_from_username("sunrisesophiamarch"))