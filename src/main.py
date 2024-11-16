#!/usr/bin/env python3


# Importing external libraries
import configparser
from datetime import datetime
from typing import Dict
import pandas as pd
import os
from pandas.core.arrays.datetimelike import Union
import pyfiglet
import numpy as np
import colorlog as logging
# Importing internal libraries
import distance_calculator
import formatter
import student_filter
import normalization_calculator
import outlier_calculator
import formatter
import student_matcher
import report
import validator


def main():
  logging.basicConfig(level=logging.INFO)
  # figlet name
  custom_fig = pyfiglet.Figlet(font='standard')
  print(custom_fig.renderText('ESN Buddy Matcher'))

  output_dir: str = 'output'


  # Load the data
  local_students: pd.DataFrame = pd.read_csv("/input/local_students.csv", skipinitialspace=True)
  logging.info("Local students loaded [%s]", local_students.shape)

  incoming_students: pd.DataFrame = pd.read_csv("/input/incoming_students.csv", skipinitialspace=True)
  logging.info("Incoming students loaded [%s]", incoming_students.shape)

  local_students_schema: pd.DataFrame = pd.read_csv("/config/local_students_schema.csv",skipinitialspace=True)
  logging.info("Local students schema loaded [%s]", local_students_schema.shape)

  incoming_students_schema: pd.DataFrame = pd.read_csv("/config/incoming_students_schema.csv",skipinitialspace=True)
  logging.info("Incoming students schema loaded [%s]", incoming_students_schema.shape)



  local_students , incoming_students = formatter.validate_and_format_data(local_students, incoming_students, local_students_schema, incoming_students_schema)

  print("local student columns: ", local_students.columns)
  print("incoming student columns:", incoming_students.columns)


if __name__ == '__main__':
  main()
