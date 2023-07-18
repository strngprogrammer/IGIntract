import requests , uuid , time , threading , random , string , re

from lib.colors import *
from lib.logo import print_logo,clear,enter_to_exit
from lib.login import *
from lib.funcs import *

class IntractExplore:
    def __init__(self) -> None:
        self.sessions = []
        self.intracted_done = 0
        self.likes = 0
        self.error_likes = 0
        self.commented = 0
        self.error_commented = 0
        self.error = 0
        self.posts = []
        self.posts_all = []
        self.comments =  []
        self.main_session = ''
        self.send_comment = False


    def get_info(self,sessions):

      self.sessions = sessions
      
      clear()
      print_logo()
      print(lightred + "- Intract in explore posts")
      print(lightcyan + "- to use this mode you need to : ")
      print(lightyellow + "1 - use multiple sessions to grab posts")
      print(lightyellow + "2 - select if you want to comment or not")
      print(lightyellow + "3 - enter your main account that you want to intract in the posts with")
      print(lightyellow + "4 - use a good sleep to make sure that your account will work safe like ( 40 - 60 )")
      print(lightblue + "Good Luck !!")

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
        
      text = f"""
{lightblue}- do you want to comment :
{darkblue}[ 1 ] Yes Comment
{darkblue}[ 2 ] No dont't comment 
        """
      print(text)
      inp = int(input(darkyellow + "select -> "))

      if inp == 1:
          
          self.send_comment = True

          self.get_comments()
        
      else:
          
          self.send_comment = False
      
      self.sleep = int(input(lightcyan + "[ + ] Enter Sleep : "))

      

      self.start_getting()

    def printing(self):
        while 1:
            clear()
            print(f"""
{darkred}- Intracting
{darkyellow}---------------------------------------------------
{lightblue}- Posts grabbed : {len(self.posts_all)}
{lightgreen}- Intracted with : {self.intracted_done}
{lightgreen}- Liked : {self.likes}
{lightgreen}- Commented : {self.commented}
{lightred}- Error liked : {self.error_likes}
{lightred}- Error Commented : {self.error_commented}
{darkred}- Errors : {self.error}
{darkyellow}---------------------------------------------------
            """)
            time.sleep(1)

    def start_getting(self):
        print("[ + ] Starting Please wait ...")

        time.sleep(1)
        self.max_id=0
        threading.Thread(target=self.printing).start()
        while 1:

            self.get_explore()

            self.max_id += 1

            time.sleep(120)

    def get_explore(self):

        try:


            headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent':
                    'Instagram 151.0.0.23.120 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
                'Cookie': f'sessionid={random.choice(self.sessions)}',
            }

            params = {
                'is_prefetch': 'false',
                'omit_cover_media': 'true',
                'max_id': str(self.max_id),
                'module': 'explore_popular',
                'use_sectional_payload': 'true',
                'timezone_offset': '10800',
                'cluster_id': 'explore_all:0',
                'session_id': str(uuid.uuid4()),
                'include_fixed_destinations': 'true',
            }

            response = requests.get(
            'https://i.instagram.com/api/v1/discover/topical_explore/',
            params=params,
            headers=headers,
            )

            sectional_items = response.json()['sectional_items']


            for secitem in sectional_items:


                if str(secitem).__contains__("fill_items"):

        
                    fill_items = secitem['layout_content']['fill_items']
                        
                    for item in fill_items:

                        self.posts.append(item)

                        self.posts_all.append(item)
                
                elif str(secitem).__contains__("medias"):

                    fill_items = secitem['layout_content']['medias']
                        
                    for item in fill_items:

                        self.posts.append(item)

                        self.posts_all.append(item)


            self.intract_grabbed()


        except Exception as e:
            self.error+=1
            self.get_explore()


    def intract_grabbed(self):

        for item in self.posts:

            post_pk = item['media']['pk']
            post_id = item['media']['id']

            self.send_intract(post_pk,post_id)

            time.sleep(self.sleep)


        self.posts.clear()

    
    def send_intract(self,post_pk,post_id):
        
        try:

            headers = {
                    'authority': 'www.instagram.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                    'content-type': 'application/x-www-form-urlencoded',
                    # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=59258159580; csrftoken=Nz5J9c8JFTUq5S5mq3HXmDQKpbtUMHjR; sessionid=59258159580%3Aato8fcgqyOGSAf%3A11%3AAYd6JKX-4O9B9OYqACG9SfBzuh4I0B7K6RUN6RKOng; rur="ODN\\05459258159580\\0541719867252:01f76c7348a934e2efc58048bcf1c7e3f35cade0ea57fd8f2bf471c1bd418fb0d516ba70"',
                    'origin': 'https://www.instagram.com',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'viewport-width': '1200',
                    'x-asbd-id': '129477',
                    'x-csrftoken': 'Nz5J9c8JFTUq5S5mq3HXmDQKpbtUMHjR',
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': 'hmac.AR1YKgAIzf5ITDs0fe4ojrUyIig8BTq2JH8Nkwfxwi_gSSKA',
                    'x-instagram-ajax': '1007781660',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie': f'sessionid={self.main_session};'
            }

            req_like = requests.post(f"https://www.instagram.com/api/v1/web/likes/{post_pk}/like/",headers=headers)

            if req_like.text.__contains__('"status": "fail"') or req_like.text.__contains__('"status":"fail"'):

                self.likes += 1

            else:
                
                self.error_likes += 1
            
            headers = {
                    'authority': 'www.instagram.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                    'content-type': 'application/x-www-form-urlencoded',
                    # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=59258159580; csrftoken=Nz5J9c8JFTUq5S5mq3HXmDQKpbtUMHjR; sessionid=59258159580%3Aato8fcgqyOGSAf%3A11%3AAYd6JKX-4O9B9OYqACG9SfBzuh4I0B7K6RUN6RKOng; rur="ODN\\05459258159580\\0541719867252:01f76c7348a934e2efc58048bcf1c7e3f35cade0ea57fd8f2bf471c1bd418fb0d516ba70"',
                    'origin': 'https://www.instagram.com',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'viewport-width': '1200',
                    'x-asbd-id': '129477',
                    'x-csrftoken': 'Nz5J9c8JFTUq5S5mq3HXmDQKpbtUMHjR',
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': 'hmac.AR1YKgAIzf5ITDs0fe4ojrUyIig8BTq2JH8Nkwfxwi_gSSKA',
                    'x-instagram-ajax': '1007781660',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie': f'sessionid={self.main_session};'
            }
            data =  {
            'comment_text': f'{ random.choice(self.comments)} {random.choices(string.digits,k=3)}',
            }

            req = requests.post(f"https://www.instagram.com/api/v1/web/comments/{post_pk}/add/",data=data,headers=headers)                                       
            if req.text.__contains__("\"status\":\"ok\""):
                self.commented += 1
            else:
                self.error_commented += 1

            self.intracted_done += 1
            
        except Exception as e:
            print(e)
            self.error+=1
            self.send_intract(post_pk,post_id)


    

    def get_comments(self):
     
     comment = str(input(darkblue + "- Enter Comment or x/X to skip : "))

     if comment.lower() == 'x':  
        pass
     else:
        self.comments.append(comment)
        self.get_comments()




if __name__ == "__main__":
    IntractExplore()