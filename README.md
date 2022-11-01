# products_categories_project
test task for the interview

![image](https://user-images.githubusercontent.com/40138357/199266070-225d8a3b-d2b5-45ec-a483-8ff4203b583a.png)

The project contains a docker-compose.yaml file that allows you to deploy the system from two containers. The first container is a postgreSQL database, which is initialized with test data in the init.sql script. The second container implements a service based on HTTP API library FastAPI and ORM SQLalchemy. The code is implemented in asynchronous style.

When deploying containers in the project folder creates a folder /logs, which contains the execution logs and the folder /pd_data, which implements persistence

Access to the service is via port 5050 on localhost
