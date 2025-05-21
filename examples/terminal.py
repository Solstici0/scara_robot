import IPython
from IPython.terminal.embed import InteractiveShellEmbed
import scara
import logging 
import scara.can_pizza as pizza
import argparse

def main(use_can = False):
    scara.logger.setLevel(logging.INFO)  # set info level for logger
    nelen = scara.Robot(use_can=use_can)  # creates an instance of the scara robot

     # Start an IPython terminal
    banner = "Welcome to the scara IPython terminal"
    ipshell = InteractiveShellEmbed(banner1=banner)
    ipshell()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with one optional argument")
    parser.add_argument('use_can',
                        nargs='?',
                        help='If an argument is given, communication over CAN is used',
                        default=None)
    args = parser.parse_args()
    main(args.use_can)