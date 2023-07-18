import requests , uuid , time , threading , random , string ,os

from lib.colors import *
from lib.logo import print_logo,clear,enter_to_exit
from lib.login import *
from classes.watchlikeStories import WatchLikeStories
from classes.commentPosts import CommentTargetedPosts

from classes.intractExplore import IntractExplore
from classes.PostLink import GetPostLink

os.system("color")

clear()




class MainClass:

    def __init__(self) -> None:
        
        self.sessions = []
        self.accounts = []

        set_init() # set the color to auto reset when using

        self.start_info() # to get info and login or sessions

    def start_info(self):

        clear()

        print_logo()

        time.sleep(1.5)

        

        login_type = int(input("    [ 1 ] Login user:password\n\n    [ 2 ] Login with Sessions\n\n    ==> "))

        if login_type == 1:
            res = load_accounts(open("accounts.txt",'r'))
            if len(res) > 0:
                self.accounts = res
                print(lightgreen+f"    [ + ] Loaded {len(res)} Account/s now i will login ...")
                res = login_with_accounts(self.accounts)
                if len(res) > 0:
                    self.sessions = res
                    for session in self.sessions:
                        with open("sessions.txt",'a') as a:
                            a.write(session+"\n")
                else:
                    print(darkred+f"    [ X ] No accounts logged in ...")
            else:
                print(darkred+f"    [ X ] No accounts in file ...")
        else:
            res = load_sessions(open("sessions.txt",'r'))
            if len(res) > 0:
                self.sessions = res
                print(lightgreen+f"    [ + ] Loaded {len(res)} Session/s ...")
            else:
                print(darkred+f"    [ X ] No sessions in file ...")

        time.sleep(1.5)

        clear()

        print(darkblue+'\n\n    Please select what you want to do : ')
        print(lightmegenta+'    [ 1 ] watch and like stories  مشاهدة ولايك الستوريات')
        print(lightmegenta+'    [ 2 ] comment in targeted posts التعليق على منشورات معينه')
        print(lightmegenta+'    [ 3 ] intract with explore posts التفاعل مع منشورات الاكسبلور')
        print(lightmegenta+'    [ 4 ] share post link to get on explore نسخ رابط منشور معين لايصاله للاكسبلور')

        selected = int(input(lightgreen + "    select -> " ))

        if selected == 1:
            WatchLikeStories().get_info(sessions=self.sessions)
        elif selected == 2:
            CommentTargetedPosts().get_info(sessions=self.sessions)
        elif selected == 3:
            IntractExplore().get_info(sessions=self.sessions)
        elif selected == 4:
            GetPostLink().get_info(sessions=self.sessions)
        else:
            exit()





if __name__ == "__main__":
    MainClass()
