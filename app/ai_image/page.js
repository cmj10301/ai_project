'use client';

import { useRef, useState } from 'react';

export default function AiImagePage() {
  const [image, setImage] = useState(null);
  const canvasRef = useRef(null);
  const [selection, setSelection] = useState(null);
  const [result, setResult] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [start, setStart] = useState({ x: 0, y: 0 });

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result);
    reader.readAsDataURL(file);
    setSelection(null);
    setResult(null);
  };

  const startSelection = (e) => {
    const rect = e.target.getBoundingClientRect();
    setStart({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
    setIsDragging(true);
  };

  const updateSelection = (e) => {
    if (!isDragging) return;
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setSelection({
      x: Math.min(start.x, x),
      y: Math.min(start.y, y),
      width: Math.abs(x - start.x),
      height: Math.abs(y - start.y),
    });
  };

  const endSelection = () => {
    setIsDragging(false);
  };

  const handleSubmit = async () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { x, y, width, height } = selection;
    const cropped = ctx.getImageData(x, y, width, height);

    const tmpCanvas = document.createElement('canvas');
    tmpCanvas.width = width;
    tmpCanvas.height = height;
    tmpCanvas.getContext('2d').putImageData(cropped, 0, 0);
    const base64 = tmpCanvas.toDataURL();

    const res = await fetch('/api/image', {
      method: 'POST',
      body: JSON.stringify({ image: base64 }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    setResult(data.prediction);
  };

  const handleAnswer = (isCorrect) => {
    alert(isCorrect ? '정답입니다!' : '오답입니다. 학습에 반영하겠습니다.');
    setResult(null);
  };

  return (
    <div className="container py-4 text-center">
      <h2>🖼️ AI 이미지 인식</h2>

      <input type="file" accept="image/*" onChange={handleImageUpload} className="form-control my-3" />
      {/* 안내 문구 */}
      <p className="text-muted mb-2">
        이미지를 업로드하고, 마우스로 <span style={{ color: 'red', fontWeight: 'bold' }}>빨간 박스</span>로 인식할 영역을 드래그하세요.
      </p>

      {image && (
        <>
          {/* 이미지 + 캔버스 영역 */}
          <div className="d-flex flex-column align-items-center">
            <div className="position-relative">
              <canvas
                ref={canvasRef}
                width={300}
                height={300}
                style={{ border: '1px solid #000', background: '#fff', cursor: 'crosshair' }}
                onMouseDown={startSelection}
                onMouseMove={updateSelection}
                onMouseUp={endSelection}
              />
              <img
                src={image}
                alt="업로드된 이미지"
                onLoad={(e) => {
                  const canvas = canvasRef.current;
                  const ctx = canvas.getContext('2d');
                  ctx.clearRect(0, 0, canvas.width, canvas.height);
                  ctx.drawImage(e.target, 0, 0, 300, 300);
                }}
                style={{ display: 'none' }}
              />
              {selection && (
                <div
                  style={{
                    position: 'absolute',
                    top: selection.y,
                    left: selection.x,
                    width: selection.width,
                    height: selection.height,
                    border: '2px solid red',
                    pointerEvents: 'none'
                  }}
                />
              )}
            </div>

            {/* 버튼 아래쪽 중앙 배치 */}
            {selection && (
              <button className="btn btn-primary mt-3" onClick={handleSubmit}>제출하기</button>
            )}
          </div>
        </>
      )}

      {/* AI 추론 결과 및 확인 */}
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
