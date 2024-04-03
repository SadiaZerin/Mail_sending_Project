

1. Created the environment.The application is set up using Flask and named the project Rest_API_project
   
2. The POST/register endpoint allows users to register by providing their email, first name, and last name. If the provided email already exists in the database, it     returns a 409 Conflict error. Otherwise, it adds the user to the database and enqueues a task to send a welcome email asynchronously.
   
3. The DELETE/user/<int:user_id> endpoint allows users to be deleted from the database based on their ID as well as GET/user/<int:user_id> to get the user.
   
4. Email sending is handled asynchronously using a task queue. When a user registers, a task is enqueued to send a welcome email to the user's email address. The create_email_message function constructs the email message with a personalized greeting using the user's first and last names. The send_email function sends the constructed email message using the Gmail API.

5. The create_email_message function is executed asynchronously in the background to send emails to users. It constructs personalized email messages and passes them to the send_email function for sending.

7. The application integrates with the Gmail API to send emails. It uses the googleapiclient library to build the Gmail service and send emails using OAuth2 authentication.

8. The application uses environment variables or configuration files (such as token.json) to store sensitive information like Gmail API credentials.

9. The Docker Compose file defines a service named 'web', which will build an image using the Dockerfile in the current context and run it.

10. The 'ports' section maps port 80 of the container to port 80 of the host machine, allowing access to the Flask application running inside the container from the host.
11. validate_email will check if the email is valid or not.
12. Docker compose yml file will run build and run three services- web, redis, rq_worker.
