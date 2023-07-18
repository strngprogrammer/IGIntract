from .colors import *
import os

logo = f"""

{lightmegenta}    ██╗ ██████╗ ██╗███╗   ██╗████████╗██████╗  █████╗  ██████╗████████╗
{lightmegenta}    ██║██╔════╝ ██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
{darkmegenta}    ██║██║  ███╗██║██╔██╗ ██║   ██║   ██████╔╝███████║██║        ██║   
{darkmegenta}    ██║██║   ██║██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║        ██║   
{darkblue}    ██║╚██████╔╝██║██║ ╚████║   ██║   ██║  ██║██║  ██║╚██████╗   ██║   
{darkblue}    ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   

{lightyellow}    | - this but made by @9hea - @GGVVGG           |
{lightyellow}    | - with this bot you can :                    |
{lightyellow}    | 1 - watch and like stories                   |
{lightyellow}    | 2 - comment in targeted posts                |
{lightyellow}    | 3 - intract with explore posts               |
{lightyellow}    | 4 - copy the post link to get in on explore  |


"""

def print_logo():

    print(logo)

def clear():
    os.system("clear||cls")

def enter_to_exit():
    input(darkblue +  "[ X ] Enter to exit ...")
    exit()


