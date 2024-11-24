import os, sys, types
import subprocess
from datetime import datetime
import pyspark
from pyspark.sql import SparkSession

from .auxiliary import path_correction
from .visuals import b, b_bl, b_re, b_gr

def save_file():
  #!! ToDo
  pass

def read_file():
  #!! ToDo
  pass

def check_directory(directory_path: str, create_if_not_exists: bool = False) -> None:
  """
  Checks if a directory exists at the given path.

  :param directory_path: str - The directory path to check.
  :param create_if_not_exists: bool - Flag to create the directory if it doesn't exist. Default is False.
  :return: None
  
  :example:
      check_directory('/path/to/directory', create_if_not_exists=True)  # Creates the directory if it does not exist
  """
  directory_path = path_correction(directory_path)

  if os.path.exists(directory_path):
    print(f'{b_gr("✓")} The directory \'{directory_path}\' exists')
  else:
    print(f'{b_re("X")} The directory \'{directory_path}\' does not exist')
    if create_if_not_exists:
      try:
        os.makedirs(directory_path)
        print(f'{b_gr("✓")} Directory \'{directory_path}\' created successfully')
      except Exception as e:
        print(f'{b_re("X")} Failed to create the directory \'{directory_path}\'. Error: {str(e)}')

def get_directories(directory_path = 'Current'):
  """
  Displays the contents of the specified directory.

  :param directory_path: The directory to list contents of. If 'Current', the current working directory is used.
  :return: None
  """
  directory_path = path_correction(directory_path)

  if directory_path == 'Current':
    current_directory = os.getcwd()
  else:
    current_directory = directory_path
  print(f'\'{current_directory}\'')

  print(b('Contents of the current directory:'))
  for item in os.listdir(current_directory):
    print(item)

def get_modules() -> None:
  """
  Prints the currently loaded modules.

  :return: None
  """
  print('Loaded modules:\n')
  for module_name in sorted(sys.modules.keys()):
    print(module_name)

def add_module_path(module_path: str) -> None:
  """
  Adds a new module path to the Python module search path.

  :param module_path: The path to the directory to add to the module search path.
  :return: None
  """
  sys.path.insert(0, module_path)

def get_hadoop_version():
  """
  Retrieves and prints the versions of Python, Hadoop, Spark, and PySpark.

  This function attempts to get the version of Hadoop using the 'hadoop version' command,
  the version of Spark through the SparkSession, and the version of PySpark from the pyspark library.

  If Hadoop is not installed or if there is an error during execution, it will handle the error gracefully.

  :return: None
  """
  try:
    hadoop_version = subprocess.check_output(['hadoop', 'version'], stderr=subprocess.STDOUT)
    hadoop_version = hadoop_version.decode('utf-8').split('\n')[0]
  except FileNotFoundError:
    hadoop_version = 'Hadoop might not be installed or properly loaded.'
  except subprocess.CalledProcessError as e:
    hadoop_version = f'Error executing "hadoop version": {e.output.decode("utf-8")}'
  
  python_version = sys.version
  hadoop_version = hadoop_version
  spark_observer = SparkSession.builder.appName('version_check').getOrCreate()
  spark_version = spark_observer.version
  pyspark_version = pyspark.__version__

  print(f'Python Version: {python_version}')
  print(f'Hadoop Version: {hadoop_version}')
  print(f'Spark Version: {spark_version}')
  print(f'PySpark Version: {pyspark_version}')
  spark_observer.stop()