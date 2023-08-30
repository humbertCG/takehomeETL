#Author: Humberto Carrillo 
#Date 29/8/2023

import sqsFunctions as sqf #Import the custom module for executing sqs functions
import postgreFunctions as pgf #Import the custom module for executing postgre functions
import sys

#Main file of the program 

def main(): 

    #If the program is run after the queue has been depleted or if there are no messages
    if sqf.get_approximate_number_of_messages()  == 0: 
        print('No more messages waiting at the queue')
        sys.exit()

    else:
        #Since sqs is limited to a max of 10 messages per request, requests must be sent continuously
        while sqf.get_approximate_number_of_messages() > 0:  #If there are messages left
            message_list = sqf.receive_messages() #retrieve them
            sqf.process_message_list(message_list) #process them
        
    pgf.closeConnection() #close the handler
    print('----------------------------Successfully processed and inserted messages-------------------------------------')

    

if __name__ == "__main__":
    main()