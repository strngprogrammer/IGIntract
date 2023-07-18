from .colors import *
import uuid , requests


uid = str(uuid.uuid4())


def load_accounts(file) -> list:
    accounts = []

    try:
        for account in file.read().splitlines():
                accounts.append(account)
        return accounts
    
    except Exception as e:
        return []
    
def load_sessions(file) -> list:
    accounts = []

    try:
        for account in file.read().splitlines():
                accounts.append(account)
        return accounts
    
    except Exception as e:
        return []
    

def login_single_account(user,password) -> str:
    headers = {
          'User-Agent':
              'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
          'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
          "Accept-Language": "Accept-Language",
          'Host': 'i.instagram.com',
          "X-IG-Connection-Type": "WIFI",
          "X-IG-Capabilities": "3brTvw==",
          'accept-encoding': 'gzip, deflate',
          "Accept": "*/*"
        }

    data = {
          "jazoest": "22452",
          "phone_id": uid,
          "enc_password": f"#PWD_INSTAGRAM:0:0:{password}",
          "username": user,
          "adid": uid,
          "guid": uid,
          "device_id": uid,
          "google_tokens": "[]",
          "login_attempt_count": "0"
        }

    req = requests.post("https://i.instagram.com/api/v1/accounts/login/",headers=headers,data=data)
    if req.text.__contains__("logged_in_user"):
            cookies = req.cookies['sessionid']
            print(lightgreen +  f"    [ + ] Logged in with {user}.")
            return cookies
        
    elif req.text.__contains__('checkpoint_required'):
            print(lightblue +  f"    [ ! ] checkpoint required {user}")
            cookies = req.cookies.get_dict()
            path = req.json()['challenge']['api_path']
                    
            info = requests.get(f"https://i.instagram.com/api/v1{path}",
                                    headers=headers, cookies=cookies)
            step_data = info.json()["step_data"]
            text = ""
            if "email" in step_data and "phone_number" in step_data:
                        text = text.join("[ 0 ] email \n")
                        text = text.join("[ 1 ] phone \n")
                        
            elif  "email" in step_data and not "phone_number" in step_data:
                        text = text.join("[ 0 ] email \n")
                        
            elif "phone_number" in step_data and not "email" in step_data:
                        text = text.join("[ 1 ] phone \n") 
            print(f"{step_data}")
            x = int(input("[ + ] select : "))
            call = ""
            if x == 0:
                call = "email"
            else:
                call = "phone"
            data = {}
            if call == "phone":
                data['choice'] = str(0)
                data['_uuid'] = uid
                data['_uid'] = uid
                data['_csrftoken'] = 'massing'
            else:
                data['choice'] = str(1)
                data['_uuid'] = uid
                data['_uid'] = uid
                data['_csrftoken'] = 'massing'
            challnge = req.json()['challenge']['api_path']
            send = requests.post(f"https://i.instagram.com/api/v1{challnge}",headers=headers, data=data, cookies=cookies)
            contact_point = send.json()["step_data"]["contact_point"]
            print(f'[+] code sent to : {contact_point}')
            code = str(input("[ ? ] Code : "))
            data = {}
            data['security_code'] = code,
            data['_uuid'] = uid,
            data['_uid'] = uid,
            data['_csrftoken'] = 'massing'
            send_code = requests.post(f"https://i.instagram.com/api/v1{path}", headers=headers, data=data,
                            cookies=cookies)
            if "logged_in_user" in send_code.text:
                cookies = req.cookies['sessionid']
                print(lightgreen +  f"    [ + ] Logged in with {user}.")
                return cookies
            else:
                  return ""
        
    else:
            print(darkred +  f"    [ X ] User or password is incorrect.")
            return ""
     
     


def login_with_accounts(accounts) -> list:

    sessions = []

    for account in accounts:
         
        user = account.split(":")[0]
        password = account.split(":")[1]

        headers = {
          'User-Agent':
              'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
          'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
          "Accept-Language": "Accept-Language",
          'Host': 'i.instagram.com',
          "X-IG-Connection-Type": "WIFI",
          "X-IG-Capabilities": "3brTvw==",
          'accept-encoding': 'gzip, deflate',
          "Accept": "*/*"
        }

        data = {
          "jazoest": "22452",
          "phone_id": uid,
          "enc_password": f"#PWD_INSTAGRAM:0:0:{password}",
          "username": user,
          "adid": uid,
          "guid": uid,
          "device_id": uid,
          "google_tokens": "[]",
          "login_attempt_count": "0"
        }

        req = requests.post("https://i.instagram.com/api/v1/accounts/login/",headers=headers,data=data)
        if req.text.__contains__("logged_in_user"):
            cookies = req.cookies['sessionid']
            sessions.append(cookies)
            print(lightgreen +  f"    [ + ] Logged in with {user}.")
        
        elif req.text.__contains__('checkpoint_required'):
            print(lightblue +  f"    [ ! ] checkpoint required {user}")
        else:
            print(darkred +  f"    [ X ] User or password is incorrect.")

    print(lightgreen + f'    [ ! ] Saved {len(sessions)} to sessions.txt!')

    return sessions
             