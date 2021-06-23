# Log Analyzer Second Attempt

# Steps:
# 1) Locate log files for application.
# 2) Create log analyzer in Python.

# Note:
# - Each log message follows a standard format. Each log entry starts with a datetime
# and the code line number, followed by the message types (INFO, WARNING, ERROR, etc.)

# Goal of Python script:
# - To report total number of errors and associated error messages.

# Note:
# - Airflow XCom stands for "cross-communication" and allows exchange of messages
# or small amount of data between tasks.
# - You can think of an XCom as a little object w/ the following fields:
# that is stored IN the metadata database of Airflow.

# Q: What is XCom push and pull in Airflow?
# - XCom push/pull just adds/retrieves a row from the XCom table in the airflow DB
# based on DAG id, execution date, task id, and key.

# Imports
import os
from datetime import date, timedelta, datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Initialize log folder path (Recall "docker exec -it airflow sh" to log into docker-airflow.)
LOG_PATH = "/opt/airflow/logs/marketvol"


# Create Python method to parse each file
def analyze_file(**kwargs):
    """
    Use this method to parse each log file.

    Next:
    - Edit code s.t. I will properly deal with directory (see terminal).

    :param kwargs:
    :return: Total count of error entries from this file. A list of error message details
    (the errors themself).
    """
    # Create log_path and stock symbol variables from kwargs input
    log_path = kwargs["log_path"]
    symbol = kwargs["stock_ticker"]

    # Iterate through log_path directory to get all log files w/ ".log" extension as list.
    log_file_list = Path(log_path).rglob("*.log")

    # Initialize empty error message list and create list of log files object
    error_list = []
    logfile_list = list(log_file_list)

    # Iterate through each log file
    for file in logfile_list:
        file_str = str(file)
        # Filter out and open only files that have "marketvol" or stock "symbol" in file string
        if file_str.find("marketvol") != -1 and file_str.find(symbol) != -1:   # TODO: Edit this part of Python script.
            log_file = open(file_str, "r")
            # Iterate through each line in log_file to see if "ERROR" msg exists (if so, append)
            for line in log_file:
                if "ERROR" in line:
                    error_list.append(line)

    # Think:
    # - How am I to filter through AAPL and TSLA log files?

    # Locate task_instance --> This will automatically be created as task is being run
    task_instance = kwargs["task_instance"]
    task_instance.xcom_push(key="error_count", value=len(error_list))
    task_instance.xcom_push(key="errors", value=error_list)


# Python operators should call the analyze_file() function.
# Name the operators t1 and t3 for the symbols AAPL and TSLA respectively.
# Also, I will use BashOperators to print out error messages and total count.

# Define default_args
default_args = {
    'owner': 'admin2',
    'start_date': datetime(2021, 6, 20)
}

# Create templated commands for BashOperator argument to print error count and list errors
# for both TESLA and APPLE stocks market data (see key = "error_count", "errors").

templated_command1 = """
    echo -e "total error count:" {{ task_instance.xcom_pull(task_ids='tsla_log_errors', key='error_count') }} "\n
    List of errors for TESLA:" {{ task_instance.xcom_pull(task_ids='tsla_log_errors', key='errors') }} 
"""

templated_command2 = """
     echo -e "total error count:" {{ task_instance.xcom_pull(task_ids='aapl_log_errors', key='error_count') }} "
     \nList of errors for APPLE:" {{ task_instance.xcom_pull(task_ids='aapl_log_errors', key='errors') }} 
"""


# Initialize DAG
with DAG(dag_id='log_analyzer',
         default_args=default_args,
         description="Simple DAG on Stock Market volume data",
         schedule_interval="* * * * *"  # Formerly used "@daily".
         ) as dag:

    t1 = PythonOperator(
        task_id="TSLA_log_errors",
        python_callable=analyze_file,
        provide_context=True,
        op_kwargs={'stock_ticker': 'TSLA', 'log_path': LOG_PATH}
    )

    t2 = BashOperator(task_id="print_TSLA_log_error",
                      bash_command=templated_command1)

    t3 = PythonOperator(
        task_id="AAPL_log_errors",
        python_callable=analyze_file,
        provide_context=True,
        op_kwargs={'stock_ticker': 'AAPL', 'log_path': LOG_PATH}
    )

    t4 = BashOperator(task_id="print_AAPL_log_error",
                      bash_command=templated_command2)

t1 >> t2
t3 >> t4


