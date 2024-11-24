import sys
import pytz
from datetime import datetime
from IPython.core.display import display, HTML

padding10 = 10
padding25 = 25
padding35 = 35
max_col_length = 50

class TextStyle:
  RESET = '\033[0m'
  BOLD = '\033[1m'
  ITALIC = '\033[3m'
  UNDERLINE = '\033[4m'
  BLACK = '\033[30m'
  RED = '\033[31m'
  GREEN = '\033[32m'
  YELLOW = '\033[33m'
  BLUE = '\033[34m'
  MAGENTA= '\033[35m'
  CYAN = '\033[36m'
  WHITE = '\033[37m'

def b(text: str) -> str:
  """
  Prints the given text as bold.

  :param text: The text to be printed in bold.
  :return: The formatted bold text as a string.
  """
  return f'{TextStyle.BOLD}{text}{TextStyle.RESET}'

def b_bl(text: str) -> str:
  """
  Prints the given text as bold blue.

  :param text: The text to be printed in bold blue.
  :return: The formatted bold blue text as a string.
  """
  return f'{TextStyle.BOLD + TextStyle.BLUE}{text}{TextStyle.RESET}'

def b_re(text: str) -> str:
  """
  Prints the given text as bold red.

  :param text: The text to be printed in bold red.
  :return: The formatted bold red text as a string.
  """
  return f'{TextStyle.BOLD + TextStyle.RED}{text}{TextStyle.RESET}'

def b_gr(text: str) -> str:
  """
  Prints the given text as bold green.

  :param text: The text to be printed in bold green.
  :return: The formatted bold green text as a string.
  """
  return f'{TextStyle.BOLD + TextStyle.GREEN}{text}{TextStyle.RESET}'

def set_start(msg: str = '') -> None:
  """
  Initializes the environment by printing a message, the current time, and the Python version. It also sets custom styles for Jupyter Notebook cells.

  :param msg: Optional message to be printed at the start. Defaults to an empty string.
  :return: None
  """
  print(b(msg))
  print(datetime.now(pytz.timezone('America/Bogota')).strftime('%b-%d-%Y %I:%M:%S %p'))
  print('Python:', sys.version)
  # print((lambda: __import__('datetime').datetime.now(__import__('pytz').timezone('America/Bogota')).strftime('%b-%d-%Y %I:%M:%S %p'))())

  styles = '''
    <style>
      .jp-Notebook {
        background-color: #ece7d9;
      }
      .jp-Cell {
        background-color: WhiteSmoke;
        margin: 7px;
        border: 1px solid white;
        padding: 5px;
        border-radius: 5px;
        width: 97%;
        margin-left: auto;
        margin-right: auto;
      }
      .jp-Editor {
        background-color: white;
      }
      .jp-mod-active {
        border: 1px solid #2171b5;
        background-color: #dcd6c3;
      }
      .jp-OutputArea-output {
        background-color: lightyellow;
        border-radius: 5px;
      }
    </style>
  '''

  display(HTML(styles))
  display(HTML('<style>pre { white-space: pre !important; }</style>')) # Get a better spark parquet visualization