# takehomeETL
Humberto Carrillo's submission for the FETCH Takehome
29/8/2023

<hr>

## Thought process Description 

For this takehome, I decided to use the python programming language because it makes it easy to interact with databases, it also saved me a lot of time with its boto3 library for connecting to sqs. I already knew how to interact with PostgreSQL databases and had knowledge about sqs however, I had never tried to connect to sqs using python, therefore I read the documentation and became familiar with the boto3 library which is the official library provided by Amazon to interact with sqs. After reading the documentation almost all the initial questions about how I would program the solution for the take-home disappeared, some of these questions were: how many messages can I retrieve from sqs at the same time? What are the credentials needed for logging in? How will the retrieved messages be structured? Before starting to code I thought about using an object-oriented approach however, since the only relevant objects here were messages, (excluding connection handlers for postgreSQL) I decided to focus more on using a mixture of functional and declarative programming. 
Out of the whole process, the most entertaining part for me was thinking about how to mask the PII. Out of the blue I remembered my cybersecurity classes in college and hashes came to mind because one rule of hashing algorithms is that the same input always yields the same output. 
After reading the documentation, remembering how to mask the PII, and deciding which approach to use, coding was straightforward. I tried to make my code as robust as possible however, due to time constraints I could only make tests on the fly with the provided dataset; I would have really liked being able to make tests with other datasets and having the opportunity to develop more robust unit tests nevertheless, I think that the solution works really well and I had a lot of fun while programming it.

<hr>

## Takehome questions and answers

● How would you deploy this application in production?

I would use an EC2 instance to deploy this application in a production environment and to also deploy the postgreSQL server, in the future this EC2 could be notified by a webhook whenever new messages are received in SQS and automatically insert them into the db. While deploying it I would use a Devops methodology to overcome challenges like slow delivery and lack of communication between development and 
operation teams. Regarding security I would create environment variables for all sensible info before deploying. 
  
● What other components would you want to add to make this production ready?

I think that a webhook or a lambda function that automatically updates the db whenever there is a new message on the sqs would be critical for this application's success. It would save a lot of time and no people would be required to run the program on a computer. 

Another thing that I would like to do would be to extensively test the functions that I developed and to refactor whenever possible to create a more robust code.

● How can this application scale with a growing dataset.

Currently the application spends about 4 seconds processing a hundred messages. This might seem fast but obviously FETCH handles much more information perhaps millions of information so when taking about large queues, I think it would struggle. However, since the sqs documentation sheds some light on the possibility of multiple users accessing the queue, I think that to scale the application, it would be a great idea to use multithreading: this would make the application faster and help it to cope with the increasing overhead of having to wait before processing the next message batch.

● How can PII be recovered later on?

Since the method that I used (SHA256) for encrypting the PII is non-reversible, I would suggest creating a secondary table on the db that includes the PII without hashing however, this table would be restricted to only the users that need the PII to perform their jobs e.g., analysts, managers. 

● What are the assumptions you made?
I assumed that the database's schema had to be respected and therefore, I did not modify it even though I think it would be a better idea to store the app version in a Varchar field because if you store it as an integer, distinguishing between major version, minor version, and patch becomes quite hard.

 
