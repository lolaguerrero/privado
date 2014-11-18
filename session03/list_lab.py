#!/usr/bin/env python

"""List Lab for Session03. 
    PART 1
    Create a list that contains 'Apples', 'Pears', 'Oranges' and 'Peaches'.
    Display the list.
    Ask the user for another fruit and add it to the end of the list.
    Display the list.
    Ask the user for a number and display the number back to the user and the fruit corresponding to that number (on a 1-is-first basis).
    Add another fruit to the beginning of the list using '+' and display the list.
    Add another fruit to the beginning of the list using insert() and display the list.
    Display all the fruits that begin with 'P', using a for loop.

    PART 2
    Display the list.
    Remove the last fruit from the list.
    Display the list.
    Ask the user for a fruit to delete and find it and delete it.
    (Bonus: Multiply the list times two. Keep asking until a match is found. Once found, delete all occurrences.)
"""
fruit_list = ['Apples', 'Pears', 'Oranges', 'Peaches']
print fruit_list

user_fruit1 = raw_input("Tell me your favorite fruit that is not on the list!: ")
fruit_list.append(user_fruit1)
print fruit_list

user_fruit2 = raw_input("Tell me another favorite fruit that is not on the list: ")
fruit_list.append(user_fruit2)
print fruit_list

# not accounting for user entering a non-integer, which causes error in the indexing
user_number = raw_input("Enter a number and I'll tell you the fruit: ")
print "Your number is " + user_number + " and that fruit is " + fruit_list[int(user_number) - 1]
#your solution below is sooo much easier to read!!
#print"Your number is %i and the fruit is %s"%(user_number, fruit_list(user_number-1))

user_fruit3 = raw_input("add another fruit ")
#fruit_list = fruit_list + [user_fruit3] #this adds it to the end, to add it to the beginning using +???
fruit_list.insert(0, user_fruit3) # this adds it using insert, easy!
print fruit_list

for fruit in fruit_list: #this will print the fruits on separate lines, in real world would put on the same line
    if fruit[0].lower() == 'p': 
        print fruit

#####################################
#####################################
print fruit_list
fruit_list.pop()
print fruit_list
user_remove = raw_input("Which fruit do you want to remove? ")
fruit_location = fruit_list.index(user_remove)
fruit_list.pop(fruit_location)
print fruit_list

#Bonus
fruit_list = fruit_list * 2
print fruit_list
# fruit_list.remove(user_remove)
# print fruit_list
for fruit in fruit_list[:]:
    if fruit == user_remove:
        fruit_list.remove(user_remove)
print fruit_list


