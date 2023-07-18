import importlib.util
spec = importlib.util.spec_from_file_location("connector", "DataBase/connector.py")
connector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connector)

if input("Are you sure you want to reset all tables? (yes/no)") != "yes":
    exit()

connector.run_sql("""DROP TABLE IF EXISTS Users, Teams, Problems;""")

connector.run_sql("""CREATE TABLE Users (
                  id INT NOT NULL AUTO_INCREMENT,
                  PRIMARY KEY (`id`),
                  name VARCHAR(255) NOT NULL,
                  username_hash VARCHAR(500) NOT NULL, 
                  password_hash VARCHAR(500) NOT NULL, 
                  privillage VARCHAR(255) NOT NULL)
                  """)

connector.run_sql("""CREATE TABLE Teams (
                    id INT NOT NULL,
                    PRIMARY KEY (`id`),
                    name VARCHAR(255) NOT NULL,
                    score INT NOT NULL,
                    stage1_problems VARCHAR(500),
                    stage2_problems VARCHAR(500),
                    stage3_problems VARCHAR(500));
                  """)

connector.run_sql("""CREATE TABLE Problems (
                    id INT NOT NULL,
                    PRIMARY KEY (`id`),
                    question_number VARCHAR(100) NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    hardness VARCHAR(100) NOT NULL,
                    team_id INT NOT NULL,
                    stage INT NOT NULL,
                    score INT,
                    stage1_time VARCHAR(100),
                    stage2_time VARCHAR(100),
                    stage3_time VARCHAR(100),
                    user_stage1 INT,
                    user_stage2 INT,
                    user_stage3 INT,
                    FOREIGN KEY (team_id) REFERENCES Teams(id),
                    FOREIGN KEY (user_stage1) REFERENCES Users(id),
                    FOREIGN KEY (user_stage2) REFERENCES Users(id),
                    FOREIGN KEY (user_stage3) REFERENCES Users(id));
                  """)


print("Done!")