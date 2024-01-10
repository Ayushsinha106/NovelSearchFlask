from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['POST'])
def post_data():
    data1 = request.get_json()

    name = data1['key1']
    name= name.replace(" ", "+")
    url = f"https://allnovelbook.com/search?q={name}"
    print(url)
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    div_element = doc.find('div', class_='special')
    print(div_element!=None)
    print(div_element)
    if div_element !=None:        
        NovelLink = div_element.find_all('a')
        data={
            "result":[]
        }
        for a in NovelLink:
            img = a.find('img')
            if img:
                items = {
                    "title": a['title'],
                    "url": a['href'],
                    "img":img['data-src']
                }
                data['result'].append(items)
        next = div_element.find('ul', class_="pagination")
        if next:
            numList = next.find_all("a", class_="page-link")
            num = [p.text for p in numList]
            val = len(num)
            i=0
            while i<val-1:
                if i==int(num[-2]):
                    break
                a = int(num[i])
                url =f"https://allnovelbook.com/search?q={name}&page={num[i]}"
                response = requests.get(url)
                doc = BeautifulSoup(response.text, "html.parser")
                div_element = doc.find('div', class_='special')
                if div_element:
                    NovelLink = div_element.find_all('a')
                    for a in NovelLink:
                        img = a.find('img')
                        if img:
                            items = {
                                "title": a['title'],
                                "url": a['href'],
                                "img":img['data-src']
                            }
                            data['result'].append(items)
                i+=1
            
    else:
        data ={
            "result":"No results for your search."
        }

    return jsonify(data)

@app.route('/api', methods=['GET'])
def get_data():
    data = {'message': 'Hello, this is a GET request'}

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)
