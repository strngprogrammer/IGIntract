import requests

def get_target_id(session,target) -> str:
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
            'Cookie': f'sessionid={session}'

    }
    req = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target}",headers=headers)

    try:
            user_id = str(req.json()['data']['user']['id'])
            return user_id
    except:
            return "false"