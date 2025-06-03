//ai_project/app/(home)/page.js

import Db_test from "@/components/db_test";

export const metadata = {
  title: 'AI_service',
  description: 'AI_service',
};

export default function Home() {
  return (
   <section className="text-center my-5">
      <h1 className="display-4 fw-bold">인터넷 미아를 위한 길잡이</h1>
      <p className="lead mt-3 mb-4">
        검색하다가 길을 잃으셨나요?<br />
        잊혀진 목적지를 AI가 함께 찾아드립니다.
      </p>
      {/* <Db_test/> */}
      <img
        src="/ai_thinking.gif"
        alt="AI thinking"
        className="img-fluid rounded"
        style={{ maxWidth: '400px' }}
      />
    </section>
  );
}
