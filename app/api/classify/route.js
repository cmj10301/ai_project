// app/api/classify/route.js
import { NextResponse } from 'next/server'

export async function POST(req) {
  const { text } = await req.json()

  const res = await fetch('http://localhost:8000/api/classify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })

  const result = await res.json()
  return NextResponse.json(result)
}
