import  mysql.connector
import importlib.util

spec = importlib.util.spec_from_file_location("config", "tools/config.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

config = config.read_config()


def run_sql(sql):
    mydb = mysql.connector.connect(
    host=config["Database_host"],
    user=config["Database_Username"],
    password=config["Database_Password"],
    database=config["Database_name"]
    )    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mydb.commit()
    return myresult


if __name__ == '__main__':

    # add a table to the database
    #run_sql("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

    # add some sample to the table 
    run_sql('INSERT INTO customers (name, address) VALUES ("John","Highway 21")')
    run_sql('INSERT INTO customers (name, address) VALUES ("John2","Highway 231")')
    run_sql('INSERT INTO customers (name, address) VALUES ("John3","Highway 241")')

    # select a sample from the table
    ans = run_sql("SELECT * FROM customers")
    print(ans)