from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://tadahiroueta:vJxZGMbvLlt8UjMU@twitter-trend-cluster.qkopkvi.mongodb.net/?retryWrites=true&w=majority")
    print("Connected to MongoDB")

except:
    print("Failed to connect to MongoDB")
    quit()

database = client["subscriptions"]
collection = database["main"]

def getSubscriptions():
    """
    Returns:
        List of subscriptions (e.g. {
            "email": str
            "hashtag": str
            "standardAlgorithm": bool
            "dailyEmail: bool
        }).
    """
    return collection.find()
