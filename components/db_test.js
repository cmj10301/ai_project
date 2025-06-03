//ai_project/components/db_test.js
'use client'
import { useEffect, useState } from "react";

export default function Db_test() {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        fetch("/api/posts")
        .then(async (res) => {
            if (!res.ok) {
                throw new Error(`서버 오류: ${res.status}`);
            }

            const text = await res.text();
            if (!text) {
                throw new Error("응답이 비어 있음.");
            }

            const data = JSON.parse(text);
            setPosts(data);
        })
        .catch ((err) => {
            console.error("데이터 불러오기 실패", err);
        })
    },[])

    return (
        <div>
            <h2>DB 접속 결과</h2>
            {posts.length > 0 ? (
                posts.map((post, i) => (
                <div key={i}>{JSON.stringify(post)}</div>
            ))
            ) : (
                <div>불러올 데이터가 없습니다.</div>
            )}
        </div>
    )
}