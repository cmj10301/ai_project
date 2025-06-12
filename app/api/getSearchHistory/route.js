import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // window → contentScript → 여기서 직접 응답 없음 (브라우저 메모리 기반 전송)
    return NextResponse.json({ message: 'use postMessage only (no DB)' })
  } catch (error) {
    console.error('❌ 오류:', error)
    return NextResponse.json({ error: '에러 발생' }, { status: 500 })
  }
}
