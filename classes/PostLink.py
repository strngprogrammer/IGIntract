import requests , uuid , time , threading , random , string , re

from lib.colors import *
from lib.logo import print_logo,clear,enter_to_exit
from lib.login import *
from lib.funcs import *
class GetPostLink():
  def __init__(self) -> None:
        
    self.sessions = []
    self.done = 0
    self.error = 0
      
  def get_info(self,sessions):

      self.sessions = sessions
      
      clear()
      print_logo()
      print(lightred + "- Copy Post Link")
      print(lightcyan + "- to use this mode you need to : ")
      print(lightyellow + "1 - use multiple sessions to comment")
      print(lightyellow + "2 - add the post link")
      print(lightyellow + "3 - use a good sleep to make sure that your account will work safe like ( 20 - 40 )")
      print(lightblue + "Good Luck !!")

     
      self.start_signle_link()
      
        
  def start_signle_link(self):
         
    self.link = str(input( lightcyan + "- Enter Link : "))

    self.get_post_info()

    self.sleep = int(input(lightcyan + "[ + ] Enter Sleep ( 30 <  ) : "))

    threading.Thread(target=self.printing).start()

    self.start_copying()
  
  def printing(self):
        while 1:
            clear()
            print(f"""
{darkred}- Sharing post with Copying
{darkyellow}---------------------------------------------------
{lightgreen}[ Shares : {self.done} ],
{lightred}[ Error sharing : {self.error} ],
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
      match = re.search(r'{"path":{"user_id":"(.*?)"},"query"', req.text)
      if match:
          self.user_id = match.group(1)
      else:
          print(darkred + "[ X ] No User Found ...")
          enter_to_exit()
      

    except:
      print(darkred + "[ X ] Error grabbing post info trying again ...")
      self.get_post_info()
    

  def start_copying(self):
     
    for session in self.sessions:
       
      
        headers = {
                    'user-agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-csrftoken': 'missing',
                    'cookie': f'sessionid={session};'
                }
        
        params = {'share_to_app': 'copy_link',}

# response = requests.get(
#     'https://i.instagram.com/api/v1/media/3141112998000832165_4213518589/permalink/',
#     params=params,
#     cookies=cookies,
#     headers=headers,
#     verify=False,
# )

        req = requests.get(f'https://i.instagram.com/api/v1/media/{self.post_id}_{self.user_id}/permalink/', params=params, headers=headers)
        print(req.text)                                       
        if req.text.__contains__("\"permalink\""):
          self.done+=1
        else:
          self.error+=1
    
    time.sleep(self.sleep)

    
