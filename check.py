import importlib.util
spec = importlib.util.spec_from_file_location("connector", "DataBase/connector.py")
connector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connector)

spec = importlib.util.spec_from_file_location("security", "tools/security.py")
suc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suc)

teams = connector.run_sql("SELECT id from teams")
temp2 = set(connector.run_sql("SELECT subject, hardness FROM problems where team_id=5713"))


def counter():
    rr = []
    for i in teams:
        i = i[0]
        #temp1 = connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))
        temp = connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))
        rr.append([len(temp), i])
    rr.sort()
    rr.reverse()
    print(rr)

def question_check():
    for i in teams:
        i = i[0]
        temp1 = set(connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i)))
        temp = len(set(connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))))
        if temp != 18:
            print(temp, i, temp2-temp1)

counter()
exit()



exit()
temp = len(connector.run_sql("SELECT * FROM multivitamin.Problems where team_id=1918;"))
print(temp)
teams = connector.run_sql("SELECT id from teams")

for i in teams:
    i = i[0]
    #temp1 = connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))
    temp = connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))
    print(len(temp), i)

exit()
teams = connector.run_sql("SELECT id from teams")
temp = set(connector.run_sql("SELECT subject, hardness FROM problems where team_id=1912"))
temp2 = set(connector.run_sql("SELECT subject, hardness FROM problems where team_id=1920"))

for i in teams:
    i = i[0]
    temp1 = set(connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i)))
    temp = len(set(connector.run_sql("SELECT subject, hardness FROM problems where team_id="+str(i))))
    if temp != 18:
        print(temp, i, temp2-temp1)
