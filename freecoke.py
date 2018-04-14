import requests,time,re

#curl 'https://survey.fast-insight.com/mcd/germany/mcd_de_voucher2.php' -H 'Host: 
#survey.fast-insight.com' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 
#Firefox/57.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 
#'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: 
#https://portal.fast-insight.com/document.asp?alias=surveo.bootstrap&project=14d57c&code=&blankedLayout=1' 
#-H 'Content-Type: application/x-www-form-urlencoded' -H 'Cookie: testcookie=testvalue; 
#VOC_id=de_5a89a8ba953d9; PHPSESSID=sl63vga19s63eacv12s0m7tta6; VOC_finished_d=2018-02-18; 
#VOC_finished_t=17%3A25%3A25' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' 
#--data 
#'lang=de&store_id=0506&screenwidth=1366&screenheight=768&colorDepth=undefined&pixelDepth=24&availWidth=1366&availHeight=741&IP=46.246.43.232&browserLANG=en&deviceType=computer&browser=Firefox&version=57.0&platform=Linux&surveyform=172&identifier=de_5a89a8ba953d9&promo=bb8jw08by0cf&code=undefined'

def toStr(n,base):
  convertString = "0123456789abcdefghijklmnopqrstuvwxyz"
  if n < base:
    return convertString[n]
  else:
    return toStr(n//base,base) + convertString[n%base]

s = requests.Session()

restaurantId = '0801' # next to CCL in Leipzig...
posId = '04' # self order
orderId = '12' # last two digits of order number
magicNumber = time.strftime(restaurantId + "%m%d%H%M" + posId + orderId + "10")

charset = '0123456789abcdefghijklmnopqrstuvwxyz'
key = 'byebyemysteryshopping'
matrix = [ [ None for y in range( len(charset) ) ] for x in range( len(charset) ) ]  # viginiere matrix

# Generate viginiere matrix
for i in range(0, len(charset)):
  counter = i
  for j in range(0, len(charset)):
    matrix[i][j] = charset[counter % len(charset)]
    counter += 1

plaintext = '0' + toStr(int(magicNumber), 36);
accessCode = ''

for i in range(0, len(plaintext)):
  a = charset.index(plaintext[i])
  b = charset.index(key[i % len(key)])
  accessCode += matrix[a][b]

print(accessCode)

headers = {
  'Host' : 'survey.fast-insight.com',
  'User-Agent' : 'you are still not learning it',
  'Referer' : 'https://portal.fast-insight.com/document.asp?alias=surveo.bootstrap&project=14d57c&code=&blankedLayout=1',
  'Content-Type' : 'application/x-www-form-urlencoded'
}

payload = {
  'screenwidth' : 1366,
  'screenheight' :  768,
  'colorDepth' :  24,
  'pixelDepth' :  24,
  'availWidth' :  1366,
  'availHeight' : 741,
  'date' : '18+02+2018',
  'time' : '19:25:46'
}

result = s.post('https://survey.fast-insight.com/mcd/germany/index.php', data=payload);
identifier = re.findall(r"&identifier=([_a-z0-9]*)&", result.text)[0]
print(identifier);

payload = {
  'lang' : 'de',
  'store_id' : restaurantId,
  'screenwidth' : 1366,
  'screenheight' :  768,
  'colorDepth' :  24,
  'pixelDepth' :  24,
  'availWidth' :  1366,
  'availHeight' : 741,
  'IP' : '46.246.43.232',
  'browserLANG' : 'en',
  'deviceType' : 'hackintosh',
  'browser' : 'Netscape',
  'version' : '1.0',
  'platform' : 'OpenBSD',
  'surveyForm' : '172',
  'identifier' : identifier,
  'promo' : accessCode,
  'code' : 'undefined',
  'alias' : 'mcd-germany-live'
}

s.get('https://survey.fast-insight.com/mcd/germany/mcd_de_sc.php')
s.headers.update({  'Referer' : 'https://portal.fast-insight.com/document.asp?alias=surveo.bootstrap&project=14d57c&code=&blankedLayout=1' })
result = s.post('https://survey.fast-insight.com/mcd/germany/mcd_de_voucher2.php', data=payload)

print(result.text.encode('utf8'))
