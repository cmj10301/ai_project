// app/api/sketch/route.js

export async function POST(req) {
  const body = await req.json();

  const response = await fetch('http://localhost:8000/sketch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  const result = await response.json();
  return new Response(JSON.stringify(result), {
    status: response.status,
    headers: { 'Content-Type': 'application/json' }
  });
}
