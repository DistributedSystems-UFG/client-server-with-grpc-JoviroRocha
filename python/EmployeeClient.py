from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

def goodbye():
  print("  .--.      .-'.      .--.      .--.      .--.      .--.      .`-.      .--.\n" +
       ":::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\n" +
       "'      `--'      `.-'      `--'      `--'      `--'      `-.'      `--'      `")
  print("\n                GOODBYE! HOPE TO SEE YOU AGAIN\n")
  print("  .--.      .-'.      .--.      .--.      .--.      .--.      .`-.      .--.\n" +
      ":::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\n" +
      "'      `--'      `.-'      `--'      `--'      `--'      `-.'      `--'      `\n\n")

def welcome():
  print("  .--.      .-'.      .--.      .--.      .--.      .--.      .`-.      .--.\n" +
       ":::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\n" +
       "'      `--'      `.-'      `--'      `--'      `--'      `-.'      `--'      `")
  print("\n                WELCOME TO THE LIST MANAGER!\n")
  print("  .--.      .-'.      .--.      .--.      .--.      .--.      .`-.      .--.\n" +
      ":::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\n" +
      "'      `--'      `.-'      `--'      `--'      `--'      `-.'      `--'      `\n\n")
  return menu()

def menu():
  return input("CHOOSE THE OPTION THAT BEST FITS YOUR NEEDS:\n1 - PRINT THE ENTIRE LIST.\n2 - SEARCH FOR A VALUE IN THE LIST.\n3 - ADD A VALUE TO THE LIST.\n" +
              "4 - APPEND ANOTHER LIST TO THE LIST. \n5 - REMOVE A VALUE FROM THE LIST. \n6 - SORT THE LIST \n0 - EXIT THE LIST MANAGER\n")

def run():
    with grpc.insecure_channel(const.IP+':'+const.PORT) as channel:
        stub = EmployeeService_pb2_grpc.EmployeeServiceStub(channel)
        x = welcome()
        while(x != '0'):
            # Print the entire list
            if x == '1':
                response = stub.ReturnList(EmployeeService_pb2.EmptyMessage())
                print (str(response), '\n')   
            # Search a value in the list
            elif x == '2':
                try:
                    data = float(input("Enter the data you want to search for: "))
                except ValueError:
                    print("The value must be a decimal number, try again!\n")
                    continue
                if str(stub.SearchValue(EmployeeService_pb2.Value(number=data))) == "status: \"OK\"" :
                    print("The value is in the list!\n")
                else: 
                    print("The value is NOT in the list!\n")
            # Add a single value to the list
            elif x == '3':
                try:
                    data = float(input("Enter the data you want to add to the list: "))
                except ValueError: 
                    print("The value must be a decimal number, try again!\n")
                    continue
                response = stub.InsertValue(EmployeeService_pb2.Value(number=data))
                if (str(response) == "status: \"OK\""):
                    print("All done! The value has been inserted!\n")
                else:
                    print("An error ocurred! Try again\n")
            # Append a list to the list
            elif x == '4':
                data = []
                try:
                    number_elements = int(input("Number of elements in the list: "))
                except ValueError:
                    print("The value must be a decimal number, try again!\n")
                    continue
                print("Enter the values from the list that you want to append: - Each value separated by an 'Enter'\n")
                for i in range(0, number_elements):
                    try:
                        print("Value ", (i + 1), ": ")
                        l = float(input())
                    except ValueError:
                        print("An error has occurred! The value must be a decimal number! \nThe program is exiting... Try again!\n")
                        exit(1)
                    data.append(l)
                    for values in data:
                        response = stub.InsertValue(EmployeeService_pb2.Value(number=values))
                print("All done! The list has been concatenated!\n")
            # Remove a value from list
            elif x == '5':
                try:
                    data = float(input("Enter the value you want to remove from the list: "))
                except ValueError:
                    print("The value must be a decimal number, try again!\n")
                    continue
                while str(stub.ReturnList(EmployeeService_pb2.Value(number=data))) == "status: \"OK\"":
                    response = stub.RemoveValue(number=data)
                print("All done! The value has been removed!\n")
            # Sort the list
            elif x == '6':
                order = input("Type \"ascending\" to sort the list in ascending order or type \"descending\" to sort the list in descending order: ")
                while (order != "ascending" and order != "descending"):
                    print("Wrong value! Try again!\n")
                    order = input("Type \"ascending\" to sort the list in ascending order or type \"descending\" to sort the list in descending order: ")
                if order == "ascending":
                    response = stub.SortAscending(EmployeeService_pb2.EmptyMessage())
                    print("Done! The list was sorted in ascending order! \n")
                else:
                    response = stub.SortDescending(EmployeeService_pb2.EmptyMessage())
                    print("Done! The list was sorted in descending order!\n")
            # Enter a invalid value
            else: 
                print("You enter an invalid option! Let's try again.\n")
            x = menu()
        goodbye()

if __name__ == '__main__':
    logging.basicConfig()
    run()