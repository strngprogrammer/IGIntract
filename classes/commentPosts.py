import requests , uuid , time , threading , random , string , re

from lib.colors import *
from lib.logo import print_logo,clear,enter_to_exit
from lib.login import *
from lib.funcs import *
class CommentTargetedPosts():
  def __init__(self) -> None:
        
    self.sessions = []
    self.done = 0
    self.error = 0
    self.comments = []
      
  def get_info(self,sessions):

      self.sessions = sessions
      
      clear()
      print_logo()
      print(lightred + "- Comment in posts")
      print(lightcyan + "- to use this mode you need to : ")
      print(lightyellow + "1 - use multiple sessions to comment")
      print(lightyellow + "2 - add the post link")
      print(lightyellow + "3 - use a good sleep to make sure that your account will work safe like ( 40 - 60 )")
      print(lightblue + "Good Luck !!")

     
      self.start_signle_link()
      
        
  def start_signle_link(self):
         
    self.link = str(input( lightcyan + "- Enter Link : "))

    self.get_post_info()

    self.get_comments()

    self.sleep = int(input(lightcyan + "[ + ] Enter Sleep ( 60 <  ) : "))

    threading.Thread(target=self.printing).start()

    self.start_comments()
  
  def printing(self):
        while 1:
            clear()
            print(f"""
{darkred}- Commenting
{darkyellow}---------------------------------------------------
{lightgreen}[ Comments Sent : {self.done} ],
{lightred}[ Error Comment : {self.error} ],
{lightcyan}[ Comments loadded ] : {len(self.comments)} 
{darkyellow}---------------------------------------------------
            """)
            time.sleep(1)

  def get_post_info(self):

    try:

      head = {
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'viewport-width': '1233',
        'x-fb-lsd': 'XLZi2eMiGsL15b7bGKZiEA',
        'x-fb-qpl-active-flows': '931594241',
        'x-ig-d': 'www',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'x-csrftoken':"missing",
        "cookie":"sessionid="+random.choice(self.sessions)
      }

      req = requests.get(self.link,headers=head)
      match = re.search(r'{"media_id":"(.*?)"}', req.text)
      if match:
          self.post_id = match.group(1)
      else:
          print(darkred + "[ X ] No Post Found ...")
          enter_to_exit()
      

    except:
      print(darkred + "[ X ] Error grabbing post info trying again ...")
      self.get_post_info()
    
  def get_comments(self):
     
     comment = str(input(darkblue + "- Enter Comment or x/X to skip : "))

     if comment.lower() == 'x':  
        pass
     else:
        self.comments.append(comment)
        self.get_comments()
  
  def start_comments(self):
     
    for session in self.sessions:
       
      
        headers = {
                    'authority': 'www.instagram.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                    'content-type': 'application/x-www-form-urlencoded',
                    # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=59258159580; csrftoken=Nz5J9c8JFTUq5S5mq3HXmDQKpbtUMHjR; sessionid=59258159580%3Aato8fcgqyOGSAf%3A11%3AAYd6JKX-4O9B9OYqACG9SfBzuh4I0B7K6RUN6RKOng; rur="ODN\\05459258159580\\0541719867252:01f76c7348a934e2efc58048bcf1c7e3f35cade0ea57fd8f2bf471c1bd418fb0d516ba70"',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/p/CgtAYBRLLdh/',
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
                    'cookie': f'sessionid={session};'
        }
        data =  {
            'comment_text': f'{ random.choice(self.comments)} {random.choices(string.digits,k=3)}',
            }

        req = requests.post(f"https://www.instagram.com/api/v1/web/comments/{self.post_id}/add/",data=data,headers=headers)                                       
        if req.text.__contains__("\"status\":\"ok\""):
          self.done+=1
        else:
          self.error+=1
    
    time.sleep(self.sleep)