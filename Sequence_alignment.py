import time, math
import sys
import tracemalloc
# import time

def generateStrings(filename):
    with open(filename, 'r') as f:
        base_str1 = f.readline().strip()
        base_str2 = ''
        lines = f.readlines()
        
        base_str1_generation_indices = []
        lineIdx = 0
        for line in lines:
            if line.strip().isdigit():
                base_str1_generation_indices.append(int(line))
                lineIdx += 1
            else: 
                base_str2 = line.strip()
                lineIdx += 1
                break
        
        base_str2_generation_indices = []
        for i in range(lineIdx, len(lines)):
            base_str2_generation_indices.append(int(lines[i]))


    str1 = generator(base_str1, base_str1_generation_indices)  
    str2 = generator(base_str2, base_str2_generation_indices) 
    return str1, str2


def generator(base_string, base_string_generation_indices):
    for idx in base_string_generation_indices:
        base_string = base_string[:idx+1] + base_string + base_string[idx+1:]
    return base_string

print(generateStrings('input2.txt'))

def mismatch_penalty(x, y):
    indices = ['A', 'C', 'G', 'T']
    p = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
    x_i = indices.index(x)
    y_i = indices.index(y)
    return p[x_i][y_i]


def minpenalty(x,y,gap_cost):
    m = len(x)
    n = len(y)
    dp = [[0]*(n+1) for i in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i * gap_cost

    for i in range(n+1):
        dp[0][i] = i * gap_cost

    for i in range(1,m+1):
        for j in range(1,n+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + mismatch_penalty(x[i-1],y[j-1]) , dp[i - 1][j] + gap_cost, dp[i][j - 1] + gap_cost)

    l = n+m
    i = m
    j = n
    xpos = l
    ypos = l
    xans = ['0']*(l+1)
    yans = ['0']*(l+1)

    while not (i == 0 or j == 0):
        if (x[i - 1] == y[j - 1]):
            xans[xpos] = x[i - 1]
            xpos -=1
            yans[ypos] = y[j - 1]
            ypos -=1
            i-=1 
            j-=1

        elif (dp[i - 1][j - 1] + mismatch_penalty(x[i-1],y[j-1]) == dp[i][j]):
        
            xans[xpos] = x[i - 1]
            xpos -=1
            yans[ypos] = y[j - 1]
            ypos -=1
            i-=1
            j-=1
        
        elif (dp[i - 1][j] + gap_cost == dp[i][j]):
        
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = '_'
            ypos-=1
            i-=1
        
        elif (dp[i][j - 1] + gap_cost == dp[i][j]):
        
            xans[xpos] = '_'
            xpos-=1
            yans[ypos] = y[j - 1]
            ypos-=1
            j-=1

    while (xpos > 0):
    
        if (i > 0): 
            i-=1
            xans[xpos] = x[i]
            xpos-=1
        else: 
            xans[xpos] = '_'
            xpos-=1

    while (ypos > 0):
     
        if (j > 0): 
            j-=1
            yans[ypos] = y[j]
            ypos-=1
        else: 
            yans[ypos] = '_'
            ypos-=1

    xans1 = []
    yans1 = []

    for X in xans:
        if X!='0':
            xans1.append(X)

    for X in yans:
        if X!='0':
            yans1.append(X)

    xansstr = ''.join(xans1)
    yansstr = ''.join(yans1)
    
    id = 1
    for i in range(l,-1,-1):
        if yans[i] == '_'  and xans[i] == '_': 
            id = i + 1
            break
    return xansstr[id-1:l], yansstr[id-1:l], dp[-1][-1]


def get_min_penalty(x,y,gap_cost):
    m = len(x)
    n = len(y)
    dp = [[0]*(n+1) for i in range(2)]

    for i in range(n+1):
        dp[0][i] = i * gap_cost

    dp[1][0] = gap_cost 
    for i in range(1,m+1):
        for j in range(1,n+1):
            if x[i-1] == y[j-1]:
                dp[1][j] = dp[0][j-1]
            else:
                dp[1][j] = min(mismatch_penalty(x[i-1], y[j-1]) + dp[0][j-1], gap_cost + dp[0][j], gap_cost + dp[1][j-1])
    
        for i in range(n+1):
            dp[0][i] = dp[1][i]

        # if i!=m:
        dp[1][0] = dp[1][0]+gap_cost
    return dp[-1]


def divide_conquer(x,y,gap_cost):
    if len(x)<=2 or len(y)<=2:
        return minpenalty(x,y,gap_cost)

    mid_x = math.ceil(len(x)/2)

    x_left = x[:mid_x]
    x_right = x[mid_x:]

    y_left_penalty_cost = get_min_penalty(x_left, y, gap_cost)
    y_right_penalty_cost = get_min_penalty(x_right[::-1], y[::-1], gap_cost)

    penalty_cost = []
    for a, b in zip(y_left_penalty_cost, y_right_penalty_cost[::-1]):
        penalty_cost.append(a+b)
    y_mid = penalty_cost.index(min(penalty_cost))

    ax, ay, gap_cost_left = divide_conquer(x_left, y[:y_mid], gap_cost)
    bx, by, gap_cost_right = divide_conquer(x_right, y[y_mid:], gap_cost)
    return (ax+bx, ay+by, gap_cost_left+gap_cost_right)

string_1, string_2 = generateStrings('input2.txt')
tracemalloc.start()
start = time.time()

a,b,c=divide_conquer(string_1,string_2,30)
print(a)
print(b)

current, peak = tracemalloc.get_traced_memory()
print('')
print('current memory is: '+str(current/10**6)+' MB; Peak was '+str(peak/10**6)+' MB')

end = time.time()
print("The time of execution of above program is :", end-start)