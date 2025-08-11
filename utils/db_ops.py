import firebase_admin
from firebase_admin import credentials, db
import json
import argparse
import numpy as np
import pandas as pd 


class FireBaseActions : 
    def __init__(self, db_url: str, cred_path: str) -> None :
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())
        self.db_url = db_url
        self.cred_path = cred_path 
        self.cred = credentials.Certificate(self.cred_path)
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': self.db_url
        })
        print("fire base initialized successfully...")

    def __load_data(self, data_path: str) -> None :
        with open(data_path, "r") as json_file:
            self.all_company = json.load(json_file) 

    def _push(self, collection_name: str, data_path: str) -> None : 
        self.__load_data(data_path)
        ref = db.reference(collection_name)
        try :
            ref.push(self.all_company)
        except Exception as e : 
            print(e)
        print("="*40)
        print("|| pushed data to firebase db")
        print("="*40)

    def _pull(self, collection_name: str, store_path: str = "data/all_company.json") -> None :
        ref = db.reference(collection_name)
        data = ref.get()
        with open(store_path, "w") as json_file:
            json.dump(data[list(data.keys())[0]], json_file)
 
        print("="*40)
        print("|| pulled from firebase db")
        print("="*40)

def main():
    parser = argparse.ArgumentParser(description="Firebase pull/push script")

    parser.add_argument("--db_url", required=True, help="Firebase Realtime DB URL")
    parser.add_argument("--cred_path", required=True, help="Path to Firebase service account JSON")
    parser.add_argument("--operation", choices=["pull", "push"], required=True, help="Operation to perform")
    parser.add_argument("--collection_name", required=True, help="Collection name in Firebase")
    parser.add_argument("--data_path", help="Local path for data to push or save") 

    args = parser.parse_args()
    db_obj = FireBaseActions(
        db_url=args.db_url,
        cred_path=args.cred_path
    )

    if args.operation == "push":
        if not args.data_path:
            raise ValueError("For push operation, --data_path is required.")
        db_obj._push(
            collection_name=args.collection_name,
            data_path=args.data_path
        )
    else:  # pull
        db_obj._pull(
            collection_name=args.collection_name,
            data_path=args.data_path 
        )

if __name__ == "__main__":
    main()