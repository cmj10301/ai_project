'use client'

import ReactFlow, {
  Background,
  Controls,
  MiniMap
} from 'react-flow-renderer';
import { useCallback, useState } from 'react';

const initialNodes = [
  {
    id: 'root',
    data: { label: '검색 시작' },
    position: { x: 250, y: 0 },
    style: { background: '#D6EAF8', padding: 10, borderRadius: 5 }
  }
];

const initialEdges = [];

export default function SearchMindmap() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const [input, setInput] = useState('');

  const handleProcess = () => {
    if (!input.trim()) return;

    const keywords = input.split(',').map(s => s.trim());
    const newNodes = [...initialNodes];
    const newEdges = [];

    keywords.forEach((kw, idx) => {
      const nodeId = `node_${idx}`;
      newNodes.push({
        id: nodeId,
        data: { label: kw },
        position: { x: 100 + idx * 150, y: 150 },
        style: { background: '#FADBD8', padding: 10, borderRadius: 5 }
      });
      newEdges.push({ id: `e_root_${nodeId}`, source: 'root', target: nodeId });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  };

  return (
    <div className="container py-4">
      <h2 className="text-center mb-3">🧭 검색 기록 마인드맵</h2>

      <div className="mb-3">
        <textarea
          className="form-control"
          rows={3}
          placeholder="브라우저에서 수집된 검색어들을 콤마(,)로 구분해 입력하세요. 예: 러닝화 추천, 스쿼트 방법, 단백질 파우더"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="btn btn-primary mt-2" onClick={handleProcess}>마인드맵 생성</button>
      </div>

      <div style={{ height: 500, border: '1px solid #ccc' }}>
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
}
