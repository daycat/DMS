import requests
import gzip
import shutil
import os
print("Now download GeoLite2-ASN.mmdb")
r = requests.get("https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-ASN&license_key=smjmb9lr1MyqdoFK&suffix=tar.gz")
open("GeoLite2-ASN.mmdb.gz", 'wb').write(r.content)
print("Download complete")
print("Now decompress GeoLite2-ASN.mmdb.gz")
with gzip.open('GeoLite2-ASN.mmdb.gz', 'rb') as f_in:
    with open('GeoLite2-ASN.mmdb', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
print("Decompress complete")
print("Now delete GeoLite2-ASN.mmdb.gz")
os.remove("GeoLite2-ASN.mmdb.gz")
print("Delete complete")
print("Now download GeoLite2-City.mmdb")
r = requests.get("https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=smjmb9lr1MyqdoFK&suffix=tar.gz")
open("GeoLite2-City.mmdb.gz", 'wb').write(r.content)
print("Download complete")
print("Now decompress GeoLite2-City.mmdb.gz")
with gzip.open('GeoLite2-City.mmdb.gz', 'rb') as f_in:
    with open('GeoLite2-City.mmdb', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
print("Decompress complete")
print("Now delete GeoLite2-City.mmdb.gz")
os.remove("GeoLite2-City.mmdb.gz")
print("Delete complete")
