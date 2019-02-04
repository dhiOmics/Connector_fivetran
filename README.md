## Connector_fivetran
#### lambda_function.py - AWS lambda function which is zipped along with python packages as "lambda_function.zip"
#### apiResumeUI.py - API gateway for dhiOmics cvClone application to communicate with AWS lambda function
#### databaseOperations.py - Fetch data from MySql database/table as per request received from AWS lamda function and respond as required
#### This AWS function is integrated as AWS_lambda connector for replicating the source table to fivetran managed data warehouse on Bigquery using fivetran(trial version).
