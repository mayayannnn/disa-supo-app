from database import db
from database import User

from database import Shelter

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

