import psycopg2 

def sql_select(query, parameters = None):
    conn = psycopg2.connect("dbname=casino")
    cur = conn.cursor()
    if parameters is not None:
        cur.execute(query,parameters)
    else:
        cur.execute(query)
    # Note that we are returning fetch all which can be empty if the executed code can't be found.
    result = cur.fetchall()
    conn.close
    return result

def sql_write(query, parameters = None):
    conn = psycopg2.connect("dbname=casino")
    cur = conn.cursor()
    if parameters is not None:
        cur.execute(query,parameters)
    else:
        cur.execute(query)
    conn.commit()
    conn.close