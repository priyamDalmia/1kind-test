# 1kind-test
1kingd Job Interview test solutions.

# Tasks. 

1. Create, host and launch a postgresql database on AWS.
2. Build a small python app to populate the database with articles scrapped from the web.

# Getting Started. 

# Running the code.

1. Populate the *config.yaml* file with the credentails provided. Once that is completed, run the commands `python3 tests/test_remote_connection.py`. The output should confirm that a succesfull connection has been established. 
2. 




### Debugging.

In case the postgreSQL service is not working use the following commands after logging into the E2C instance to debug: 

1. Check postgresSQL service status using the command: `cd /etc/init.d; ./postgresql status`.
2. That should normally show that the postgreSQL is running on the instance. Somtimes however an instance on E2C might close the running service automatically. If not, use the command: `cd /etc/init.d: ./postgresql restart` to restart the service.
3. Use the previous command again or this command to get a more detailed report of the running postgreSQL service: `systemctl status postgresql@12-main.service`.
4. Finally make sure that postgreSQL is listening at port 5432 using command: `sudo netstat -antup | grep 5432`. I have configured the security groups and setup this port but incase it dosen't work for some reason, contact me and I will set it up again.

###  

