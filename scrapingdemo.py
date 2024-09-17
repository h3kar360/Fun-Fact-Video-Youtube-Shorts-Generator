import requests
from gtts import gTTS
import os

# limit = 3
# api_url = 'https://api.api-ninjas.com/v1/facts'
# response = requests.get(api_url, headers={'X-Api-Key': 'A58p2qySrkVl5IevVv9iUw==DEQRx34va7nznCTl'})
# if response.status_code == requests.codes.ok:
#     data = response.json()
# else:
#     print("Error:", response.status_code, response.text)

# fact = data[0]["fact"]

# splitStr = fact.split(' ')
# newSplit = []
# for i in range(0, len(splitStr)):
#     newSplit.append(splitStr[i])
#     if (i+1)%10 == 0:
#         newSplit.append('\n')
    
# combinedSplit = ' '.join(newSplit)
# print(combinedSplit)

def findLenFact():
    api_url = 'https://api.api-ninjas.com/v1/facts'
    response = requests.get(api_url, headers={'X-Api-Key': 'A58p2qySrkVl5IevVv9iUw==DEQRx34va7nznCTl'})
    if response.status_code == requests.codes.ok:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)

    fact = data[0]["fact"]   

    if len(fact) >= 10:
        splitStr = fact.split(' ')
        newSplit = []
        for i in range(0, len(splitStr)):
            newSplit.append(splitStr[i])
            if (i+1)%4 == 0:
                newSplit.append('\n')
    
        combinedSplit = ' '.join(newSplit)
        return combinedSplit
    else:
        return findLenFact()
    
print(findLenFact())