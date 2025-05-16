import firebase_admin
from firebase_admin import credentials

cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred, {
    "projectId": "nabi-7db09",
    "databaseURL": "https://nabi-7db09-default-rtdb.asia-southeast1.firebasedatabase.app"

})
