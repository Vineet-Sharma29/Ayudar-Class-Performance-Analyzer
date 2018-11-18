def makeDF (tuples, header):
    row_index = [int(i) for i in range(1, len(tuples) + 1)]
    col_index = list(header)
    df = pd.DataFrame(tuples, row_index, col_index)
    for col in list(df.columns):
        df[col] = df[col].fillna(value = 0)
    df['fraud'] = 0
    df['fraud'] = df[df.columns[-2]]

    return df

def scaleMarks (df):
    for exam in list(df.columns):
        if len(exam.split('-')) > 2:
            df[exam] = df[exam].apply(lambda x : (x*100)/int(exam.split('-')[2]))
    
    return df

def createAvg (marks):
    marks['overall'] = 0
    marks['avgExam'] = 0
    marks['avgLab'] = 0
    marks['avgAsgn'] = 0
    marks['avgOth'] = 0
    exams = 0
    lab = 0
    asgn = 0
    oth = 0

    for exam in list(marks.columns):
        if exam.lower().startswith('exam'):
            marks['avgExam'] += marks[exam]
            exams += 1  
            
        elif exam.lower().startswith('lab'):
            marks['avgLab'] += marks[exam]
            lab += 1
            
        elif exam.lower().startswith('asgn'):
            marks['avgAsgn'] += marks[exam]
            asgn += 1
            
        elif exam.lower().startswith('oth'):
            marks['avgOth'] += marks[exam]
            oth += 1
            
        else :
            continue

    marks['overall'] = 0.5*marks['avgExam']/exams + 0.3*marks['avgLab']/lab + 0.1*marks['avgAsgn']/asgn + 0.1*marks['avgOth']/oth
    return marks

def createChMarks (marks):
    df['ChMarks'] = (marks['avgExam'] + marks['avgLab'] + marks['avgOth'])/3
    return df

def variance(df):
    ls = list(df.columns)
    buffer = []
    for i in range(len(ls)):
        if len(ls[i].split('-')) > 2:
            buffer.append(ls[i])
        else:
            continue
    df['var'] = [int(i) for i in range(len(df[df.columns[0]]))]
    row_index = [int(i) for i in range(1, 1 + len(df[df.columns[0]]))]
    df['var'] = df['var'].apply(lambda x : (df.loc[row_index,buffer].iloc[x].describe()['std'])**2)
    return df

def CI(marks, column):
    column = str(column)
    std_error = marks[column].describe()['std']/(len(marks['avgExam']))**0.5
    mean = marks[column].describe()['mean']
    return (mean - 2*std_error, mean + 2*std_error,)

def width(tup):
    return tup[1] - tup[0]

def CourseStats(marks):
    marker = marks['overall'].describe()['75%']
    if marker > 0 and marker <40 :
        course_difficulty = "HIGH"
    elif marker > 40 and marker < 75 :
        course_difficulty = "MODERATE"
    else :
        course_difficulty = "EASY"
    
    cheatProb = 1 - width(CI(marks, 'avgAsgn'))/width(CI(marks, 'ChMarks'))
    if cheatProb > 0.7 and cheatProb < 1 :
        cheat_risk = "HIGH"
    elif cheatProb >0.4 and cheatProb < 0.7 :
        cheat_risk = "MODERATE"
    else :
        cheat_risk = "LOW"
    
    marks['cheatflagged'] = 0
    marks['cheatflagged'] = marks['avgAsgn'] - df['ChMarks']
    cheat_flagged = marks.sort_values('cheatflagged', ascending = False)['RollNumber'].iloc[1:6]
    
    avg_marks = str(CI(df,'overall')[0]) + '-' + str(CI(df,'overall')[1])
    
    quartile1 = marks['overall'].describe()['25%']
    quartile2 = marks['overall'].describe()['50%']
    quartile3 = marks['overall'].describe()['75%']
    
    return (course_difficulty, cheat_risk, list(cheat_flagged), avg_marks, quartile1, quartile2, quartile3,)

def ExamStats(marks):
    temp = list(marks.columns)
    count = 1
    for i in range(len(temp)):
        if temp[i].split('-') > 2 :
            count += 1
    location = temp[count]
    marker = marks[location].describe()['50%']
    if marker > 0 and marker <40 :
        course_difficulty = "HIGH"
    elif marker > 40 and marker < 75 :
        course_difficulty = "MODERATE"
    else :
        course_difficulty = "EASY"
        
    freq_df = df['fraud'].apply(lambda x : int(x%10)).value_counts()
    for i in range (10):
        try:
            if freq_df.loc[i] >= 0:
            continue
        except:
        freq_df.loc[i] = 0
    
    cheat_var = freq_df.describe()['std']**2
    if cheat_var < 15 :
        cheat_risk = 'LOW'
    if cheat_risk > 15 and cheat_risk < 80 :
        cheat_risk = 'MODERATE'
    else:
        cheat_risk = 'HIGH'
    
    max_repeat = freq_df.index[0]
    marks['fraud'] = marks['fraud'].apply(lambda x : int(x%10))
    suspicious = marks[marks['fraud'] == max_repeat]['fraud']
    check_sheets_index = random.sample(range(len(suspicious)), 5)
    cheat_flagged = []
    for index in check_sheets_index:
        cheat_flagged.append(marks['RollNumber'].iloc[index])
       
    avg_marks = str(CI(df,location)[0]) + '-' + str(CI(df,location)[1])
    
    quartile1 = marks[location].describe()['25%']
    quartile2 = marks[location].describe()['50%']
    quartile3 = marks[location].describe()['75%']
    
    return (course_difficulty, cheat_risk, cheat_flagged, avg_marks, quartile1, quartile2, quartile3,)
        

def PersistentLabels(df):
    consistent =  list(df[df['var'] < 30]['RollNumber'])
    moderately_varying = list(df[(df['var'] > 30) & (df['var'] < 150)]['RollNumber'])
    highly_varying = list(df[df['var'] > 150]['RollNumber'])
    
    return (consistent, moderately_varying, highly_varying,)


def PerformanceLabels(df):
    exceptional = list(df[df['overall'] > 85]['RollNumber'])
    promising = list(df[(df['overall'] < 85) & (df['overall'] > 50)]['RollNumber'])
    average = list(df[(df['overall'] < 50) & (df['overall'] > 30)]['RollNumber'])
    needy = list(df[df['overall'] < 30]['RollNumber'])
    
    return (exceptional, promising, average, needy,)

def mainFunc(df):
    df['temp'] = df['overall'] + df['var']
    
    return list(df.sort_values('temp', ascending = False)['RollNumber'][1:6])

def initialize(tuples, headers):
    df = makeDF(tuples, headers)
    df = scaleMarks(df)
    df = createAvg(df)
    df = createChMarks(df)
    df = variance(df)
    
    return df
