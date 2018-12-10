def activityBuddies(ratings):
    num_students = len(ratings)
    num_activities = len(ratings[0])
    available = set(range(num_students))
    num_allocated = [0]  * num_activities
    chosen_act = [0]  * num_students
    score = 0
    while available:
        black_list = []
        num_required = sum([2-i if i<2 else 0 for i in num_allocated])
        if len(available) <= num_required:
            black_list = [i for i in range(len(num_allocated)) if num_allocated[i] >= 2]
            if black_list:
                print('\tblack=', black_list)
        
        max_actitvity = None
        max_student = None
        max_added_fun = None
        for student in available:
            act_for_student = [(i,ratings[student][i]) for i in range(num_activities) if not i in black_list]
            sorted_act_for_student = sorted(act_for_student, key=lambda x:x[1], reverse=True)
            added_fun = sorted_act_for_student[0][1] - (sorted_act_for_student[1][1] if len(sorted_act_for_student)>1 else 0)
            if not max_added_fun or max_added_fun < added_fun:
                max_added_fun = added_fun
                max_student = student
                max_actitvity = sorted_act_for_student[0][0]
                if max_added_fun == 0 and len(sorted_act_for_student)>1: # choosing least index between two equal activities
                    max_actitvity = min(sorted_act_for_student[0][0], sorted_act_for_student[1][0])
        
        print('st=', max_student, ', act=', max_actitvity, ',add=', max_added_fun)

        score += ratings[max_student][max_actitvity]
        available.remove(max_student)
        num_allocated[max_actitvity] += 1
        chosen_act[max_student] = max_actitvity

    print(score, ' = ', chosen_act)

    return num_allocated

def activityBuddies2(ratings):
    score = [0]
    result = [[0]]

    num_students = len(ratings)
    num_activities = len(ratings[0])

    allocation = [0] * num_students
    activities = [0] * num_activities
    
    def allocate(student, new_score):
        if student == num_students:
            if new_score > score[0]:
                score[0] = new_score
                result[0] = activities.copy()
                print(allocation)
            return
        else:
            num_required = sum([2-i if i<2 else 0 for i in activities])
            white_list = range(num_activities) if num_students-student > num_required else [i for i in range(num_activities) if activities[i] < 2]
            for i in white_list:
                allocation[student] = i
                activities[i] += 1
                allocate(student+1, new_score + ratings[student][i])
                activities[i] -= 1

    allocate(0, 0)
    print(score[0], ' = ', result[0])
    return result[0]

def activityBuddies3(ratings):
    num_students = len(ratings)
    num_activities = len(ratings[0])
    
    allocation = [0] * num_students
    activities = [0] * num_activities
    score = 0
    
    #iniital allocation
    for i in range(num_students):
        max_score = max(ratings[i])
        score += max_score
        max_actitvity = ratings[i].index(max_score)
        allocation[i] = max_actitvity
        activities[max_actitvity] += 1
    print(score, ' = ', allocation)

    #worsening off initial solution
    while min(activities) < 2:
        fixing_activitiy = activities.index(min(activities))
        score_adj = -score
        switch_student = -1
        for i in range(num_students):
            if allocation[i] < 0 or allocation[i] == fixing_activitiy: # skip the ones we switch already
                continue
            new_score_adj = -ratings[i][allocation[i]] + ratings[i][fixing_activitiy] 
            if score_adj < new_score_adj:
                score_adj = new_score_adj
                switch_student = i
        activities[allocation[switch_student]] -= 1
        allocation[switch_student] = -fixing_activitiy-10
        activities[fixing_activitiy] += 1
        score += score_adj
        print(score, ' = ', allocation)

    return activities         

def calcScore(ratings, choosen):
    score = 0
    for i in range(len(choosen)):
        score += ratings[i][abs(choosen[i])]
    return score


# input = [[10,4], [10,9], [9,10], [8,9], [3,3]]
input = [[6,9,6,4], 
 [6,8,6,9], 
 [2,9,8,9], 
 [7,2,7,9], 
 [1,2,2,1], 
 [4,1,4,3], 
 [6,2,1,7], 
 [5,5,4,8], 
 [6,8,5,5], 
 [7,2,6,2]]

# allocations = generateAllocations(input)
# print(len(allocations))
print(activityBuddies3(input))
better = [1, 3, 1, 3, 2, 2, 0, 3, 1, 0]
print(calcScore(input, better), ' = ', better)
print([better.count(i) for i in range(len(input[0]))])
