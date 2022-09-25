import psycopg2

def init_user_table(uri):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()

    # テーブルの新規作成(ユーザー)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS public.users
    (
        id serial,
        email text COLLATE pg_catalog."default",
        name text COLLATE pg_catalog."default",
        hashed_password text COLLATE pg_catalog."default",
        is_active boolean DEFAULT true,
        CONSTRAINT users_pkey PRIMARY KEY (id),
        CONSTRAINT users_email_key UNIQUE (email),
        CONSTRAINT users_name_key UNIQUE (name)
    )
    TABLESPACE pg_default;
    ALTER TABLE public.users
        OWNER to postgres;
    INSERT INTO users values
    (
        0, 'example@example.com', 'exampleUser', '$2b$12$vcVfhe90CGknHjEQL/IGR.9qegL9BftgeR22y1AXnVsz1rT.6R80i', true
    )
    ON CONFLICT DO NOTHING;
    """
    )
    cur.close()
    conn.commit()
    conn.close()

def init_video_table(uri):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()

    # テーブルの新規作成(動画)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS public.videos
    (
        id serial,
        dist text,
        title text,
        username text,
        duration integer,
        playcount integer,
        datetime timestamp without time zone,
        CONSTRAINT videos_pkey PRIMARY KEY (id)
    )
    TABLESPACE pg_default;
    ALTER TABLE public.videos
        OWNER to postgres;
    """
    )
    cur.close()
    conn.commit()
    conn.close()