'use client'

import { useEffect, useState } from 'react'

export default function HistoryPage() {
  const [history, setHistory] = useState([])

  useEffect(() => {
    const listener = (event) => {
      if (event.source !== window || event.data?.type !== 'FROM_EXTENSION') return;
      setHistory(event.data.payload || []);
    };

    window.addEventListener("message", listener);
    return () => window.removeEventListener("message", listener);
  }, [])

  return (
    <main style={{ padding: 20 }}>
      <h2>🧠 최근 검색 기록 (브라우저에서 가져옴)</h2>
      {history.length === 0 ? (
        <p>확장 프로그램을 통해 데이터를 가져와주세요.</p>
      ) : (
        <ul>
          {history.map((item, idx) => (
            <li key={idx} style={{ marginBottom: 5 }}>
              <strong>{item.title}</strong><br />
              <small>{item.url}</small>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
