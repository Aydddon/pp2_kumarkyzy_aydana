CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.phone
    FROM contacts AS c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    IF p_limit <= 0 OR p_limit > 100 THEN
        RAISE EXCEPTION 'Limit must be between 1 and 100';
    END IF;

    IF p_offset < 0 THEN
        RAISE EXCEPTION 'Offset cannot be negative';
    END IF;

    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.phone
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone_numbers TEXT
)
LANGUAGE sql
STABLE
AS $$
    SELECT c.id, c.first_name, c.email, c.birthday, g.name,
           COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '')
    FROM contacts AS c
    LEFT JOIN groups AS g ON g.id = c.group_id
    LEFT JOIN phones AS p ON p.contact_id = c.id
    WHERE COALESCE(c.first_name, '') ILIKE '%' || COALESCE(p_query, '') || '%'
       OR COALESCE(c.email, '') ILIKE '%' || COALESCE(p_query, '') || '%'
       OR EXISTS (
           SELECT 1 FROM phones AS px
           WHERE px.contact_id = c.id
             AND px.phone ILIKE '%' || COALESCE(p_query, '') || '%'
       )
    GROUP BY c.id, c.first_name, c.email, c.birthday, g.name
    ORDER BY c.id;
$$;
