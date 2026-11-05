Hacker News Pipeline

This is a project for Data Engineering, which I'm learning on the go. The python script collects Data from the official Hacker News Source. 

For the first version, I have used systemd for triggering the python script for every 15 minutes. The second version will use Airflow. 

Postgres is used as the Database and Grafana is used for showing a dashboard. Both are used as Docker Containers. I have created a Docker-compose file which you can run with docker compose up -d. Grafana runs on localhost:3000

This is my first time working on these so, I would appreciate any feedback
