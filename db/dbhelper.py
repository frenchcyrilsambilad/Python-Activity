from sqlite3 import connect,Row
database:str = "db/school.db"

def getprocess(sql:str,vals:list)->list:
    try:
        print(sql)
        conn:any = connect(database)
        conn.row_factory = Row
        cursor:any = conn.cursor()
        cursor.execute(sql,vals)
        data:list = cursor.fetchall()
    except Exception as ex:
        print(f"Exception: {ex}")
    finally:
        cursor.close()
        conn.close()
        return data
        
def postprocess(sql:str,vals:list)->bool:
    try:
        print(sql)
        conn:any = connect(database)
        cursor:any = conn.cursor()
        cursor.execute(sql,vals)
        conn.commit()
    except Exception as ex:
        print(f"Exception: {ex}")
    finally:
        cursor.close()
        conn.close()
        return True if cursor.rowcount>0 else False
#
def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql,[])
    
def getrecord(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append(f"`{key}`=?")
    fields:str = " AND ".join(flds)
    sql:str = f"SELECT * FROM `{table}` WHERE {fields}"
    return getprocess(sql,vals)
    
def deleterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append(f"`{key}`=?")
    fields:str = " AND ".join(flds)
    sql:str = f"DELETE FROM `{table}` WHERE {fields}"
    return postprocess(sql,vals)
    
def addrecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    print(vals)
    dta:list = ['?']*len(keys)
    data:str = ",".join(dta)
    fields:str = "`,`".join(keys)
    sql:str = f"INSERT INTO `{table}`(`{fields}`) VALUES({data})"
    return postprocess(sql,vals)
    
def updaterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    newvals:list = []
    for index in range(1,len(keys)):
        flds.append(f"`{key[index]}`=?")
        newvals.append(f"{vals[index]}")
    fields:str = ",".join(flds)
    sql:str = f"UPDATE `{table}` SET {fields} WHERE `{key[0]}`={vals[0]}"
    return postprocess(sql,vals)
    