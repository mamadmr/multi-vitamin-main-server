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

if __name__ == '__main__':
    print(give_question_subjects())
    print(give_question_hardness("math"))