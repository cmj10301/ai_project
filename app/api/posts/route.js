// ai_project/app/api/posts/route.js
import { connectDB } from "@/backend/mongoDBConnect.js"

export async function GET() {
  const client = await connectDB
  const db = client.db("ai_service")
  const posts = await db.collection("post").find().toArray()

  return new Response(JSON.stringify(posts ?? []), {
    headers: { "Content-Type": "application/json" },
    status: 200
  });
}
