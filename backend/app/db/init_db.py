def init_db(conn):
    if not conn:
        print("❌ DB 연결 실패로 테이블 생성 중단")
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS index_types (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR(20) UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT
                );
            """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS index_data (
                    id SERIAL PRIMARY KEY,
                    index_type_id INT NOT NULL REFERENCES index_types(id),
                    date DATE NOT NULL,
                    value FLOAT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(index_type_id, date)  
                );
            """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS index_score (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    score FLOAT NOT NULL,
                    explanation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date)
                );
            """
            )

            conn.commit()
    finally:
        conn.close()
    print("✅ 테이블 생성 완료")
