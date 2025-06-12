'use client';

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand bg-primary navbar-dark px-4">
      <a className="navbar-brand me-4" href="/">AI Project</a>
      <ul className="navbar-nav">
        <li className="nav-item">
          <a className="nav-link" href="/ai_quiz">AI 퀴즈</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/ai_drawing">AI 스케치</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/ai_image">AI 이미지</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/ai_history">기록</a>
        </li>
      </ul>
    </nav>
  );
}
