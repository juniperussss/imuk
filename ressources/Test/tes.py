from meteostat import Hourly
import pandas  as pd
import json
from datetime import datetime
from ressources.tools.imuktools import nclwwstring
# load data using Python JSON module
with open('../Data/full.json', 'r') as f:
    data = json.loads(f.read())
# Flatten data
icao_to_meteostat = pd.json_normalize(data)#, record_path =['identifiers'], meta=["id"])
#print(icao_to_meteostat.head()["identifiers.icao"])
#print(icao_to_meteostat.columns)
listofairportsfound=["ENJA","Schnling"]
listofairportsfound_meteostat=[]
icao_to_meteostat=icao_to_meteostat.rename(columns={"name.en": "a", "location.latitude": "latitude"})
for i in listofairportsfound:
    #listofairportsfound_meteostat.append(icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i])
    listofairportsfound_meteostat.append(icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].latitude.squeeze())

#print(listofairportsfound_meteostat)
#print(type(listofairportsfound_meteostat[1]))
#listofairportsfound_meteostat = [i for i in listofairportsfound_meteostat if isinstance(i,str) else 'None'] #!= 'Series([], Name: id, dtype: object)']
listofairportsfound_meteostat = [i if isinstance(i,str) else 'None'for i in listofairportsfound_meteostat]
#print(listofairportsfound_meteostat)
start = datetime(2023, 3, 22,0,0)
end = datetime(2023, 3, 22, 0, 0)
test=['LSMA0', '06610', 'EEEI0']#, '16641', '06762', '03894', '03204', '16648', '16627', '16665', '16742', '16650', '16723', '16140', '10619', '10500', '16687', '03068', 'LTCP0', 'LTAY0', '17234', '17112', '17099', 'LTCN0', 'LTDA0', 'LTFD0', 'LTFG0', 'LBPG0', 'LBPL0', '10687', '17124', 'LTAB0', '17129', '17244', '17090', '17150', '17115', '17218', 'LTBQ0', '17202', '17170', '17120', '06240', '07480', '07055', '07240', '08540', '08534', '37212', 'UWLW0', '03583', '03644', '17350', '03391', '16706', '11414', '11448', '11165', '17092', '03967', '08562', '16312', '16148', '16088', '16245', '16459', '10775', '10607', '10614', '10633', '16261', '26478', 'ULPB0', '27760', '16429', '16332', '16546', '16045', '16098', '16206', '03577', '17098', '16253', 'EVGA0', '13615', 'LSZC0', 'EKRS0', 'LSMD0', '06614', 'ESTA0', '02000', 'EGCK0', 'EGHQ0', '02945', '02929', '02869', 'EFKT0', '02958', '02948', '02966', '02672', '02604', 'ESOH0', 'ESNZ0', '02562', '02520', '02154', 'ESIA0', '02458', 'ESNV0', 'ESUP0', 'ESND0', '02947', 'EEKE0', 'EDBC0', 'EDTY0', '10200', '06104', '06180', '06080', '06170', '06190', '06118', '06110', '06108', '02807', '02935', '02864', '02903', '02970', '02952', '02845', '02944', '02972', '02911', '01452', '01408', '01271', '16754', '16749', '01210', '01289', 'LSGC0', '06700', '06720', '06770', 'LSZB0', '06632', '06670', '06690', 'LSZS0', '02664', '02526', '02550', '02512', '02651', '02636', '02641', '02366', '02267', '02044', '02293', '02286', '02416', '02446', '02186', '02571', '02590', '03917', '03534', '03724', '03768', 'EGNJ0', 'EGNX0', '03017', '03003', '03091', '03924', '03243', '10528', '02049', '02259', 'ESOE0', 'ESSL0', 'ESUT0', 'EETN0', '26242', '02974', '26406', '26502', '26730', '03715', '03772', '03683', 'ESKN0', '02464', '02435', '01049', '01083', '01059', '01290', '16531', '16076', '16120', '16080', 'ENBL0', 'ENHK0', '01068', '01074', '01217', '16520', '16560', '16066', '16059', '16242', '16170', '01347', '01162', '01046', '16718', '16270', '16320', '16460', '16405', '16099', '16108', '16149', '16090', '16105', '11240', '11150', '10385', '10488', '10554', '10637', '10147', '10513', '10469', '10708', '10738', '10338', '06478', '10315', '10400', '10866', '10763', '10224', '10348', '10018', '03895', '06590', 'ENBS0', '01310', '01097', '16239', '11120', '11231', '11010', '11036', '06449', '06407', '10192', '10149', 'EDHK0', '10805', 'ESKM0', '10730', '16682', '16726', '16746', '16622', '10571', '10616', '10156', '10403', '10426', '10416', '10852', '10935', '10685', '10702', '10436', '06450', '06451', '03160', '03135', '03026', '06070', '06060', '01152', '01241', '01161', '01025', '02460', '02897', '02917', '02875', '06030', '16230', '16362', '16191', '16490', '16181', '06275', '06350', '06269', '10439', '10502', '03590', '10343', '10334', '10476', '10853', '10743', '10172', '03334', '03673', 'EGLC0', '03075', '03059', '03140', '03022', '03492', '03839', '03649', '06380', '06280', '06344', '06370', 'LTCS0', '10335', '10246', '10856', '16289', '10136', '03776', '17352', '17300', '17060', '17219', '17295', '17260', '17082', '17200', '17195', '17280', '17096', '17038', '17282', '17128', 'LBGO0', 'LTBR0', 'LTBU0', '17241', 'LTFJ0', 'EPSY0', 'LFGA0', 'LFJR0', '12970', '12825', 'LHPR0', '12860', 'LFLP0', 'LFQA0', '08495', '07109', 'LYBT0', 'LYKV0', '13183', '03384', '07603', '07675', '07648', '12465', '12424', '07530', '07552', '07093', '07635', '07579', 'LFMU0', '12882', '12942', '11692', 'LFOV0', 'LFRV0', 'LFSG0', 'LFAQ0', 'LFBU0', 'LFOZ0', 'LFPT0', '08233', 'UUBW0', 'UUDL0', 'UUMO0', '37235', 'URMO0', 'UWKS0', '08075', 'LUKK0', '13348', 'LEHC0', 'LESB0', '08397', '15260', '07379', '07153', '60338', '12150', '12566', '12560', 'EPMO0', '12330', '12580', '12205', '12375', '15655', '15625', '15614', '15552', '12839', '15420', '15481', '15421', '15247', '14474', '14280', '14307', '13116', '14444', '14241', '14431', '14014', '14026', '13105', '11782', '11518', '11723', '13353', '13586', '13272', '13388', '13457', '11816', '11934', '07003', '07630', '07610', '07621', '07602', '07790', '07754', '07761', '07491', '07460', '07481', '07486', '07684', '07475', '07650', '07690', '07747', '07643', '07028', '07146', '07149', '07024', '07125', '07031', '07027', '07130', '07201', '07222', '07217', '07299', '07180', '07190', '07646', '07524', '07502', '07607', '07780', '07038', '07037', '07150', '07157', '07147', '07205', '07280', '07169', '07179', '07181', '07292', '07667', '08000', '08545', '08524', '26850', 'UUDD0', '34929', '37054', '34949', '37171', 'URWA0', '34861', '34560', 'UUEE0', 'UUWW0', 'UWKD0', '27607', '28900', '08360', '08487', '08011', '08025', '08181', '08002', 'LEDA0', '08184', '08419', '08373', '08451', '08433', 'LELL0', '08221', '08482', '08314', '08306', '08085', '08175', '08029', '08042', '08284', '08140', '08080', '08045', '08021', '08160', '08391', '08055', '08202', '07647', '07476', '11624', '11652', 'URML0', '03746', '03809', '03853', '03165', '03414', '03302', '03066', '03171', '03658', '03761', '03749', '03672', '03257', '03462', '03377', '03264', '03379', '03372', '03482', '06340', '08536', '06458', '06479', '06432', '06465', '06456', '06496', '03955', '03969', '03962', '07510', '07412', '07434', '07428', '07765', '07168', '07247', '13242', '13257', '08280', '08410', '08330', '08084', '08227', '07386', '07549', '07257', '07249', '07306', '07235', '16158', '08554', '26063', 'URKA0', '10752', '06235', '26898', '34214', 'UUOK0', 'UWGG0', 'UWLL0', '22550', '22113', '26702', '34122', '23804', '15150', '15450', '15090', '15023', '15335', '15200', '15014', '15120', '15080', '15010', '15145', '06270', '06375', '16597', '06400', '16699']
data = Hourly(test, start, end)
data = data.fetch()
#print(data.head())
#for x in data.index:
    #print(x[0])
    #print(icao_to_meteostat[icao_to_meteostat["id"]==x[0]].latitude.squeeze())
#print(data.loc["LSMA0"].pres.squeeze())
#data.index = data.index.get_level_values(0)
#data = pd.DataFrame({'station':data.index, 'pres':data["pres"]})
#print(data.head())
#print(data.index)
#print(icao_to_meteostat.columns)

from metar import Metar

obs = Metar.Metar('METAR KEWR 111851Z VRB03G19KT 2SM R04R/3000VP6000FT TSRA BR FEW015 BKN040CB BKN065 OVC200 22/22 A2987 RMK AO2 PK WND 29028/1817 WSHFT 1812 TSB05RAB22 SLP114 FRQ LTGICCCCG TS OHD AND NW -N-E MOV NE P0013 T02270215')
cc=[]
#print(obs.wind_speed)
#print(str(10).zfill(3)[0:2])
#print(str(int(-1928.8))[1:4])

#print(cloudcover(obs))
datas = pd.read_csv('../Data/metarsupp.csv')
#print(datas[0])
df=nclwwstring(datas)
#print(df.head())