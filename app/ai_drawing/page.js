'use client'

import { useRef, useState } from 'react';

export default function AiSketchPage() {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [mode, setMode] = useState('draw');
  const [result, setResult] = useState(null);
  const [correctLabel, setCorrectLabel] = useState('');
  const [isCorrect, setIsCorrect] = useState(null);

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

    const res = await fetch('http://localhost:8000/api/sketch', {
      method: 'POST',
      body: JSON.stringify({ image: imageData }),
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await res.json();
    setResult(data.prediction);
    setIsCorrect(null);
  };

  const handleAnswer = async (answer) => {
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL('image/png');
    const isAnswerCorrect = answer === 'yes';

    try {
      const res = await fetch('http://localhost:8000/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image: imageData,
          prediction: result,
          is_correct: isAnswerCorrect,
          correct_label: !isAnswerCorrect ? correctLabel : null
        })
      });

      if (!res.ok) {
        throw new Error('서버 저장 실패');
      }

      alert(isAnswerCorrect ? '정답으로 확인되었습니다!' : '오답 정보가 저장되었습니다.');
      setResult(null);
      setCorrectLabel('');
      setIsCorrect(null);
    } catch (err) {
      alert('오답 저장 중 문제가 발생했습니다. 다시 시도해주세요.');
    }
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
          <button className="btn btn-success me-2" onClick={() => handleAnswer('yes')}>맞아요</button>
          <button className="btn btn-danger me-2" onClick={() => setIsCorrect(false)}>아니에요</button>

          {isCorrect === false && (
            <div className="mt-2">
              <input
                type="text"
                placeholder="정답을 입력하세요 (예: dog)"
                value={correctLabel}
                onChange={(e) => setCorrectLabel(e.target.value)}
                className="form-control mt-2"
              />
              <button className="btn btn-primary mt-2" onClick={() => handleAnswer('no')}>정답 제출</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
