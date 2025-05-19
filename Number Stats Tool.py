"""✅ Q5 – Number Stats Tool
🕐 Estimated time: 30–45 mins
📚 Teaches: Lists, built-in functions, user-defined functions, formatting, modular code

❓Task:
Write a program that:

Lets the user enter numbers until they type "done".

Stores all numbers in a list.

Then calculates:

Average

Max

Min

Median (write your own function!)

Standard deviation (optional challenge)

Print results in a neat format.

🔑 Concepts:
while True: and break

Type casting and error handling (try...except)

sum(), max(), min()

Sorting and indexing for median

"""
nums = []
i=0
maxNum = -99999
minNum = +99999
sNum = 0
print("Please input all the numbers you want 1 by 1. Type DONE when tou are finished ")
aNum = input("Input number: ")

while aNum != "DONE":
    try:
        aNum = int(aNum)
        nums.append(aNum) #List assignment index out of range
        if aNum < minNum:
            minNum = aNum
        if aNum > maxNum:
            maxNum = aNum
        i +=1
    except:
        print("That is not a number nor DONE")
    aNum = input("Input number: ")
avgNum = sum(nums)/i
nums.sort()
medianNum= nums[int(i/2)]
print(nums)
print("The highest number was: ", maxNum)
print("The lowest number was: ", minNum)
print("The average was :",avgNum)
print("The median was: ", medianNum)