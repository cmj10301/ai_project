'use client'

import { useRef, useState } from 'react';

export default function AiSketchPage() {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [mode, setMode] = useState('draw'); // 'draw' or 'erase'
  const [result, setResult] = useState(null);

  const startDraw = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    setIsDrawing(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = mode === 'draw' ? 'black' : 'white';
    ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    ctx.stroke();
  };

  const endDraw = () => {
    setIsDrawing(false);
  };

  const handleSubmit = async () => {
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL('image/png');
    
    const res = await fetch('/api/sketch', {
      method: 'POST',
      body: JSON.stringify({ image: imageData }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    setResult(data.prediction); // 예: "banana"
  };

  const handleAnswer = (isCorrect) => {
    alert(isCorrect ? '정답으로 확인되었습니다!' : '다시 학습에 반영하겠습니다.');
    // 여기에 FastAPI로 feedback 보내기 가능
    setResult(null);
  };

  return (
    <div className="container py-4 text-center">
      <h2>AI 스케치</h2>
      <canvas
        ref={canvasRef}
        width={300}
        height={300}
        style={{ border: '1px solid #000', background: '#fff', cursor: 'crosshair' }}
        onMouseDown={startDraw}
        onMouseMove={draw}
        onMouseUp={endDraw}
        onMouseLeave={endDraw}
      />
      <div className="my-2">
        <button className="btn btn-secondary me-2" onClick={() => setMode('draw')}>연필</button>
        <button className="btn btn-secondary me-2" onClick={() => setMode('erase')}>지우개</button>
        <button className="btn btn-primary" onClick={handleSubmit}>제출하기</button>
      </div>

      {result && (
        <div className="mt-4">
          <p>🤖 AI의 추론: <strong>{result}</strong></p>
          <button className="btn btn-success me-2" onClick={() => handleAnswer(true)}>맞아요</button>
          <button className="btn btn-danger" onClick={() => handleAnswer(false)}>아니에요</button>
        </div>
      )}
    </div>
  );
}
