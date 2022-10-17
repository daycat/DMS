from flask import Flask, request, jsonify
from ipaddress import ip_address, IPv4Address
import maxminddb
import json
import requests
import string
import random
zoneid = "your-domain-zone-id"
yourdomain = "your-domain"

cloudflare_headers = {
    'X-Auth-Email': 'your_email',
    'X-Auth-Key': 'your_cloudflare_token',
}
app = Flask(__name__)


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/api/v1/', methods=['GET', 'POST'])
def api():
    try:
        ip = request.form['ip']
        try:
            if type(ip_address(ip)) == IPv4Address:
                recordtype = 'A'
            else:
                recordtype = 'AAAA'
        except ValueError:
            return jsonify({'success': 'false', 'reason': 'Invalid IP'})
    except:
        try:
            ip = request.args.get('ip')
            try:
                if type(ip_address(ip)) == IPv4Address:
                    recordtype = 'A'
                else:
                    recordtype = 'AAAA'
            except ValueError:
                return jsonify({'success': 'false', 'reason': 'Invalid IP'})
        except:
            return jsonify({'success': 'false', 'reason': 'Invalid IP'})
    with maxminddb.open_database('GeoLite2-ASN.mmdb') as iplookup:
        ipinfo = iplookup.get(ip)
        try:
            asn = ipinfo['autonomous_system_number']
            aso = ipinfo['autonomous_system_organization']
            if asn == 13335:
                return jsonify({'success': 'false', 'reason': 'Warp detected'})
        except TypeError:
            asn = 'N/A'
            aso = 'N/A'
        print(ipinfo)
    with maxminddb.open_database('GeoLite2-City.mmdb') as iplookup:
        try:
            iplocation = iplookup.get(ip)['country']['iso_code']
        except:
            iplocation = 'world'
    with maxminddb.open_database('GeoLite2-City.mmdb') as iplookup:
        try:
            ipcity = iplookup.get(ip)['city']['names']['en']
        except:
            ipcity = 'N/A'
    l2domain_heading = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))
    cloudflare_json_data = {
        'type': recordtype,
        'name': iplocation + '-' + l2domain_heading + '.'+ yourdomain,
        'content': ip,
        'ttl': 60,
        'priority': 10,
        'proxied': False,
    }
    response = requests.post('https://api.cloudflare.com/client/v4/zones/'+zoneid+'/dns_records',
                             headers=cloudflare_headers, json=cloudflare_json_data)
    data = json.loads(response.text)
    print(data)
    return jsonify({'success': 'true', 'domain': data['result']['name'], 'cdn': data['result']['proxied'],
                    'id': data['result']['id'], 'type': data['result']['type'], 'asn': asn, 'org': aso, 'city': ipcity})


@app.route('/api/v1/proxytoggle/', methods=['GET', 'POST'])
def proxytoggle():
    try:
        recordid = request.form['id']
    except:
        try:
            recordid = request.args.get('id')
        except:
            return jsonify({'success': 'false', 'reason': 'Invalid params'})
    try:
        toggle = request.form['toggle']
    except:
        try:
            toggle = request.args.get('toggle')
        except:
            return jsonify({'success': 'false', 'reason': 'Invalid params'})
    if toggle == 'true' or toggle == 'True' or toggle == 'yes' or toggle == 1:
        togglestate = True
    else:
        togglestate = False
    json_data = {
        'proxied': togglestate,
        'Content-Type': 'application/json',
    }
    try:
        response = requests.patch('https://api.cloudflare.com/client/v4/zones/'+zoneid+'/dns_records/' + recordid, headers=cloudflare_headers, json=json_data)
        data = json.loads(response.text)
        print(data)
        if(data['success'] == True):
            return jsonify({'success': 'true', 'proxied': togglestate})
        else:
            return jsonify({'success': 'false', 'reason': 'unknown'})
    except:
        return jsonify({'success': 'false', 'reason': 'unknown'})


@app.route('/api/ipinfo/', methods=['GET', 'POST'])
def ipinfo():
    try:
        ip = request.form['ip']
        try:
            if type(ip_address(ip)) == IPv4Address:
                recordtype = 'A'
            else:
                recordtype = 'AAAA'
        except ValueError:
            return jsonify({'success': 'false', 'reason': 'Invalid IP'})
    except:
        try:
            ip = request.args.get('ip')
            try:
                if type(ip_address(ip)) == IPv4Address:
                    recordtype = 'A'
                else:
                    recordtype = 'AAAA'
            except ValueError:
                return jsonify({'success': 'false', 'reason': 'Invalid IP'})
        except:
            return jsonify({'success': 'false', 'reason': 'Invalid IP'})
    with maxminddb.open_database('GeoLite2-ASN.mmdb') as iplookup:
        ipinfo = iplookup.get(ip)
        try:
            asn = ipinfo['autonomous_system_number']
            aso = ipinfo['autonomous_system_organization']
        except TypeError:
            asn = 'N/A'
            aso = 'N/A'
    with maxminddb.open_database('GeoLite2-City.mmdb') as iplookup:
        print(iplookup.get(ip))
        try:
            iplocation = iplookup.get(ip)['country']['names']['en']
        except:
            iplocation = 'world'
        try:
            ipcity = iplookup.get(ip)['city']['names']['en']
        except:
            ipcity = 'N/A'
        try:
            iptime = iplookup.get(ip)['location']['time_zone']
        except:
            iptime = 'N/A'
        try:
            iporigin = iplookup.get(ip)['registered_country']['names']['en']
        except:
            iporigin = 'N/A'
        try:
            iploc_acc = iplookup.get(ip)['location']['accuracy_radius']
            iploc_lat = iplookup.get(ip)['location']['latitude']
            iploc_lon = iplookup.get(ip)['location']['longitude']
        except:
            iploc_acc = 'N/A'
            iploc_lat = 'N/A'
            iploc_lon = 'N/A'

    return jsonify({'success': 'true', 'asn info': {'asn': asn, 'org': aso},
                    'location': {'city': ipcity, 'country': iplocation, 'timezone': iptime,
                                 'registered country': iporigin},
                    'coordinates': {'latitude': iploc_lat, 'longitude': iploc_lon, 'Accuracy': iploc_acc}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)