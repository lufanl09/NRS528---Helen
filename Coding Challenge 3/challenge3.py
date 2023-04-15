######################
# Coding Challenge 3 #
######################

### PART 1. Simple Directory Tree
#start by importing os package
import os

#create directory tree
os.mkdir("C:\draft_code")
os.mkdir("C:\draft_code\pending")
os.mkdir("C:\draft_code\complete")

os.mkdir("C:\includes")

os.mkdir("C:\layouts")
os.mkdir("C:\layouts\default")
os.mkdir("C:\layouts\post")
os.mkdir("C:\layouts\post\posted")

os.mkdir("C:\site")

#delete directory tree
os.removedirs("C:\draft_code\pending")
os.removedirs("C:\draft_code\complete")

os.removedirs("C:\includes")

os.removedirs("C:\layouts\default")
os.removedirs("C:\layouts\post\posted")

os.removedirs("C:\site")



### PART 2. Push sys.argv to the limit
import sys

# first we need to create a batch file
argument1 = sys.argv[1]
argument2 = sys.argv[2]
argument3 = sys.argv[3]

argument_list = [argument1, argument2, argument3]
counter = 1

for i in argument_list:
    print("I have " + str(counter) + " " + str(i))
    counter = counter + 1



### PART 3. Working with CSV
import csv

# 1. Annual average for each year in the dataset
# split and create list of all years

year_list = []  # check all unique years
num_in_year = []  # count how many times the year shows up
sum_in_year = []
counter = -1
with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        date = row[0]
        month, day, year = date.split("/")
        if year in year_list:
            num_in_year[counter] = num_in_year[counter] + 1  # counter is telling you where you are
            sum_in_year[counter] = float(sum_in_year[counter]) + float(row[1])

        if year not in year_list:
            year_list.append(year)
            num_in_year.append(1)
            sum_in_year.append(float(row[1]))
            counter = counter + 1

print(year_list)
print(sum_in_year[0])

# calculate average per year
avg_per_year = []
for i in range(0, len(sum_in_year)):
    avg_per_year.append(float(sum_in_year[i]) / float(num_in_year[i]))
print(avg_per_year)

# 2. Minimum, maximum and average for the entire dataset.
# generate value column as a list
value_list = []
with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        value_list.append(float(row[1]))
print(value_list)
print(min(value_list))
print(max(value_list))
sum_list = sum(value_list)
average = sum_list / (int(len(value_list)))
print(average)

# 3. Seasonal average if Spring (March, April, May),
# Summer (June, July, August), Autumn (September, October, November)
# Winter (December, January, February).
spring = []
summer = []
autumn = []
winter = []

with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        date = row[0]
        value = row[1]
        month, day, year = date.split("/")

        if (int(month) == 3) or (int(month) == 4) or (int(month) == 5):
            spring.append(float(value))
        if (int(month) == 6) or (int(month) == 7) or (int(month) == 8):
            summer.append(float(value))
        if (int(month) == 9) or (int(month) == 10) or (int(month) == 11):
            autumn.append(float(value))
        if (int(month) == 12) or (int(month) == 1) or (int(month) == 2):
            winter.append(float(value))

spring_avg = sum(spring) / len(spring)
print(spring_avg)

summer_avg = sum(summer) / len(summer)
print(summer_avg)

autumn_avg = sum(autumn) / len(autumn)
print(autumn_avg)

winter_avg = sum(winter) / len(winter)
print(winter_avg)

# 4. Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.
# anomaly = mean - value
anomaly_list = []
with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        anomaly_list.append(average - float(row[1]))

print(anomaly_list)







