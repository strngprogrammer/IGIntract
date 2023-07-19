import requests , uuid , time , threading , random , string

from lib.colors import *
from lib.logo import print_logo,clear,enter_to_exit
from lib.login import *
from lib.funcs import *
class WatchLikeStories():

    def __init__(self) -> None:
        
        self.sessions = []
        self.main_session = ''
        self.done = 0
        self.error = 0
        self.nostories = 0
        self.users = []
        self.like = False

        self.all_users = []

    def get_target(self):

        session = random.choice(self.sessions)

        res = get_target_id(session,self.target_user)

        if res == "false":

            print( darkred + f"[ X ] Target not found or session not working trying again ...")

            self.get_target()

        else:
            print(lightgreen+f"[ + ] Grabbed {self.target_user} info.")
            self.target_id = res

        


    def get_info(self,sessions):

        self.sessions = sessions
        
        clear()

        print_logo()

        print(lightred + "- watching and liking stories")
        print(lightcyan + "- to use this mode you need to : ")
        print(lightyellow + "1 - use multiple sessions to fetch users")
        print(lightyellow + "2 - use a single account to watch and like stories")
        print(lightyellow + "3 - use a good sleep to make sure that your account will work safe like ( 40 - 60 )")
        print(lightblue + "Good Luck !!")

        mods = f"""
{darkmegenta}- there is three mods please select one :
{darkyellow}[ 1 ] target followers
{darkyellow}[ 2 ] target followings
{darkyellow}[ 3 ] your followings
        """
        print(mods)

        mod = int(input("select mode -> "))

        if mod == 1 or mod == 2:

            self.target_user = str(input("[ + ] Enter Target : "))

            print( lightblue + "[ / ] Getting target info please wait ...")

            time.sleep(1)

            self.get_target()

            time.sleep(1)

        else:
            pass

        
        text = f"""
{lightblue}- enter your main account that you want it to watch and like :
{darkblue}[ 1 ] Login
{darkblue}[ 2 ] Use Session 
        """
        print(text)
        inp = int(input(darkyellow + "select -> "))

        if inp == 1:
            username = str(input(lightcyan+"[ + ] Username : "))
            password = str(input(lightcyan+"[ + ] Password : "))
            res = login_single_account(username,password)

            if res != "":
                self.main_session = res
                print(lightgreen +  f"[ + ] Main session is {res} .")
            else:
                print(darkred +  f"[ X ] Error Login with Account!")
                enter_to_exit()
        else:
            self.main_session = str(input(lightcyan+"[ + ] Session : "))
            print(lightgreen +  f"[ + ] Main session is {self.main_session} .")

        self.sleep = int(input("[ + ] Sleep ( 35 - 60 ) : "))

   
        sendlike = int(input("[ 1 ] Like Story\n[ 2 ] No Like\n==>"))
        if sendlike == 1:
            self.like = True
        else:
            self.like = False

        if mod == 1:
            self.start_target_followers()
        elif mod == 2:
            self.start_target_followings()
        else:
            self.start_your_followings()



    # 1 [[ Target Follwers ]]    


    def start_target_followers(self):

        print("[ + ] Starting Please wait ...")

        time.sleep(1)

        while 1:

            self.is_there_more = True

            self.max_id = ""

            threading.Thread(target=self.printing).start()

            while self.is_there_more:

                if self.max_id == "":

                    self.get_target_followers(first=True)
                
                else:
                    self.get_target_followers(first=False)


                time.sleep(self.sleep)
        
        print(lightyellow+"[ + ] Bot Stopped After watching all stories.")
        enter_to_exit()

    def printing(self):
        while self.is_there_more:
            clear()
            print(f"""
{darkred}- Watching Stories
{darkyellow}---------------------------------------------------
{lightcyan}[ Users Grabbed : {len(self.all_users)} ],
{lightgreen}[ Watched Stories : {self.done} ],
{lightblue}[ User without stories : {self.nostories} ],
{lightred}[ Error watching : {self.error} ]
{darkyellow}---------------------------------------------------
            """)
            time.sleep(1)
    
    def get_target_followers(self,first=True):

        

        headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent':
                    'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
                'Cookie': f'sessionid={random.choice(self.sessions)}',
        }

        params = {}

        if first:
            params = {
                'search_surface': 'follow_list_page',
                'query': '',
                'enable_groups': 'true',
                'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
            }
        else:
            params = {
                    'search_surface': 'follow_list_page',
                    'max_id': self.max_id,
                    'query': '',
                    'enable_groups': 'true',
                    'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
             }
        response = requests.get(
                    f'https://i.instagram.com/api/v1/friendships/{self.target_id}/followers/',
                    params=params,
                    headers=headers)
        
        try:
            for user in response.json()['users']:
                if not user['is_private']:
                    self.users.append( { "userid":user['pk'],"username": user['username']})
                    self.all_users.append({ "userid":user['pk'],"username": user['username']})
            
            if response.json()['next_max_id'] != "" or response.json()['next_max_id'] != None:
                self.max_id = response.json()['next_max_id']
            else:
                self.is_there_more = False
            self.watch_grabbed()
            
        except Exception as e:
            
            self.error+=1
            if first:
                self.get_target_followers(first=True)
            else:
                self.get_target_followers(first=False)


    def get_stories(self,user) -> list:
        try:
            stories = []
            headers = {
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'User-Agent':
                        'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-csrftoken': 'missing',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'Cookie': f'sessionid={random.choice(self.sessions)}',
            }

            req = requests.get(f'https://i.instagram.com/api/v1/feed/user/{user["userid"]}/story/',headers=headers)
            if not req.text.__contains__('"reel":null,'):
                stories = req.json()["reel"]['items']
                return stories
            else:
                return []
        except:
            self.error+=1

            self.get_stories(user)

            return []


            
    def watch_grabbed(self):

        for user in self.users:

            stories = self.get_stories(user=user)

            if len(stories) > 0 :

                for st in stories:

                    url = 'https://www.instagram.com/api/v1/stories/reel/seen'
                    current_timestamp = int(time.time())
                    headers = {
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'User-Agent':
                        'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-csrftoken': 'missing',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                            'Cookie': f'sessionid={self.main_session}',
                    }
                    data = {
                        'reelMediaId': st['pk'],
                        'reelMediaOwnerId': user["userid"],
                        'reelId': user["userid"],
                        'reelMediaTakenAt': current_timestamp,
                        'viewSeenAt': current_timestamp,
                    }
                    req2 = requests.post(url,data=data,headers=headers)
                    if req2.text.__contains__('{"status":"ok"}'):
                                self.done += 1
                    else:
                                self.error += 1

                    time.sleep(1)
                
                last_story = stories[-1]
                data = {
                                    'media_id': str(last_story['id']),
                    }
                req2 = requests.post('https://i.instagram.com/api/v1/story_interactions/send_story_like',data=data,headers = {
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'User-Agent':
                        'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-csrftoken': 'missing',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                            'Cookie': f'sessionid={self.main_session}',
                    })
            else:
                
                self.nostories += 1
            
            time.sleep(3)
        
        self.users.clear()

    # 2 [[ Target Followings ]] 

    def start_target_followings(self):

        print("[ + ] Starting Please wait ...")

        time.sleep(1)


        while 1:

            self.is_there_more = True

            self.max_id = ""

            threading.Thread(target=self.printing).start()

            while self.is_there_more:

                if self.max_id == "":

                    self.get_target_followings(first=True)
                
                else:
                    self.get_target_followings(first=False)


                time.sleep(self.sleep)
        
        print(lightyellow+"[ + ] Bot Stopped After watching all stories.")
        enter_to_exit()
 

    def get_target_followings(self,first=True):

        headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent':
                    'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
                'Cookie': f'sessionid={random.choice(self.sessions)}',
        }

        params = {}

        if first:
            params = {
                'search_surface': 'follow_list_page',
                'query': '',
                'enable_groups': 'true',
                'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
            }
        else:
            params = {
                    'search_surface': 'follow_list_page',
                    'max_id': self.max_id,
                    'query': '',
                    'enable_groups': 'true',
                    'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
             }
        response = requests.get(
                    f'https://i.instagram.com/api/v1/friendships/{self.target_id}/following/',
                    params=params,
                    headers=headers)
        
        try:
            for user in response.json()['users']:
                if not user['is_private']:
                    self.users.append( { "userid":user['pk'],"username": user['username']})
                    self.all_users.append({ "userid":user['pk'],"username": user['username']})
            if response.json()['next_max_id'] != "" or response.json()['next_max_id'] != None:
                self.max_id = response.json()['next_max_id']
            else:
                self.is_there_more = False
            self.watch_grabbed()
            
        except Exception as e:
            print(e)
            self.error+=1
            if first:
                self.get_target_followings(first=True)
            else:
                self.get_target_followings(first=False)

    # 2 [[ Target Followings ]] 

    def get_main_id(self) -> str :

        headers = {
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'User-Agent':
                        'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-csrftoken': 'missing',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                            'Cookie': f'sessionid={self.main_session}',
        }

        try:
            req = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true",headers=headers)

            return str(req.json()['user']['pk'])
        
        except:

            return "error"

            


    def start_your_followings(self):

        print("[ + ] Starting Please wait ...")

        time.sleep(1)

        r = self.get_main_id()

        if r == "error":
            print(darkred + f"[ X ] Error grabbing Your id.")
            enter_to_exit()
        else:
            pass

        while 1:

            self.is_there_more = True

            self.max_id = ""

            threading.Thread(target=self.printing).start()

            while self.is_there_more:

                if self.max_id == "":

                    self.get_your_followings(first=True)
                
                else:
                    self.get_your_followings(first=False)


                time.sleep(self.sleep)

        
        print(lightyellow+"[ + ] Bot Stopped After watching all stories.")
        enter_to_exit()
 

    def get_your_followings(self,first=True):

        headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent':
                    'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
                'Cookie': f'sessionid={random.choice(self.sessions)}',
        }

        params = {}

        if first:
            params = {
                'search_surface': 'follow_list_page',
                'query': '',
                'enable_groups': 'true',
                'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
            }
        else:
            params = {
                    'search_surface': 'follow_list_page',
                    'max_id': self.max_id,
                    'query': '',
                    'enable_groups': 'true',
                    'rank_token': '2eeb3b18-6279-4df7-bbc3-4ef518081a7c',
             }
        response = requests.get(
                    f'https://i.instagram.com/api/v1/friendships/{self.target_id}/following/',
                    params=params,
                    headers=headers)
        
        try:
            for user in response.json()['users']:
                if not user['is_private']:
                    self.users.append( { "userid":user['pk'],"username": user['username']})
                    self.all_users.append({ "userid":user['pk'],"username": user['username']})
            if response.json()['next_max_id'] != "" or response.json()['next_max_id'] != None:
                self.max_id = response.json()['next_max_id']
            else:
                self.is_there_more = False
            self.watch_grabbed()
            
        except Exception as e:
            self.error+=1
            if first:
                self.get_your_followings(first=True)
            else:
                self.get_your_followings(first=False)

                

            

        
