from bs4 import BeautifulSoup
import requests
from flask import Flask,jsonify,session
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def extract_table_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    headers = [header.get_text(strip=True) for header in soup.find_all('th')]

    for row in soup.find_all('tr')[1:]:
        row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
        data=(dict(zip(headers, row_data)))
    checksum_status = data.get("Checksum Status")
    if checksum_status == "Valid Checksum":
        data["Checksum Status"] = "true"
    else:
        data["Checksum Status"] = "false"
    return data

def getValid(gstno):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://gstserver.com',
        'Connection': 'keep-alive',
        'Referer': 'https://gstserver.com/gstnumbervalidator/',
        # 'Cookie': '_ga_2RXB4P5EZL=GS1.1.1691055092.1.1.1691055333.60.0.0; _ga=GA1.2.77717361.1691055093; _gid=GA1.2.405234940.1691055093; __gads=ID=d32d3c3d6322087b-222f927db9e7003d:T=1691055094:RT=1691055094:S=ALNI_Ma0iwGF-gMe6bXvd5Vw18IVXyGCvA; __gpi=UID=00000c2696dc5427:T=1691055094:RT=1691055094:S=ALNI_MYgg4eY213m4OqHEeWNTMXfcYpR0Q; _gat_gtag_UA_120501355_1=1',
        # 'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {
        'gstnos': gstno,
        'button': 'Submit',
    }

    response = requests.post('https://gstserver.com/gstnumbervalidator/', headers=headers, data=data)
    return extract_table_data(response.text)
@app.route('/validgst/<string:gstNum>')
def index(gstNum):
    return jsonify(getValid(gstNum))
app.run(host='0.0.0.0', port=81)
# app.run(debug=True)