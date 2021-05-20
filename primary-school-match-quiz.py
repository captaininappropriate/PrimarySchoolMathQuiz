#! python
########################################################################
# Author : Greg Nimmo
# Version : 1.0
# Description : this is a mathamatics program for my kids to test 
# how they are progressing with match at school
# negative numbers have been removed to align to what they are learning
# this program will allow you to chose from the four main mathamatics operators
# your session will be saved to a file to allow for review
#######################################################################

# import required modules
import random, os, sys, operator, datetime

# global variables 
maths_list = ['Addition', 'Subtraction', 'Multiplication', 'Division']
maths_dict = {'Addition': '+', 'Subtraction': '-', 'Multiplication': '*', 'Division': '/'}
operatorlookup = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}
correct_answers = 0 # keep track of correct answers
incorrect_answers = 0 # keep track of incorrect answers
total_questions = 0 # used to determine the percentage answered correctly

# set timestamp variables
date_and_time = datetime.datetime.now()
timestamp = date_and_time.strftime("%d/%m/%Y %H:%M:%S")

# create a welcome banner
def START_BANNER():
	heading = 'MATHS QUIZ'
	print(heading.center(40, '-'))

# create a main menu banner
def MAIN_MENU(maths_list):
	print('\nSelect the type of maths to practice, or enter q to quit')
	for item in range(len(maths_list)):
		print('(' + str(item + 1) + ') ' + maths_list[item])
	print('Division is to two decimal places')

# response for invalid menu selection 
def INVALID_OPTION():
	print('\nInvalid option, you must select a valid option')
	
# print the banner
START_BANNER()

# setup a loop for the main menu
while(True):
	MAIN_MENU(maths_list)	
	# get the users name for use in logging
	# check to ensure the user entered their name
	username = input('Enter your name ').split()
	if(not username):
		print('\n[*] ERROR you must enter your name')
		continue
	else:
		pass
	
	# used for logging results to the disk
	log_file_directory = os.path.join('Users', 'Public', 'Documents')
	log_file_name = username[0] + '_maths-quiz-results.txt'	
	path = log_file_directory + '\\' + log_file_name
	
	# check that the user selected option is valid
	selection = int(input('Maths equation to practice : '))
	try:
		selection in maths_list
	except Exception as e:
		INVALID_OPTION
		
	# check that the value supplied exists in the maths_list
	if((int(( selection - 1) in range(len(maths_list))))):
		# this could be compressed into fewer lines  but is more readable this way
		# set the correct index value by subtracting 1 from the current value
		maths_operator_index = selection - 1
		# assign the value of the list item to a variable 
		maths_function = maths_list[maths_operator_index]
		# check the value is a valid key in the dictionary
		if(maths_function in maths_dict):
			# get the correct operator from the dictionary 
			maths_operator = maths_dict[maths_function]
			# set the operation type based on what is in the dictionary
			set_maths_operator = operatorlookup.get(maths_operator)
			# ask the user to the upper most value for the maths function
			try:
				highest_value = int(input('\nEnter the high value to perform the calculation : '))
			except ValueError:
				print('\nYou must enter a numerical value')
				continue
			
			# create a loop to run the maths questions using the current operator until the user decides to quit
			while(True):
				# randomally choose the questions
				first_value_temp = random.randint(1,highest_value)
				second_value_temp = random.randint(1,highest_value)
				
				# ensure that the largest number is on the left of the equasion so there is no negative equasions
				# if the values are the same assign the variables and continue
				if(first_value_temp == second_value_temp):
					first_value = first_value_temp
					second_value = second_value_temp
				# if the second value is larger than the first set the second value to the left
				elif(second_value_temp > first_value_temp):
					first_value = second_value_temp
					second_value = first_value_temp
				else:
					continue
				
				# calculate the answer and save with two decimal places
				correct_value = round(set_maths_operator(first_value, second_value),2)
				
				# print the question for the user
				response = (input('What is ' + str(first_value) + ' ' + str(maths_operator) + ' ' + str(second_value) + ' ? (or type \'q\' to quit) '))
				
				# check to see if the user was correct and test for zero division error
				try:
					if(response[0].upper() == 'Q'):
						# notify the user of the saved results
						print('\nYour sessions results have been written to ' + path)
						# exit back to the main menu
						break
					elif(float(response) == correct_value):
						result = 'Correct' # used for logging purposes
						correct_answers += 1 # increment the correct answer counter
						print('\nCongratulations that is correct\n')
					else:
						result = 'Incorrect' # used for logging purposes
						print('\nThat is incorrect. The correct answer was ' + str(correct_value) + '\n')
						incorrect_answers += 1 # incremented the incorrect answer counter
				except ZeroDivisionError:
					pass
				
				# increment the total questions counter
				total_questions += 1 
				
				# check the directory exists
				if(os.path.isdir('C:\\' + log_file_directory)):
					os.chdir('C:\\' + log_file_directory)
					
					# check if answers were correct or not and append log as appropiate
					# if the answer is correct
					if(float(response) == correct_value):
						with open(log_file_name, 'a') as file_handle:
							file_handle.write(timestamp + '\t' + str(first_value) + ' ' + maths_operator + ' ' + str(second_value) + ' = ' + str(response) + '\t' + result + '\n')
					# if the answer is incorrect
					else:
						with open(log_file_name, 'a') as file_handle:
							file_handle.write(timestamp + '\t' + str(first_value) + ' ' + maths_operator + ' ' + str(second_value) + ' = ' + str(response) + '\t' + result + ', the correct answer is ' + str(correct_value) + '\n')
		
                # error if path does not exist 
				else:
					print('\n[*] ERROR: ' + log_file_directory + ' does not exist')
	
	# invalid main menu option
	else:
		INVALID_OPTION()
		
	# print percentage correct to two decimal places
	total_correct = ((correct_answers / (correct_answers + incorrect_answers)) * 100)
	print('\nYou got ' + str(round(total_correct,2)) + '% correct')
	
	# check if user wants to quit the program
	quit_program = input('\nEnter \'Y\' to quit or \'N\' for the main menu : ')
	if(quit_program[0].upper() == 'Y'):
		# inform the user of their session details and quit the program
		print('\nGoodbye')
		sys.exit()
	else:
		continue
