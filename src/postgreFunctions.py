#Author: Humberto Carrillo 
#Date 29/8/2023

import psycopg2
import datetime




#In a production environment it would be required to use environment variables for sensible info however, since this app will be running locally and not everyone has access
#to the db image, no environment variables were used.
handler = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")



def createTuple(customerData: dict):
     
     cursor = handler.cursor()
     
     statement = 'INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s);'

     data = (customerData['user_id'], customerData['device_type'], customerData['masked_ip'], customerData['masked_device_id'], customerData['locale'], 
             int(customerData['app_version']), datetime.date.today())
     
     cursor.execute(statement, data)

     cursor.close()

     handler.commit()


def closeConnection():
     handler.close()
