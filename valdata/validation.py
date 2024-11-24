from typing import Union
import pytz
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from collections import Counter, defaultdict
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import functions as F

from .auxiliary import check_type, now_timedelta
from .visuals import padding10, padding25, padding35, b, b_bl, b_re, b_gr

def now() -> str:
  """
  Returns the current time in the 'dd-MonthAb-yy hh:mm:ss AM/PM' format for the 'America/Bogota' timezone.

  :return: Current time as a formatted string.
  """
  return datetime.now(pytz.timezone('America/Bogota')).strftime('%b-%d-%y %I:%M:%S %p')

def tms_0() -> None:
  """
  Initializes the start time for the valdata process by setting the global variable 'valdata_start_time' to the current time.

  :return: None
  """
  global valdata_start_time
  valdata_start_time = now_timedelta()

def tms_1() -> None:
  """
  Calculates and prints the elapsed time since 'tms_0' in the format 'days - hours:minutes:seconds'.

  :return: None
  """
  # t: time_elapsed
  t = now_timedelta() - valdata_start_time
  t = int(t.total_seconds())

  minutes, seconds = divmod(t, 60)
  hours, minutes = divmod(minutes, 60)
  days, hours = divmod(hours, 24)

  elapsed_time = '{:02d} - {:02d}:{:02d}:{:02d}'.format(int(days), int(hours), int(minutes), int(seconds))
  print('Execution time:', elapsed_time, f'[Finished at: {now()}]')

def get_overview(df: Union[pd.DataFrame, SparkDataFrame]) -> None:
  """
  Prints an overview of the given DataFrame, whether it's a Pandas or Spark DataFrame, including its shape, type, head and composition (Variables, unique counts and unique values).

  :param df: The DataFrame to be analyzed (Pandas or Spark).
  :return: None
  """
  # Use check_type function to determine type of df
  df_type = check_type(df)

  if df_type == 'Pandas DataFrame':
    print(b('Data shape:'), f'Variables: {df.shape[1]}\n            Registers: {df.shape[0]}')
    print(b('Type:'), b_bl(type(df)))
    # print(b('Structure:'), '\n', get_pandas_schema(df), '\n')
    print(b('Data:'))
    show_pandas_as_table(df)
    print(b('\nComposition:'))
    # show_pandas_as_table(df.nunique())
    unique_values = []
    for col in df.columns:
      unique_vals = df[col].unique()
      count_unique = len(unique_vals)
      if count_unique > 10:
        unique_values.append([col, count_unique, f'[{", ".join(map(str, unique_vals[:10]))}, {b_bl(f"{count_unique - 10} more")}]'])
      else:
        unique_values.append([col, count_unique, list(unique_vals)])
    print(tabulate(unique_values, headers=['Variable', 'Unique Count', 'Unique Values'], tablefmt='psql'))
  elif df_type == 'Spark DataFrame':
    print(b('Data shape:'), f'Variables: {len(df.columns)}\n            Registers: {df.count()}')
    print(b('Type:'), b_bl(type(df)))
    # print(b('Structure:'), '\n', df, '\n')
    print(b('Data:'))
    df.show(5)
    print(b('Composition:'))
    # distinct_counts = df.agg(*(F.countDistinct(F.col(c)).alias(c) for c in df.columns))
    # distinct_counts.show()
    # df.agg(*(F.collect_set(F.col(c)).alias(c) if df.select(c).distinct().count() <= 10 else F.concat(F.lit(''), F.countDistinct(F.col(c)).cast('string'), F.lit(' values')).alias(c) for c in df.columns)).show(truncate=max_col_length)
    unique_values = []
    for col in df.columns:
      count_unique = df.select(col).distinct().count()
      unique_vals = df.select(F.collect_set(col)).first()[0]
      # f'...' syntax conflicts with spark show(), then it is required to print as pd df
      if count_unique > 10:
        unique_values.append([col, count_unique, '[' + ', '.join(map(str, unique_vals[:10])) + f', {b_bl(f"{count_unique - 10} more")}]'])
      else:
        # unique_values.append([col, count_unique, list(unique_vals)]) #X
        unique_values.append([col, count_unique, '[' + ', '.join(map(str, unique_vals)) + ']'])
    # ANSI conflicts
    # unique_df = spark.createDataFrame(unique_values, ['Variable', 'Unique Count', 'Unique Values'])
    # unique_df.show(truncate=False)
    # pandas_df = unique_df.toPandas()

    pandas_df = pd.DataFrame(unique_values, columns=['Variable', 'Unique Count', 'Unique Values'])
    print(tabulate(pandas_df, headers='keys', tablefmt='psql', showindex=False))
  else:
    print(f'Unsupported DataFrame type: {df_type}')

def get_pandas_schemaStr(df: pd.DataFrame) -> str:
  """
  Returns a schema-like representation of a Pandas DataFrame, similar to the Spark DataFrame schema.
  
  :param df: The Pandas DataFrame to extract schema from.
  :return: A string representation of the DataFrame's schema.
  """
  schema_info = 'DataFrame['
  column_info = []
  for col in df.columns:
    dtype = str(df[col].dtype)
    if dtype == 'object':
      dtype = 'string'  # Align with Spark's string type
    column_info.append(f'{col}: {dtype}')
  schema_info += ', '.join(column_info) + ']'
  return schema_info

def show_pandas_as_table(df: Union[pd.DataFrame, pd.Series], num_rows: int = 5) -> None:
  '''
  Display a Pandas DataFrame or Series in a tabular format, similar to the way Spark shows DataFrames.

  :param df: The Pandas DataFrame or Series to display.
  :param num_rows: The number of rows to display. Default is 5.
  :return: None
  '''
  if df.empty:
    print('DataFrame or Series is empty')
    return

  if isinstance(df, pd.Series):
    df = df.to_frame()
    data = df[0].tolist()
    headers = df.index.tolist()
    print(tabulate([data], headers=headers, tablefmt='psql'))
  else:
    data = df.head(num_rows).values.tolist()
    headers = df.columns.tolist()
    print(tabulate(data, headers=headers, tablefmt='psql'))
    print(f'only showing top {num_rows} rows')

def tblt_ocurrences(df_columns, conditionated: bool = False) -> None:
  """
  Tabulates the occurrence of values in a specific variable or variables.

  :param df_columns: A list of Series or DataFrame columns to tabulate. 
    The first item is the variable of interest, and the second item is the condition (if any).
  :param conditionated: A boolean indicating whether to tabulate conditioned on a second variable.
  :return: None
  """
  # Normal
  if conditionated == False:
    if check_type(df_columns) == 'Series' or check_type(df_columns) == '':
      df_columns = [df_columns]
    counts = Counter(df_columns[0])
    counts_list = [(value, count) for value, count in counts.items()]
    print(tabulate(counts_list, headers=['Value', 'Count']))

  # Conditionated
  elif conditionated == True:
    nested_counter = defaultdict(Counter)
    for value, case in zip(df_columns[0], df_columns[1]):
      nested_counter[case][value] += 1

    counts_list = []
    for case, inner_counter in nested_counter.items():
      for value, count in inner_counter.items():
        counts_list.append((value, f'{df_columns[1].name}={case}', count))
    print(tabulate(sorted(counts_list, key=lambda x: x[0]), headers=['Value', 'Condition', 'Count']))

def tblt_concentrations(df, conditioner: str, thresholds: list) -> None:
  """
  Tabulates the concentration of data for a variable given a set of thresholds.

  :param df: The DataFrame containing the data to be analyzed.
  :param conditioner: The name of the column used as a condition for filtering.
  :param thresholds: A list of threshold values to evaluate the concentration.
  :return: None
  """
  concentration_results = []
  for threshold in thresholds:
    concentration_results.append((threshold, len(df[df[f'{conditioner}'] > threshold])))

  print('Concentration by threshold:')
  print(tabulate(concentration_results, headers=[f'Threshold for {conditioner}', 'Concentration']))

def unique_values(df) -> None:
  """
  Prints the unique values of each column in the given DataFrame.

  :param df: The DataFrame for which to display unique values.
  :return: None
  """
  print('Unique values per variable:\n')
  for column in df.columns:
    unique_values = df[column].unique()
    if len(unique_values) > 200:
      print(f'{column}: [{", ".join(map(str, unique_values[:10]))}, {len(unique_values) - 10} more]\n----------')
    else:
      print(f'{column}: {list(unique_values)}\n----------')

def equal_df(df1: pd.DataFrame, df2: pd.DataFrame, aggregated: bool = False) -> None:
  """
  Compare two Pandas DataFrames for equality, either element-wise or aggregated by columns.

  :param df1: pd.DataFrame - The first DataFrame to compare.
  :param df2: pd.DataFrame - The second DataFrame to compare.
  :param aggregated: bool - Determines the level of comparison.
    - If False, performs a full element-wise comparison, printing `True` if all elements across both DataFrames match, and `False` if any mismatch is found.
    - If True, performs an aggregated comparison, outputting a DataFrame showing `True` or `False` values for each cell, indicating equality by column for every row.
  :return: None
  """
  comparison = df1 == df2

  if aggregated == False:
    total_comparison = comparison.all().all()
    print(total_comparison)
  elif aggregated == True:
    print(comparison)

def equal_df_mult(dfs_dict: dict, df_comparison: str, row_count: bool = False) -> None:
  """
  Compare multiple DataFrames to a reference DataFrame for structural and row-wise equality.
  
  :param dfs_dict: dict - Dictionary where keys are DataFrame names (str) and values are the DataFrames (pd.DataFrame or Spark DataFrame) to compare.
  :param df_comparison: str - The name of the reference DataFrame within dfs_dict that other DataFrames will be compared against.
  :param row_count: bool - If True, includes row count for each DataFrame in the comparison output; if False, omits row count details.
  
  :return: None - Prints a summary of comparison results for each DataFrame in dfs_dict against the reference DataFrame.
  
  Functionality:
  1. **Column Comparison**:
  - Checks if the reference DataFrame (`df_comparison`) and each other DataFrame in `dfs_dict` have the same number of columns.
  - Skips the comparison if the column counts differ.
  
  2. **Row Comparison**:
  - Uses `.exceptAll()` for Spark DataFrames to identify row-wise differences between the reference and each other DataFrame, handling duplicates and row order.
  
  3. **Output Format**:
  - For identical DataFrames, outputs a checkmark (✓) indicating that both DataFrames have the same shape and no different rows.
  - For differing DataFrames, outputs an error (X) with row mismatch details.
  - If `row_count` is True, includes row counts for each DataFrame; otherwise, displays "Omitted" in place of row counts.
  
  :example:
    dfs_dict = {'df_name_1': df1, 'df_name_2': df2, 'df_name_comparison': df_ref}
    equal_df_mult(dfs_dict, 'df_name_comparison', row_count=True)
  """
  all_columns = set()
  for df in dfs_dict.values():
    all_columns.update(df.columns)
  all_columns = sorted(list(all_columns))

  df_comparison_ = dfs_dict[df_comparison]

  if row_count:
    df_comparison__count = df_comparison_.count()

  for df_nm, df in dfs_dict.items():
    print(f'--- Comparing [{df_comparison}] and {df_nm}')

    if len(df_comparison_.columns) != len(df.columns):
      print(f'{b("E")} The DataFrames have a different number of columns, operation cannot be performed\n')
      continue

    if df_nm != df_comparison:
      diff_rows_df1 = df.exceptAll(df_comparison_).count() #There are 2 comparisons considering order of operations and duplicate handling of this function
      diff_rows_df2 = df_comparison_.exceptAll(df).count()

      if row_count == False:
        df_comparison__count = 'Omitted'
        df_count = 'Omitted'
      elif row_count:
        df_count = df.count()

      if diff_rows_df1 == 0 and diff_rows_df2 == 0:
        print(f'{b_gr("✓")} {df_comparison} and {df_nm} have the same shape:')
        print(f'{df_comparison}'.ljust(padding25)+f'-> Columns: {len(df.columns)} x Rows: {df_comparison__count} | Different Rows Records: {diff_rows_df1}')
        print(f'{df_nm}'.ljust(padding25)+f'-> Columns: {len(df.columns)} x Rows: {df_count} | Different Rows Records: {diff_rows_df2}\n')
      else:
        print(f'{b_re("X")} {df_comparison} and {df_nm} have a different shape:')
        print(f'{df_comparison}'.ljust(padding25)+f'-> Columns: {len(df.columns)} x Rows: {df_comparison__count} | Different Rows Records: {diff_rows_df1}')
        print(f'{df_nm}'.ljust(padding25)+f'-> Columns: {len(df.columns)} x Rows: {df_count} | Different Rows Records: {diff_rows_df2}\n')

    elif df_nm == df_comparison:
      print(f'{b("—")} Skipping self reference\n')

def check_variables(dfs_dict: dict, df_comparison: str = None) -> None:
  """
  Compares the variables (columns) of multiple DataFrames, with an option to compare to a reference DataFrame.
  
  :param dfs_dict: dict - A dictionary where keys are DataFrame names (str) and values are the DataFrames (pd.DataFrame or Spark DataFrame) to compare.
  :param df_comparison: str or None - The name of the reference DataFrame to compare against. If None, all DataFrames are compared against each other.
  
  :return: None - Prints a table showing the columns of each DataFrame and highlights any discrepancies.
  
  Functionality:
  1. **Column Comparison**:
  - If `df_comparison` is provided, compares the columns of the specified DataFrame (`df_comparison`) with the other DataFrames in `dfs_dict`.
  - If `df_comparison` is not provided, compares all DataFrames against each other.
  
  2. **Missing Columns**:
  - The table will show 'Error' for missing columns in the reference DataFrame (`df_comparison`), or '...' for missing columns in other DataFrames when not in `df_comparison`.
  
  3. **Output Format**:
  - Displays a formatted table showing the column names of all DataFrames and their alignment. Missing or differing columns are highlighted.
  
  :example:
    dfs_dict = {'df_name_1': df1, 'df_name_2': df2, 'df_comparison': df_ref}
    check_variables(dfs_dict, df_comparison='df_comparison')
  """
  data_structure = check_type(dfs_dict[next(iter(dfs_dict))])
  all_columns = set()
  if df_comparison == None:
    max_varnum_key = max(dfs_dict, key=lambda key: len(dfs_dict[key].columns))
    df_max_varnum = dfs_dict[max_varnum_key]

    for df in dfs_dict.values():
      all_columns.update(df.columns)
    all_columns = sorted(list(all_columns))
    print(f'Mode: Comparing all variables')

  elif df_comparison != None:
    df_max_varnum = dfs_dict.get(df_comparison)
    all_columns = sorted(df_max_varnum.columns)
    print(f'Mode: Comparing to "{df_comparison}" variables')

  # padding = 35
  formatted_colnames = []
  formatted_columns = []
  for df_nm, df in dfs_dict.items():
    formatted_colname = b_bl(f'{df_nm} (x={len(df.columns)})'.ljust(padding35)) if df_nm == df_comparison else f'{df_nm} (x={len(df.columns)})'.ljust(padding35)
    formatted_colnames.append(formatted_colname)

    formatted_column_sub = []
    for colname in all_columns:
      if df_nm == df_comparison:
        formatted_column = colname if colname in df.columns else 'Error'
      else:
        formatted_column = colname if colname in df.columns else '...'
      formatted_column_sub.append(formatted_column)
    formatted_columns.append(formatted_column_sub)
  format_strct = '|' + '|'.join([f'{{:{padding35}}}'] * len(formatted_colnames)) + '|'
  header = format_strct.format(*formatted_colnames)
  separator = format_strct.replace('|', '+').format(*['-' * padding35] * len(formatted_colnames))
  formatted_columns = list(zip(*formatted_columns))

  print(separator)
  print(header)
  print(separator)
  for row in formatted_columns:
    # print(row)
    print(format_strct.format(*row))
  print(separator)