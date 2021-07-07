import pandas as pd
import os
import math as mt

def geojsonsectors():
    limiter = 0
    try:
        sitestb=pd.read_csv("D:/4.Computers/gtemplate_site_testeload.csv")
        tablesites = pd.DataFrame(sitestb)
        tablesites.sort_values(by=['SITE'])
        aux = list(tablesites.columns)
        fields = []
        for i in aux:
            fields.append(i[0])

        try:

            tablesectors = pd.DataFrame(pd.read_csv("D:/4.Computers/gtemplate_sector_testeload.csv"))
            tablesectors.sort_values(by=['SITE','SECTOR'], inplace=True)

            agregation = list(tablesites['AGREGATION'].unique())
            aux = list(tablesectors.columns)

            fieldsect = []


            for i in aux:

                fieldsect.append(i)
        except:
            pass

        ############creating agregation style#############

        kmltext = open('geomap.txt', 'w')
        kmltext.writelines(['{ \n "type": "FeatureCollection",\n'])
        kmltext.writelines(['"features":[\n'])

        kmltext.close()
        kmltext = open('geomap.txt', 'a')


        ########################creating folder agregation-sites#############################
        for i in range(tablesites.shape[0]):

            site = tablesites.iat[i,1]
            print(site)
            lat = round(float(tablesites.iat[i,2]), 8)
            long = round(float(tablesites.iat[i,3]), 8)
            ###############starting site description##################
            # estou aqyi

            kmltext.writelines('{\n"type": "Feature",\n')
            kmltext.writelines('"properties": {')
            kmltext.writelines('"Site":"' + str(site) + '",\n')

            for l in range(4, tablesites.shape[1]):
                paramsites = tablesites.iat[i,l]
                kmltext.writelines('"' + fields[l] + '": "' + tablesites.iat[i,l] + '",')
            kmltext.writelines('"none":""},\n')
            kmltext.writelines('"geometry": {\n')
            kmltext.writelines('"type": "Polygon",\n')
            kmltext.writelines('"coordinates": [' + str(long) + "," + str(lat) + ']\n')
            kmltext.writelines('}\n')
            kmltext.writelines('},\n')  # ending site


            ###################starting sector creation##################################


            counter = 0
            terminator = 0

            for isc in range(limiter, tablesectors.shape[0]):


                if site == tablesectors.iat[isc,2]:
                    counter = terminator
                    limiter = limiter + 1
                    kmltext.writelines('{\n"type": "Feature",\n')

                    sector = tablesectors.iat[isc,3]
                    azimuth = float(tablesectors.iat[isc,5]* 1)
                    bandhor = float(tablesectors.iat[isc,8]* 1)

                    kmltext.writelines('"properties": {')
                    kmltext.writelines('"sector":"' + str(sector) + '",\n')


                    for lns in range(13, tablesectors.shape[1]):
                        paramsector = tablesectors.iat[isc,lns]
                        kmltext.writelines('"' + str(fieldsect[lns]) + '": "' + str(tablesectors.iat[isc,lns]) + '",\n')

                    kmltext.writelines('"none":""},\n')
                    kmltext.writelines('"geometry": {\n')
                    kmltext.writelines('"type": "Polygon",\n')

                    latp1 = lat + (250 * (180 / mt.pi) * mt.cos(
                        (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000
                    lonp1 = long + (250 * (180 / mt.pi) * mt.sin(
                        (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000

                    latp2 = lat + (250 * (180 / mt.pi) * mt.cos(
                        (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000
                    lonp2 = long + (250 * (180 / mt.pi) * mt.sin(
                        (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000

                    kmltext.writelines('"coordinates": [[[' + str(round(long,6)) + "," + str(round(lat ,6)) +'],'\
                                        +'['+str(round(lonp1,6))+','+str(round(latp1 ,6))+'],'
                                        +'['+str(round(lonp2,6))+','+str(round(latp2 ,6))+'],'
                                        +'['+str(round(long,6))+','+str(round(lat ,6))+']]]\n')

                    kmltext.writelines('}\n')
                    kmltext.writelines('},\n')  # ending sector

                else:
                    pass
                if counter > 0:
                    xy = terminator - counter
                    if xy == 1:
                        break
                terminator = terminator + 1


        print('foca')
        kmltext.writelines('{"type": "Feature",\n"properties": {"none":"none"},\n"geometry": {\n"type": "Polygon",\n"coordinates": [[[ 45.424706,-75.695245],[ 45.424849,-75.695051],[ 45.424704,-75.694923],[ 45.424706,-75.695245]]]\n}\n}')

        kmltext.writelines(']\n}\n')
        kmltext.close()

        try:
            pathfile = 'del geomap.geojson'
            pathfile = pathfile.replace('/', os.sep)
            os.system(pathfile)
        except:
            pass
        pathfile = 'rename geomap.txt geomap.geojson'
        pathfile = pathfile.replace('/', os.sep)
        os.system(pathfile)

    except:
        #elementtyp == 'site'
        pass

geojsonsectors()