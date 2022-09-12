import json as jn
import os
from BD.classes import Resposta

class Json:
    def __init__(self):
        caminho = os.path.dirname(os.path.abspath(__file__))
        self.caminhoJson = f"{caminho}/respostas.json" 

    def setResposta(self, questao, fase, text):
        with open(self.caminhoJson, "r+") as jsonFile:
            objJson = jn.load(jsonFile)
            
            if questao == 7:
                numResp = 1
                for x in text:
                    objJson[f"Fase{fase}"][f"Questao{questao}"][f"Resposta{numResp}"] = x
                    numResp += 1
            else:
                text = text[3:]
                objJson[f"Fase{fase}"][f"Questao{questao}"]["Resposta"] = text

            jsonFile.seek(0)
            jn.dump(objJson, jsonFile, indent=4)
            jsonFile.truncate()
    
    def insereReposta(self):
        with open(self.caminhoJson, "r+") as jsonFile:
            objJson = jn.load(jsonFile)

            questFase1 = 1
            for x in objJson["Fase1"]:
                print(objJson["Fase1"][x]["Resposta"])
                Resposta.insert_resposta(objJson["Fase1"][x]["Resposta"], questFase1)
                questFase1 += 1

            questFase2 = 1
            for x in objJson["Fase2"]:
                print(x)
                if x == "Questao7":
                    for y in range(1, 7):
                        print(objJson["Fase2"][x][f"Resposta{y}"])
                        Resposta.insert_resposta(objJson["Fase2"][x][f"Resposta{y}"], questFase2)
                else:
                    print(objJson["Fase2"][x]["Resposta"])
                    Resposta.insert_resposta(objJson["Fase2"][x]["Resposta"], questFase2)

                questFase2 += 1
