from pulp import *
import time

jobs = ["J1","J2","J3","J4","J5"] #list to keep the name of jobs
processing = {"J1":2,"J2":2,"J3":1,"J4":3,"J5":3} #dictionary for jobs' processing time
due = {"J1":3,"J2":3,"J3":3,"J4":9,"J5":4} #dictionary for jobs' due date
periods = range(sum(processing.values())) #all time slots for the machine scheduling

combinations = [(j,p) for j in jobs for p in periods] #all legal combinations for "job-time slot" allocation

late_check = {j:{periods:0 for periods in periods} for j in jobs} #dict that keeps whether job is late if job j starts at period p 

for i in late_check: #Constraint for every job to start only once.
    for j in late_check[i].keys():
        if j + processing[i] > due[i]:
            late_check[i][j] = 1 

prob = LpProblem("Single Machine Scheduling", LpMinimize) #Defining the problem
jobs_var= LpVariable.dicts("Jobs",(jobs,periods),cat="Binary") #Defining the variable


prob +=lpSum([jobs_var[j][t] * late_check[j][t] for (j,t) in combinations]) #Objective Function.



for j in jobs:
    count = 0
    for i in range(max(periods)-processing[j]+2):
        count += jobs_var[j][i]  
    prob += lpSum(count) == 1 #Constraint for every job to be start once.

for t in periods:
    prob += lpSum((sum(jobs_var[j][p] for j in jobs for p in range(max(0,t-processing[j]),t)))) <= 1
    
    
    
start = time.time()
status = prob.solve()
end = time.time()

LpStatus[status]

print(prob)
print("Number of late job is " + str(value(prob.objective)))
print("Overall solving time for alternative formulation is " + str(end-start))

for j in jobs:
    for p in periods:
        if (j,p) in combinations:
            if value(jobs_var[j][p]) == 1:
                print(str(j) + " "+ str(p) + " "+ str(value(jobs_var[j][p])))