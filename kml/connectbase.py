import pandas as pd
import sqlite3, os
import math as mt
from django.core.files.storage import FileSystemStorage

def upload_sectors(table):
    con = sqlite3.connect('map.sqlite')
    cur = con.cursor()
    try:
        spatialite_path ='D:/4.Computers/2.Python/DJANGO/developing/MAPS/maps/kml/mod_spatialite-5.0.1-win-amd64/mod_spatialite-5.0.1-win-amd64'
        os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']

        con.enable_load_extension(True)
        con.load_extension("mod_spatialite")

    except sqlite3.Error as error:
        print(error)
    try:
        cur.execute('DROP TABLE sectors')
        print('deletado')
    except sqlite3.Error as err:
        print('bolaerrada')
        print(str(err))

    con.commit()
    dataframe = pd.read_csv(table)
    print(dataframe)
    strqueryend = '(SECID INTEGER PRIMARY KEY AUTOINCREMENT,'
    strquery = '('
    for i in list(dataframe.columns):
        strqueryend = strqueryend + i + ','
        strquery = strquery + i + ','

    strqueryend = strqueryend + 'SELECTOR,COLOR)'
    strquery = strquery + 'SELECTOR,COLOR)'
    sqlqueryend = 'CREATE TABLE sectors ' + strqueryend
    cur.execute(sqlqueryend)
    query="Select AddGeometryColumn ('sectors','geometry',4326,'POLYGON','XY');"
    cur.execute(query)


    row = 0
    sqlcoluna = ''
    dima = dataframe.shape

    # collecting data
    for i in range(dima[0]):
        col = 0
        sqlrow = '('
        for n in list(dataframe.loc[i]):
            sqlrow = sqlrow + '"' + str(n) + '",'
            col = col + 1
        sqlrow = sqlrow + '"","")'

        if i < int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ','

        if i == int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ';'

    #####insertin data into the table sites######
    sqlquery = 'INSERT INTO sectors ' + strquery + ' VALUES' + sqlcoluna
    cur.execute(sqlquery)
    con.commit()
    try:
        cur.execute('DROP TABLE sectorstemp')
        sqlquery = 'CREATE TABLE sectorstemp AS SELECT * FROM sectors;'
        cur.execute(sqlquery)
    except:
        sqlquery = 'CREATE TABLE sectorstemp AS SELECT * FROM sectors;'
        cur.execute(sqlquery)


def upload_sites(table):
    spatialite_path = 'D:/4.Computers/2.Python/DJANGO/developing/MAPS/maps/kml/mod_spatialite-5.0.1-win-amd64/mod_spatialite-5.0.1-win-amd64'
    os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']
    con = sqlite3.connect('map.sqlite')
    con.enable_load_extension(True)
    con.load_extension("mod_spatialite")
    cur = con.cursor()
    try:
        cur.execute('DROP TABLE sites')
    except:
        pass

    dataframe = pd.read_csv(table)
    strqueryend = '(STID INTEGER PRIMARY KEY AUTOINCREMENT,'
    strquery = '('
    for i in list(dataframe.columns):
        strqueryend = strqueryend + i + ','
        strquery = strquery + i + ','

    strqueryend = strqueryend + 'SELECTOR,COLOR)'
    strquery = strquery + 'SELECTOR,COLOR)'
    sqlqueryend = 'CREATE TABLE sites ' + strqueryend
    cur.execute(sqlqueryend)
    query = "Select AddGeometryColumn ('sites','geometry',4326,'POINT','XY');"
    cur.execute(query)


    row = 0
    sqlcoluna = ''
    dima = dataframe.shape

    #collecting data
    for i in range(dima[0]):
        col = 0
        sqlrow = '('
        for n in list(dataframe.loc[i]):
            sqlrow = sqlrow + '"' + str(n) + '",'
            col = col + 1
        sqlrow = sqlrow + '"","")'

        if i < int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ','

        if i == int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ';'

    #####insertin data into the table sites######
    sqlquery = 'INSERT INTO sites ' + strquery + ' VALUES' + sqlcoluna
    cur.execute(sqlquery)
    con.commit()
    try:
        cur.execute('DROP TABLE sitestemp')
        sqlquery = 'CREATE TABLE sitestemp AS SELECT * FROM sites;'
        cur.execute(sqlquery)
    except:
        sqlquery = 'CREATE TABLE sitestemp AS SELECT * FROM sites;'
        cur.execute(sqlquery)

def createsectors(elementtyp):
    fs = FileSystemStorage()
    spatialite_path = 'D:/4.Computers/2.Python/DJANGO/developing/MAPS/maps/kml/mod_spatialite-5.0.1-win-amd64/mod_spatialite-5.0.1-win-amd64'
    os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']
    con = sqlite3.connect('map.sqlite')
    con.enable_load_extension(True)
    con.load_extension("mod_spatialite")
    cur = con.cursor()
    limiter = 0
    try:
        sqlquery = 'SELECT * FROM sites'
        cur.execute(sqlquery)
        tablesites = pd.DataFrame(cur.fetchall())
        tablesites.sort_values(by=[1, 2], inplace=True)
        aux = list(cur.description)
        fields = []
        for i in aux:
            fields.append(i[0])

        try:
            sqlquery = 'SELECT * FROM sectors'
            cur.execute(sqlquery)
            tablesectors = pd.DataFrame(cur.fetchall())
            tablesectors.sort_values(by=[1, 3, 4], inplace=True)
            agregation = list(tablesites[1].unique())
            aux = list(cur.description)
            fieldsect = []
            for i in aux:
                fieldsect.append(i[0])
        except:
            pass

        ########################creating folder agregation-sites#############################
        for i in range(tablesites.shape[0]):

            #colorsite = tablesites[tablesites.shape[1] - 2][i]
            #if colorsite == '':
                #colorsite = '#eaebec'

            selected = tablesites[tablesites.shape[1] - 3][i]
            site = tablesites[2][i]
            lat = round(float(tablesites[3][i]), 8)
            long = round(float(tablesites[4][i]), 8)
            ###############starting site description##################
            # estou aqyi
            query="UPDATE sites SET geometry= (GeomFromText('POINT("+str(lat)+" "+str(long)+")',4326)) WHERE site= '"+str(site)+"'"
            print(query)
            cur.execute(query)

            ###################starting sector creation##################################

            if elementtyp == 'sectorclick':
                counter = 0
                terminator = 0
                for isc in range(limiter, tablesectors.shape[0]):

                    if site == tablesectors[3][isc]:
                        counter = terminator
                        limiter = limiter + 1

                        #colorsec = tablesectors[tablesectors.shape[1] - 2][isc]
                        #if colorsec == '':
                            #colorsec = '#55ffff'
                        sector = tablesectors[4][isc]
                        azimuth = float(tablesectors[6][isc] * 1)
                        bandhor = float(tablesectors[9][isc] * 1)

                        latp1 = lat + (250 * (180 / mt.pi) * mt.cos(
                            (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000
                        lonp1 = long + (250 * (180 / mt.pi) * mt.sin(
                            (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000

                        latp2 = lat + (250 * (180 / mt.pi) * mt.cos(
                            (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000
                        lonp2 = long + (250 * (180 / mt.pi) * mt.sin(
                            (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000

                        query="UPDATE sectors SET geometry= "
                        query=query+"(GeomFromText('POLYGON(("+str(lat)+" "+str(long)+","+str(latp1)+" "+str(lonp1)+","+str(latp2)+" "+str(lonp2)+","+str(lat)+" "+str(long)+"))',4326))"
                        query=query+" WHERE sector='"+sector+"'"
                        cur.execute(query)

                    else:
                        pass
                    if counter > 0:
                        xy = terminator - counter
                        if xy == 1:
                            break
                    terminator = terminator + 1

        con.commit()

    except:
        elementtyp == 'site'
        pass

#upload_sectors('D:/4.Computers/2.Python/Scripts/gtemplate_sector_testeload.csv')
#upload_sites('D:/4.Computers/2.Python/Scripts/gtemplate_site_testeload.csv')
#createsectors('sectorclick')