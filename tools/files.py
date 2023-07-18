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
            return os.listdir('questions/' + subject + '/' + i)

def get_price_total_score(subject, hardness):
    # read the folders in the questions folder
    types = give_question_hardness(subject)
    for i in types:
        if i[0] == hardness:
            return i[1], i[2]


if __name__ == '__main__':
    print(give_question_subjects())
    print(give_question_hardness("math"))
    print(get_price_total_score("math", "hard"))
    print(get_question_numbers("math", "simple"))