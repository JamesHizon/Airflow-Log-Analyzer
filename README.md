# Airflow Log Analyzer Mini-Project

This mini-project will be used to monitor the statust of various jobs inside my pipeline on a regular basis after scheduling a DAG object in Airflow. In order to monitor the job status, I will be analyzing the log messages generated from each run.

The log analyzer should show the following information:
- Total count of error messages
- A detailed message regarding each error.

### Learning Objectives
- Use text processing techniques in Python to make sense of logs.
- Learn where logs are located in Airflow.
- Learn how to monitor automated Airflow DAGs to ensure they are working properly.

### Dependencies
In order for me to complete this Airflow Mini-Project, I need to run Airflow on Docker provided through folder from Springboard mentor. In order for me to view the log analyzer information on log error messages, I need to execute ```docker exec -it airflow sh``` inside the ```springboard-airflow``` folder provided. Then, I need to manually seek out the ```marketvol``` folder and observe folder with task_id ```print_TSLA_log_error``` and ```print_AAPL_log_error```.

### Other Key Information
Inside the analyze_file() function, I mainly iterate through a specified log file path. I use regular expressions to obtain all log files using ```.rglob("*.log")```. Based on Airflow configuration settings, the log file name depends on the task_id, so I needed to make sure that both ```TSLA``` and ```AAPL``` appear in the log file name to obtain error message and error count for both stock_tickers.

### Sample
See screenshot to view example of log analyzer file inside terminal. For most of the log files, there are no error messages which means that the DAG seems to run without much error.

### Order of Tasks
t1 >> t2

t3 >> t4
