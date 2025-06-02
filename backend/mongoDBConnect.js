//ai_project/backend/mongoDBConnect.js

import { MongoClient } from 'mongodb'

const uri = process.env.MONGODB_URI;
if (!uri) throw new Error("URI가 비어있음");

let client
let connectDB

if (process.env.NODE_ENV === 'development') {
  if (!global._mongoClient) {
    client = new MongoClient(uri);
    global._mongoClient = client.connect()
  }
  connectDB = global._mongoClient
} else {
  client = new MongoClient(uri);
  connectDB = client.connect()
}

export { connectDB }