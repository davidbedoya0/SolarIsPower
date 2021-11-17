from ComponentsDB import *
# importaciond del modulo ps
import psycopg2

def createDBData(dbName, db, Dtyp, cursor):
    names = []
    for name, dict_ in db.items():
        names.append(name)

    sqlcrt = "CREATE TABLE " + dbName + " ("
    
    for i in range(len(names)):
        if i == (len(names) - 1):
            sqlcrt = sqlcrt + " " + names[i] + " " + Dtyp[i] + ")"
            break;
        sqlcrt = sqlcrt + " " + names[i] + " " + Dtyp[i] + ","
    cursor.execute(sqlcrt)
    con.commit()



def dbupdate(dbName, db, index, con, cursor):
    data = []
    names = []
    for name, dict_ in db.items():
        names.append(name)
    tam = len(db[names[0]])    
    sql_1 = "INSERT INTO " + dbName + " ("
    
    for i in range(len(names)):
        if i == len(names) - 1:
            sql_1 = sql_1 + names[i] + ") VALUES( "    
            break;
        sql_1 = sql_1 + names[i] + ", "
    
    for i in range(len(names)):
        if i == len(names) - 1:
            data.append(0)
            sql_1 = sql_1 + "%s)"    
            break;
        data.append(0)
        sql_1 = sql_1 + "%s, "

    for i in range(tam):
        for j in range(len(names)):
            var = db[names[j]][i]
            data[j] = str(var)
        cursor.execute(sql_1, data)
        con.commit()


con = psycopg2.connect( user="postgres", 
                        password="password123",
                        host='127.0.0.1', 
                        port="5432",
                        database="pvprojdata")
curs = con.cursor()
createDBData("proteccionesAC", proteccionesAC, ["VARCHAR (50)", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT"], curs)
dbupdate("proteccionesAC", proteccionesAC, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], con, curs)

createDBData("DPS_AC", DPS_AC, ["VARCHAR (50)", "INT", "INT", "FLOAT", "INT"], curs)
dbupdate("DPS_AC", DPS_AC, [0, 0, 0, 0, 1], con, curs)

createDBData("DPS_DC", DPS_DC, ["VARCHAR (50)", "INT", "INT", "INT", "INT", "VARCHAR (50)"], curs)
dbupdate("DPS_DC", DPS_DC, [0, 0, 0, 0, 1, 0], con, curs)

createDBData("WiresISO", WiresISO, ["VARCHAR (50)", "INT", "FLOAT", "INT", "INT"], curs)
dbupdate("WiresISO", WiresISO, [0, 0, 0, 0, 1], con, curs)

createDBData("WiresDCIso", WiresDCIso, ["VARCHAR (50)", "INT", "FLOAT", "INT", "INT"], curs)
dbupdate("WiresDCIso", WiresDCIso, [0, 0, 0, 0, 1], con, curs)

createDBData("bdMeters", bdMeters, ["VARCHAR (50)", "INT", "INT"], curs)
dbupdate("bdMeters", bdMeters, [0, 0, 0], con, curs)

createDBData("dbCT", dbCT, ["VARCHAR (50)", "INT", "INT", "INT", "INT"], curs)
dbupdate("dbCT", dbCT, [0, 0, 0, 0, 0], con, curs)

createDBData("PVC", PVC, ["VARCHAR (50)", "FLOAT", "FLOAT", "INT", "INT"], curs)
dbupdate("PVC", PVC, [0, 0, 0, 1, 0], con, curs)

createDBData("EMT", EMT, ["VARCHAR (50)", "FLOAT", "FLOAT", "INT", "INT"], curs)
dbupdate("EMT", EMT, [0, 0, 0, 1, 0], con, curs)

createDBData("IMC", IMC, ["VARCHAR (50)", "FLOAT", "FLOAT", "INT", "INT"], curs)
dbupdate("IMC", IMC, [0, 0, 0, 1, 0], con, curs)

createDBData("SoilStruct", SoilStruct, ["VARCHAR (50)", "INT", "INT"], curs)
dbupdate("SoilStruct", SoilStruct, [0, 0, 0], con, curs)

createDBData("clayTileStruct", clayTileStruct, ["VARCHAR (50)", "INT", "INT"], curs)
dbupdate("clayTileStruct", clayTileStruct, [0, 0, 0], con, curs)

createDBData("metalicStruct", metalicStruct, ["VARCHAR (50)", "INT", "INT"], curs)
dbupdate("metalicStruct", metalicStruct, [0, 0, 0], con, curs)

