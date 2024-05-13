import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from random import randint
from tinyec import registry
from ecc import field
from Crypto.Hash import SHA256
import netifaces
import requests
#Select an elliptic curve for the ECC-based protocol
samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)
def get_mac_address(interface="eth0"):
    mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    mac_address_bytes = bytes.fromhex(mac_address.replace(":", ""))
    return mac_address_bytes

#Gen key pair
mac_address = get_mac_address()
print(mac_address)
cid = input('Enter collector ID:')
di = SHA256.new(cid.encode() + mac_address).digest()
di = int.from_bytes(di, byteorder='big')
Di = di * curve.g
print(Di.x, Di.y)
'''
# Định nghĩa URL mục tiêu và dữ liệu để gửi
url = 'http://127.0.0.1:8000/collectors'
data = {
  "Collector_id": cid,
  "Di_x": str(Di.x),
  "Di_y": str(Di.y)
}
# Thực hiện yêu cầu POST
response = requests.post(url, json=data)

# Kiểm tra mã trạng thái của phản hồi
if response.status_code == 200:
    print("Yêu cầu POST thành công!")
    print("Nội dung phản hồi:", response.json())
else:
    print("Yêu cầu POST không thành công. Mã trạng thái:", response.status_code)

def rec_response(response):
    return response.json()
    '''