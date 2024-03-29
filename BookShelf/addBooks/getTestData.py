import requests, random, json, sys, re, datetime

sys.path.append('../')
from bookList.models import book

uri = 'https://api.openbd.jp/v1/get?isbn='


def createData():
    i = 0
    j = 0
    pubList = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "12", "13", "14", "15", "16", "19",
               "253", "255", "257", "262", "265", "272", "273", "275", "277", "309", "314", "323", "324", "326", "329",
               "331", "333", "334", "336", "338", "344", "384", "385", "387", "390", "396", "403", "404", "409", "408",
               "413", "415", "418", "422", "423", "426", "434", "471", "472", "473", "474", "478", "479", "480", "487",
               "488", "492", "529", "532", "534", "537", "540", "560", "566", "568", "569", "575", "576", "577", "579",
               "582", "584", "586", "588", "591", "592", "594", "579", "620", "621", "622", "624", "634", "635", "636",
               "638", "642", "643", "651", "657", "7515", "7551", "7561", "7569", "7571", "7572", "7574", "7575",
               "7577", "7601", "7630", "7631", "7637", "7641", "7642", "7660", "7664", "7669", "7674", "7713", "7735",
               "7741", "7744", "7826", "7828", "7837", "7845", "7853", "7872", "7885", "7890", "7897", "7906", "7916",
               "7917", "7942", "7949", "7952", "7958", "7962", "7966", "7967", "7973", "7980", "7981", "8056", "8062",
               "8067", "8072", "8103", "8104", "8108", "8118", "8120", "8158", "8163", "8184", "8211", "8288", "8315",
               "8332", "8340", "8343", "8379", "8387", "8398", "8399", "8401", "8402", "8421", "8443", "8451", "8457",
               "8458", "86002", "86029", "86152", "87013", "87025", "87031", "87043", "87110", "87198", "87233",
               "87275", "87278", "87283", "87287", "87290", "87366", "87376", "87465", "87502", "87697", "87698",
               "87719", "87728", "87738", "87746", "87771", "87792", "87893", "87919", "87995", "88008", "88108",
               "88112", "88284", "88309", "88337", "88338", "88475", "88595", "88653", "88706", "88713", "88721",
               "88724", "88745", "88914", "89036", "89194", "89215", "89309", "89393", "89419", "89434", "89436",
               "89486", "89544", "89637", "89642", "89691", "89694", "89737", "89799", "89815", "89777", "89977",
               "901142", "901706", "901917", "906496", "906443", "906576", "900757", "900874", "906011", "907818",
               "915146", "915497", "915512", "924684", "925235", "930787", "931246", "938165", "938339", "938463",
               "938508", "938706", "938733", "939029", "939111", "939115", "944098", "944154", "944236", "946483",
               "9901097"]
    digit = 8  # 桁数
    while i < 100:
        index = random.randint(0, pubList.__len__()-1)
        ranDigit = digit - pubList[index].__len__()
        isbn = random.randrange(10 ** (ranDigit - 1), 10 ** ranDigit)
        response = requests.get(uri + createParity('9784' + pubList[index] + str(isbn)))
        print(response.text + str(j) + "-" + str(i))
        if not response.text == '[null]' and str(response.status_code) == "200":
            jsonData = json.loads(response.text)
            summary = jsonData[0]["summary"]

            genreList = {0, 'onix', 'DescriptiveDetail', 'Subject', 0, 'SubjectCode'}
            if checkJson(jsonData,genreList):
                genre = jsonData[0]['onix']['DescriptiveDetail']['Subject'][0]['SubjectCode']
            else:
                genre = None

            textList = {0, 'onix', 'CollateralDetail', 'TextContent', 0, 'Text'}
            if checkJson(jsonData, textList):
                text = jsonData[0]['onix']['CollateralDetail']['TextContent'][0]['Text']
            else:
                text = None

            priceAmountList = {0, 'onix', 'ProductSupply', 'SupplyDetail', 'Price', 0}
            if checkJson(jsonData, priceAmountList):
                priceAmount = jsonData[0]['onix']['ProductSupply']['SupplyDetail']['Price'][0]
            else:
                priceAmount = None

            addData(summary, genre, text, priceAmount)
            i += 1
        j += 1


def checkJson(json_dict, keys):
    key = keys.pop(0)
    if type(key) is int:
        if len(json_dict) > 0:
            if len(keys) > 0:
                return checkJson(json_dict[key], keys)
            else:
                return True
        else:
            return False
    else:
        if key in json_dict:
            if len(keys) > 0:
                return checkJson(json_dict[key], keys)
            else:
                return True
        else:
            return False


def createParity(strings):
    char_list = list(strings)
    i = 0
    count = 1
    for char in char_list:
        if count % 2 == 1:
            i += int(char)
        else:
            i += int(char)*3
        count += 1
    i = i % 10
    if not i == 0:
        i = 10 - i
    strings += str(i)
    return strings


def addData(summary, genre, text, price_amount):
    count = summary["pubdate"].count('-')
    dateStr = re.sub("\\D", "", summary["pubdate"])
    if dateStr.__len__() == 4:
        dateStr += "01"
    if dateStr.__len__() == 6 and not count == 2:
        dateStr += "01"
    dateTimes = datetime.datetime.strptime(dateStr, '%Y%m%d')

    if book.objects.filter(isbn=summary["isbn"]).exists():
        books = book.objects.get(isbn=summary["isbn"])
        books.picture_name = summary["cover"]
        books.title = summary["title"]
        books.author = summary["author"]
        books.publisher = summary["publisher"]
        books.pubdate = dateTimes
        books.genre = genre
        books.text = text
        books.price = price_amount
        message = 'update Book'

    else:
        books = book(isbn=summary["isbn"], picture_name=summary["cover"],
                     title=summary["title"], author=summary["author"],
                     publisher=summary["publisher"], pubdate=dateTimes, genre=genre, text=text, price=price_amount)
        message = 'add Book'

    print(message)
    books.save()
