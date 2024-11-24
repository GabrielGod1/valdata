.. valdata documentation master file, created by
   sphinx-quickstart on Mon Sep 23 12:11:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _valdata:

===============================================
valdata - Data validation and consistency toolkit
===============================================

**valdata** is a robust Python package developed to streamline data validation and consistency checks across various data structures and environments, particularly those used in financial and risk analysis. By providing structured data insights, comparisons, and file management capabilities, `valdata` simplifies data analysis and improves data quality assurance processes.

Features
========
- **Compatibility with Pandas and Spark DataFrames**: Ensures easy integration with common data structures.
- **Detailed Data Insights**: View unique values, data types, and column composition for better data understanding.
- **Data Consistency Checks**: Compare multiple DataFrames for equality, validate variables, and analyze column-specific occurrences and concentrations.
- **Flexible File Management**: Seamlessly work with directories and modules, allowing for more efficient data processing.
- **System Compatibility**: Detects versions of relevant software, such as Hadoop, Spark, and PySpark, to help ensure compatibility in distributed computing environments.

Use Cases
=========
- **Financial Analysis**: Easily validate data from multiple sources, ensuring consistent and accurate datasets for risk assessments or portfolio analysis.
- **Data Audits**: Rapidly identify and troubleshoot discrepancies in datasets, especially useful for large data teams.
- **Risk Management**: Monitor data for anomalies, rare occurrences, or threshold-based concentrations in high-risk datasets.
- **Data Pipeline Debugging**: Detect and correct schema mismatches or data quality issues within ETL (Extract, Transform, Load) processes.

Getting Started
===============

To install `valdata`, ensure that Python and Spark are set up beforehand. Then, install the package:

.. code-block:: bash

  pip install valdata

Modules
=======
  
• Auxiliary:

  This module provides utility functions for type checking, path correction, and timezone-aware datetime retrieval. These functions are particularly useful within the library, enabling seamless integration with other module components.
  
• Utils:

  This module includes utility functions for managing directories, displaying system information, and integrating with Spark. It provides tools for checking and creating directories, listing contents, managing Python module paths, and retrieving version details for Hadoop, Spark, and PySpark.

• **Validation:**

  Module for DataFrame analysis and comparison, supporting both Pandas and Spark DataFrames.

  This module includes functions to track execution time, print DataFrame summaries, compare DataFrames, and tabulate various statistics. It supports operations like counting unique values, checking variable consistency, and comparing DataFrames either element-wise or by structure. It also provides functionality to visualize data distributions and concentrations with thresholds.

• Visuals:

  This module defines various utility functions and styles for text formatting and Jupyter Notebook customization.

Usage Examples
==============

**Example 1: Data Overview**

Analyze a Pandas DataFrame for a summary of its structure and unique values in each column:

.. code-block:: python

  import pandas as pd
  from valdata import get_overview

  # Example DataFrame
  df = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bob', 'Alice', 'David'],
    'Score': [88, 95, 88, 75]
  })

  get_overview(df)

This function provides an instant overview of variables, data types, unique values, and structure.

**Example 2: Data Consistency Comparison**

Compare multiple DataFrames to identify structural and data differences:

.. code-block:: python

  from valdata import equal_df, equal_df_mult

  # Create a few DataFrames
  df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c']
  })
  df2 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c']
  })

  # Simple comparison
  equal_df(df1, df2)

  # Multiple DataFrame comparison
  dfs_dict = {'Reference': df1, 'Comparison': df2}
  equal_df_mult(dfs_dict, 'Reference')

**Example 3: Concentration Analysis**

Evaluate the concentration of data points above a given threshold:

.. code-block:: python

  from valdata import tblt_concentrations

  df = pd.DataFrame({
    'Scores': [55, 75, 80, 90, 45, 88, 92]
  })

  tblt_concentrations(df, 'Scores', thresholds=[60, 80, 90])

This function provides insight into the distribution of values, helping to identify high or low concentration points.

**Note**

You can import the entire `valdata` package using:

.. code-block:: python

  import valdata as vd

This allows you to access all functions with the `vd.function_name` syntax, so you don't need to import each function individually. This simplifies your code and makes it easier to work with the full suite of `valdata` tools.

Contents
========
.. toctree::
  :maxdepth: 4

  valdata

Further Documentation
=====================
For detailed descriptions and additional usage examples, refer to the function-specific documentation within each module of `valdata`. Additionally, explore our GitHub repository where we provide a comprehensive Jupyter Notebook (jupyter_testing.ipynb). This notebook includes practical examples and showcases the full functionality of valdata in action, helping you to better understand its capabilities and integration with data validation workflows.