import os


def give_question_subjects():
    # read the folders in the questions folder
    folders = []
    for i in os.listdir("questions"):
        if '.' not in i:
            folders.append(i)
    return folders

def give_question_hardness(subject):
    # read the folders in the questions folder
    folders = []
    for i in os.listdir("questions/" + subject):
        if '.' not in i:
            folders.append(i.split('-'))
    return folders

def get_question_numbers(subject, hardness):
    temp =  os.listdir('questions/' + subject)
    for i in temp:
        if i.startswith(hardness):
            return [i for i in os.listdir('questions/' + subject + '/' + i) if i.endswith('.pdf')]

def get_price_total_score(subject, hardness):
    # read the folders in the questions folder
    # price - total_score
    types = give_question_hardness(subject)
    for i in types:
        if i[0] == hardness:
            return i[1], i[2]


if __name__ == '__main__':
    #print(give_question_subjects())
    #print(give_question_hardness("فیزیک"))
    print(get_question_numbers("زیست", "سخت"))

    #print(get_question_numbers("math", "simple"))