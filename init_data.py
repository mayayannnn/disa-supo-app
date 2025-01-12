from database import db
from database import User
from database import Shelter
from database import Hospital
from database import Pharmacy
from database import ReliefSupplies
from database import ReliefSuppliesCategory


def init_shelter_data():
    shelters = [
        {
            'name': '盛岡市総合アリーナ',
            'Latitude': '39.701431',
            'Longitude': '141.136015',
            'category': '指定避難所',
            'capacity': '1000',
            'phone_number': '019-601-5700'
        },
        {
            'name': '岩手県営体育館', 
            'Latitude': '39.703947',
            'Longitude': '141.152170',
            'category': '指定避難所',
            'capacity': '800',
            'phone_number': '019-637-2111'
        },
        {
            'name': '盛岡市立上田中学校体育館',
            'Latitude': '39.718760', 
            'Longitude': '141.147015',
            'category': '指定避難所',
            'capacity': '500',
            'phone_number': '019-623-4237'
        }
    ]
        # データベースに登録
    for shelter in shelters:
        Shelter.create(**shelter)

def init_hospital_data():
    hospitals = [
        {
            'name': '盛岡市立病院',
            'Latitude': '39.690316877806225',
            'Longitude': '141.12467815042243',
            'category': '総合病院',
            'capacity': '1000',
            'phone_number': '019-635-0101'
        },
        {
            'name': 'おはようクリニック内科整形外科', 
            'Latitude': '39.72572973222641',
            'Longitude': '141.13576248060795',
            'category': 'クリニック・医院・診療所',
            'capacity': '800',
            'phone_number': '019-662-0840'
        },
        {
            'name': '松園第二病院',
            'Latitude': '39.756606211877546', 
            'Longitude': '141.1627650170758',
            'category': '総合病院',
            'capacity': '500',
            'phone_number': '019-662-0100'
        }
    ]

    # データベースに登録
    for hospital in hospitals:
        Hospital.create(**hospital)



def init_pharmacy_data():
    pharmacies = [
        {
            'name': 'かえで薬局',
            'Latitude': '39.736019243138124',
            'Longitude': '141.14373533700808',
            'category': '調剤薬局',
            'capacity': '1000',
            'phone_number': '019-656-1493'
        },
        {
            'name': 'しんせい薬局', 
            'Latitude': '39.73133940827187',
            'Longitude': '141.15300194111077',
            'category': '調剤薬局',
            'capacity': '800',
            'phone_number': '019-663-2366'
        },
        {
            'name': 'ツルハドラッグ黒石野店',
            'Latitude': '39.74164729264911', 
            'Longitude': '141.1458998201698',
            'category': 'ドラッグ ストア',
            'capacity': '500',
            'phone_number': '019-681-9887'
        }
    ]

    # データベースに登録
    for pharmacy in pharmacies:
        Pharmacy.create(**pharmacy)

def init_reliefsupplies_data():
    reliefsupplies = [
        {
            "shelter_id":1,
            "reliefsuppliescategory_id":1,
            "required_number":100,
            "used_number":80
        },
                {
            "shelter_id":1,
            "reliefsuppliescategory_id":2,
            "required_number":10,
            "used_number":3
        },
                {
            "shelter_id":2,
            "reliefsuppliescategory_id":1,
            "required_number":85,
            "used_number":23
        }

    ]
    for reliefsuppli in reliefsupplies:
        Pharmacy.create(**reliefsuppli)

def init_reliefsuppliescategory_date():
    reliefsuppliescategories = [
        {
            "name" : "水"
        },
        {
            "name" : "米"
        }
        
    ]
    for reliefsuppliescategory in reliefsuppliescategories:
        Pharmacy.create(**reliefsuppliescategory)