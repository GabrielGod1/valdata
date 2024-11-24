import types
from typing import Union
import pytz
from datetime import datetime
import pandas as pd
import numpy as np
from pyspark.sql import DataFrame as SparkDataFrame

def check_type(item: Union[pd.Series, np.ndarray, pd.DataFrame, SparkDataFrame, list, dict]) -> str:
  """
  Checks the type of the given item and returns its name as a string.

  :param item: The item whose type is to be checked.
  :return: A string indicating the type of the item.
  """
  if isinstance(item, pd.Series):
    return 'Pandas Series'
  elif isinstance(item, np.ndarray):
    return 'NumPy Array'
  elif isinstance(item, pd.DataFrame):
    return 'Pandas DataFrame'
  elif isinstance(item, SparkDataFrame):
    return 'Spark DataFrame'
  elif isinstance(item, list):
    return 'List'
  elif isinstance(item, dict):
    return 'Dictionary'
  else:
    return 'Unknown'
  
def path_correction(path: str) -> str:
  """
  Corrects the path by replacing backslashes with forward slashes.

  :param path: The file path to be corrected.
  :return: The corrected path with forward slashes.
  """
  return path.replace('\\', '/')

def now_timedelta() -> datetime:
  """
  Returns the current time in the 'dd-MonthAb-yy hh:mm:ss AM/PM' format for the 'America/Bogota' timezone.

  :return: Current time in the 'America/Bogota' timezone as a datetime object.
  """
  return datetime.now(pytz.timezone('America/Bogota'))