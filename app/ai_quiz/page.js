'use client';

import { useState } from 'react';

export default function AiGuessPage() {
  const [messages, setMessages] = useState([
    { from: 'ai', text: '당신이 생각한 동물의 특징을 알려주세요.' }
  ]);
  const [input, setInput] = useState('');
  const [aiGuess, setAiGuess] = useState('');
  const [showGuess, setShowGuess] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    const userText = input.trim();
    if (!userText) return;

    // 사용자 응답 표시
    setMessages(prev => [...prev, { from: 'user', text: userText }]);
    setInput('');

    // 서버에 전달
    const res = await fetch('/api/guess', {
      method: 'POST',
      body: JSON.stringify({ user_input: userText }),
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await res.json();

    if (data.guess) {
      setAiGuess(data.guess);
      setShowGuess(true);
    } else {
      setMessages(prev => [...prev, { from: 'ai', text: data.next_question }]);
    }
  };

  const handleFeedback = async (isCorrect) => {
    await fetch('/api/feedback', {
      method: 'POST',
      body: JSON.stringify({ guess: aiGuess, correct: isCorrect }),
      headers: { 'Content-Type': 'application/json' }
    });
    alert(isCorrect ? 'AI가 맞췄어요!' : '틀렸지만, 더 똑똑해질게요.');

    // 상태 초기화
    setMessages([{ from: 'ai', text: '다시 시작해볼까요? 어떤 동물을 생각하셨나요?' }]);
    setAiGuess('');
    setShowGuess(false);
  };

  return (
    <div className="container py-4">
      <h2 className="text-center">🧠 스무고개 AI</h2>

      {/* 대화 내역 */}
      <div className="border rounded p-3 mb-3" style={{ height: '300px', overflowY: 'auto' }}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`text-${msg.from === 'ai' ? 'primary' : 'dark'} mb-2`}>
            <strong>{msg.from === 'ai' ? '🤖 AI' : '🙋 사용자'}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {/* 입력창 */}
      {!showGuess && (
        <form onSubmit={sendMessage} className="d-flex align-items-center gap-2 mt-3">
          <input
            className="form-control"
            placeholder="특징을 자연어로 입력하세요. 예: 물속에서 살아요, 초식이에요"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            className="btn btn-primary"
            type="submit"
            style={{ whiteSpace: 'nowrap', minWidth: '80px' }}
          >
            전송
          </button>
        </form>
      )}

      {/* 최종 추론 결과 */}
      {showGuess && (
        <div className="mt-4 text-center">
          <p>🤖 AI의 추측: <strong>{aiGuess}</strong></p>
          <button className="btn btn-success me-2" onClick={() => handleFeedback(true)}>맞아요</button>
          <button className="btn btn-danger" onClick={() => handleFeedback(false)}>아니에요</button>
        </div>
      )}
    </div>
  );
}
