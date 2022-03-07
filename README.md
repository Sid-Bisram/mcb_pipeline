# mcb_pipeline
The purpose of this repository is a requirement for MCB technical assessement.

# Required:
1) Pip  freeze requirements.txt for installing all the necessary libraries
2) Create empty directories reports(to store downloadable reports).
3) Run create statements

Database (Mariadb)
1) The dataconfig.config file should be filled in with the proper details such as host, username, password and db_name
2) Once all the scripts, the database should contain the following:

### tables
tbl_country_region - containing all the country related information
happiness_report_sourcetable -> for storing all the data dumps prior to further processing by stored_proc > transfer_to_maintable <
happiness_report_maintable -> this is the final table that will contain the curated data namely the normalisation of the country field

Note: The reason of using 2 tables is to use the sourcetable as a rollback table should there be any issues such as in a BI architecture.

### functions
1. overall_rank - using ranking for answering question 3
2. rank_per_region - using ranking again for answering question 3

### stored_procedures
1. report_3 - returns full dataset as per question requirement. Proc is called with python codebase question_3.py
2. report_4 - returns full dataset as per question requirement. Proc is called with python codebase question_4.py
3. transfer_to_maintable - stored procedure is used to transfer raw data to final table >happiness_report_maintable<

# how to run codefiles
### 1. Question 1 -> Just run the sql scripts
### 2. Question 2 -> on cmd, run question_2.py
### 3. Question 3 -> on cmd, run question_3.py. User will be prompted for 3 inputs and in the end, the report(csv or parquet) will be downloaded to directory reports in root folder.
### 4. Question 4 -> on cmd, run question_4.py. User will be prompted for 1 input and finally, json file will be donwloaded to reports directory.
### 5. Question 5 -> on cmd, run question_5.py. User will receive a localhost to click whereby they can view the map visualisation.
### 6. Question 6 -> on cmd, run question_6.py. The country records will be updated with their capital, longitude and latitude.

Unfortunately, due to lack of time on my end, i was unable to complete question 5 and 6.
