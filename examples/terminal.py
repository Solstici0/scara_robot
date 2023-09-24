import IPython
from IPython.terminal.embed import InteractiveShellEmbed
import scara
import logging 
import scara.can_pizza as pizza

def main():
    scara.logger.setLevel(logging.INFO)  # set info level for logger
    nelen = scara.Robot()  # creates an instance of the scara robot

     # Start an IPython terminal
    banner = "Welcome to the scara IPython terminal"
    ipshell = InteractiveShellEmbed(banner1=banner)
    ipshell()

if __name__ == "__main__":
    main()