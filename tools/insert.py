import importlib.util
spec = importlib.util.spec_from_file_location("connector", "DataBase/connector.py")
connector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connector)

spec = importlib.util.spec_from_file_location("security", "tools/security.py")
suc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suc)

def insert_user(name, username, password, privillage):
    password = suc.hash(password)

    connector.run_sql(f"""
                    INSERT INTO Users (name, username, password_hash, privillage) VALUES  
                    ("{name}", "{username}" , "{password}", "{privillage}");                 
                  """)

def insert_team(name, id):
    connector.run_sql(f"""
                    INSERT INTO Teams (name, id, score, stage1_problems, stage2_problems, stage3_problems) VALUES  
                    ("{name}", {id} , 0, "", "", "");                 
                  """)
  
def insert_problem(question_number, subject, hardness, team_id, user_stage1, stage1_time, price, total_score):
    connector.run_sql(f"""
                    INSERT INTO Problems (question_number, subject, hardness, team_id, stage, score, user_stage1, stage1_time, price, total_score) VALUES  
                    ("{question_number}", "{subject}", "{hardness}", {team_id}, 1, 0, {user_stage1}, "{stage1_time}", {price}, {total_score});         
                  """)
