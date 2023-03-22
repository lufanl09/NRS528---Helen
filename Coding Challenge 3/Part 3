# 3. Working with CSV

import csv
import os

###1. Annual average for each year in the dataset
#split and create list of all years

year_list = []   #check all unique years
num_in_year = [] #count how many times the year shows up
sum_in_year = []
counter = -1
with open("co2-ppm-daily.csv") as co2_csv:
   next(co2_csv)
   for row in csv.reader(co2_csv):
       date = row[0]
       month, day, year = date.split("/")
       if year in year_list:
           num_in_year[counter] = num_in_year[counter] + 1    #counter is telling you where you are
           sum_in_year[counter] = float(sum_in_year[counter]) + float(row[1])
        
       if year not in year_list:
           year_list.append(year)
           num_in_year.append(1)
           sum_in_year.append(float(row[1]))
           counter = counter + 1 

print(year_list)
print(sum_in_year[0])

#calculate average per year
avg_per_year = []
for i in range(0, len(sum_in_year)):
    avg_per_year.append(float(sum_in_year[i])/float(num_in_year[i]))
print(avg_per_year)



###2. Minimum, maximum and average for the entire dataset.
#generate value column as a list
value_list = []
with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        value_list.append(float(row[1]))
print(value_list)
print(min(value_list))
print(max(value_list))
sum_list = sum(value_list)
average = sum_list/(int(len(value_list)))
print(average)



###3. Seasonal average if Spring (March, April, May),
### Summer (June, July, August), Autumn (September, October, November)
### Winter (December, January, February).
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
            
        
spring_avg = sum(spring)/len(spring)
print(spring_avg)

summer_avg = sum(summer)/len(summer)
print(summer_avg)

autumn_avg = sum(autumn)/len(autumn)
print(autumn_avg)                             

winter_avg = sum(winter)/len(winter)
print(winter_avg)



###4. Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.
#anomaly = mean - value
anomaly_list = []
with open("co2-ppm-daily.csv") as co2_csv:
    next(co2_csv)
    for row in csv.reader(co2_csv):
        anomaly_list.append(average - float(row[1]))
        
print(anomaly_list)
