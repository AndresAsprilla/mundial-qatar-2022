import requests
import json

def getCalendar():
    with open(f'/home/valoraanalitik/public_html/mundial/json/transmision.json') as jsonFile:
            tv  = json.load(jsonFile)
            jsonFile.close()


    result = {'partidos':[]}
    url2 = 'https://api.fifa.com/api/v3/calendar/matches?idseason=255711&idcompetition=17&language=es-ES&count=100'
    response = requests.get(url2)
    jsondata = json.loads(response.content)
    for i in jsondata['Results']:
        if i['Home']:
            if i['Away']:

                cast = str(i['MatchNumber'])
                result['partidos'].append({"fecha": i['Date'],
                                        "numero": i['MatchNumber'], 
                                        "fase": i['StageName'][0]['Description'], 
                                        #"grupo": i['GroupName'][0]['Description'], 
                                        "local": {"nombre": i['Home']['TeamName'][0]['Description'],
                                                "abreviacion":i['Home']['IdCountry']}, 
                                        "visitante": {"nombre": i['Away']['TeamName'][0]['Description'],
                                                    "abreviacion":i['Away']['IdCountry']},
                                        "estado": i['MatchStatus'],
                                        "tiempo": i['MatchTime'],
                                        "marcador":{"local": i['HomeTeamScore'],
                                                    "visitante": i['AwayTeamScore']},
                                        "transmision":tv['partidos'][cast]
                                        })
            else:
                cast = str(i['MatchNumber'])
                result['partidos'].append({"fecha": i['Date'],
                                        "numero": i['MatchNumber'], 
                                        "fase": i['StageName'][0]['Description'], 
                                        #"grupo": i['GroupName'][0]['Description'], 
                                        "local": {"nombre": i['Home']['TeamName'][0]['Description'],
                                                "abreviacion":i['Home']['IdCountry']}, 
                                        "visitante": {"nombre": i['PlaceHolderB'], 
                                                  "abreviacion": "dontflag" },
                                        "estado": i['MatchStatus'],
                                        "tiempo": i['MatchTime'],
                                        "marcador":{"local": i['HomeTeamScore'],
                                                    "visitante": i['AwayTeamScore']},
                                        "transmision":tv['partidos'][cast]
                                        })

        else:
          cast = str (i['MatchNumber'])
          result['partidos'].append({"fecha": i['Date'],
                                    "numero": i['MatchNumber'], 
                                    "fase": i['StageName'][0]['Description'], 
                                    "local": {"nombre": i['PlaceHolderA'], 
                                              "abreviacion": "dontflag"}, 
                                    "visitante": {"nombre": i['PlaceHolderB'], 
                                                  "abreviacion": "dontflag" },
                                    "estado": i['MatchStatus'],
                                    "tiempo": i['MatchTime'],
                                    "marcador":{"local": i['HomeTeamScore'],
                                                "visitante": i['AwayTeamScore']},
                                    "transmision":tv['partidos'][cast]
                                    
                                    })                              
        
    
    return result


import requests
import json


def standings():
    with open(f'/home/valoraanalitik/public_html/mundial/json/traduction.json') as jsonFile:
     tr  = json.load(jsonFile)
     jsonFile.close()
    
    stand = {"A":[],"B":[],"C":[],"D":[],"E":[],"F":[],"G":[],"H":[]}
    groups = ["A","B","C","D","E","F","G","H"]

    url ="http://api.cup2022.ir/api/v1/user/login"
    val = {"email": "fasprilla@grupovalora.com.co","password": "123456789"}
    body = requests.post(url, json=val)
    json_token = json.loads(body.content)
    for k in groups:
        url ="http://api.cup2022.ir/api/v1/standings/"+ k
        headers={'Authorization':'Bearer ' + json_token["data"]["token"]}

        resp = requests.get(url,headers=headers)
        json_data = json.loads(resp.content)

        #print(json_data["data"][0]["teams"])

        for i in json_data["data"][0]["teams"]:
            #print(i)
            item ={"nombre": tr["equipos"][i["name_en"]]["nombre"] , "abreviacion": tr["equipos"][i["name_en"]]["abreviacion"] , "jugados": i["mp"], "ganados": i["w"], "empatados": i["d"], "perdidos": i["l"], "diferencia": i["gd"], "puntos": i["pts"], "gf": i["gf"], "gc": i["ga"]}
            stand[k].append(item)
    return stand



#Create JSON File
def rightFormatJson(realJson,name):
    with open(f'/home/valoraanalitik/public_html/mundial/json/{name}.json', 'w') as file:
        json.dump(realJson ,file, indent=4)
        file.close()

#results = standings()
partidos = getCalendar()
rightFormatJson(partidos,"partidos") 
#rightFormatJson(results,"standings")           
