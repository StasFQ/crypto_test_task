
To run the project, follow these steps:

1. Make sure you have Docker and Docker Compose installed.

2. Open the `docker-compose.yml` file and configure the database connection in the `app.environment.SQLALCHEMY_DATABASE_URI` section. Fill in the correct values for the `username`, `password`, `host`, `port`, and `database` parameters.

3. Update the database connection in the `settings/app.py` file. Edit the `SQLALCHEMY_DATABASE_URI` line with the value you used in the `docker-compose.yml` file.

4. In your terminal, navigate to the root folder of the project and run the command: docker-compose up
This command will start the project and bring up the containers for the application and the database.

5. The project will be accessible at http://localhost:5050.

## Documentation

Information about all available endpoints and their parameters can be found in the `docs` folder.

Hours spent on the project: 5
