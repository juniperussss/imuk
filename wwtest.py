#
#  File:
#    wmstnm03.py
#
#  Synopsis:
#    Illustrates plotting station model data over a map.
#
#  Category:
#    Wind barbs/Station model data.
#
#  Author:
#    Fred Clare
#
#  Date of initial publication:
#    September, 2007
#
#  Description:
#    Draws station model data for U.S. cities using a satellite
#    view map projection.
#
#  Effects illustrated:
#    o  Drawing station model data over a map.
#    o  Adjustment of the wind barb directions based on latitude.
#
#  Output:
#    A single visualization is produced that draws the
#    given station model data.
#
#  Notes:
#
from __future__ import print_function
import Ngl
import numpy
import sys

#
#  Plot station model data over a map.
#

cities = [       "NCAR",       "Seattle", "San Francisco",    \
          "Los Angeles",      "Billings",       "El Paso",    \
              "Houston",   "Kansas City",   "Minneapolis",    \
              "Chicago",       "Detroit",       "Atlanta",    \
                "Miami",      "New York",        "Eugene",    \
                "Boise",     "Salt Lake",       "Phoenix",    \
          "Albuquerque",      "Bismarck",         "Tulsa",    \
               "Dallas",   "Little Rock",     "Lexington",    \
            "Charlotte",       "Norfolk",        "Bangor"     \
         ]
city_lats = [      40.0,            47.6,            37.8,    \
                   34.1,            45.8,            31.8,    \
                   29.8,            39.1,            45.0,    \
                   41.9,            42.3,            33.8,    \
                   25.8,            40.8,            44.1,    \
                   43.6,            40.7,            33.5,    \
                   35.1,            46.7,            36.0,    \
                   32.8,            34.7,            38.1,    \
                   35.2,            36.8,            44.8     \
            ]
city_lons = [    -105.0,          -122.3,          -122.4,    \
                 -118.3,          -108.5,          -106.5,    \
                 -095.3,          -094.1,          -093.8,    \
                 -087.6,          -083.1,          -084.4,    \
                 -080.2,          -074.0,          -123.1,    \
                 -116.2,          -111.9,          -112.1,    \
                 -106.6,          -100.8,          -096.0,    \
                 -096.8,          -092.3,          -084.1,    \
                 -080.8,          -076.3,          -068.8     \
            ]
#
#  Station model data for the 27 cities.
#
imdat =  ["11000000751126021360300004955054054600007757087712",  \
          "11103100011104021080300004959055050600517043080369",  \
          "11206200031102021040300004963056046601517084081470",  \
          "11309300061000021020300004967057042602017125082581",  \
          "11412400091002021010300004971058038602517166083592",  \
          "11515500121004020000300004975050034603017207084703",  \
          "11618600151006020030300004979051030603507248085814",  \
          "11721700181008020050300004983052026604007289086925",  \
          "11824800211009020070300004987053022604507323087036",  \
          "11927900241011020110300004991054018605017364088147",  \
          "11030000271013020130300004995055014605517405089258",  \
          "11133100301015020170300004999056010606017446080369",  \
          "11236200331017020200300004000057006606517487081470",  \
          "11339300361019020230300004004058002607017528082581",  \
          "11442400391021020250300004008050000607517569083692",  \
          "11545500421023020270300004012051040608017603084703",  \
          "11648600451025020290300004017052008608517644085814",  \
          "11751700481027020310300004021053012609017685086925",  \
          "11854800511029020330300004025054016609507726087036",  \
          "11958900541031020360300004029055018610007767088147",  \
          "11060000571033020380300004033056030610507808089258",  \
          "11163100601035020410300004037057034611007849080369",  \
          "11266200631037020430300004041058043611507883081470",  \
          "11369300661039020470300004045050041612007924082581",  \
          "11472400691041020500300004048051025612507965083692",  \
          "11575500721043020530300004051052022613507996084703",  \
          "11678600751048021580300004055053013614007337085814"   \
        ]


#---Open file for graphics
wks_type = "png"
wks = Ngl.open_wks(wks_type,"wmstnm03")

#
#  Draw a world map.
#
mpres = Ngl.Resources()
mpres.nglFrame     = False
mpres.mpSatelliteDistF  = 1.3
mpres.mpOutlineBoundarySets  = "USStates"
mpres.mpCenterLatF =  40.
mpres.mpCenterLonF = -97.
mpres.mpCenterRotF =  35.
mpres.mpProjection = "Satellite"
map = Ngl.map(wks,"Satellite",mpres)

#
#  In the middle of Nebraska, draw a wind barb for a north wind
#  with a magnitude of 15 knots.
#
Ngl.wmbarbmap(wks,42.,-99.,0.,-15.)

#
#  Draw the station model data at the selected cities.  The call
#  to wmsetp informs wmstnm that the wind barbs will be drawn over
#  a map.  To illustrate the adjustment for plotting the model
#  data over a map, all winds are from the north.
#
Ngl.wmsetp("ezf",1)
Ngl.wmstnm(wks,city_lats,city_lons,imdat)

Ngl.frame(wks)
Ngl.end()