-- Search contacts by name, email, or any phone number.
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
    SELECT c.id,
           c.first_name,
           c.email,
           c.birthday,
           g.name,
           COALESCE(
               string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id),
               ''
           )
    FROM contacts AS c
    LEFT JOIN groups AS g ON g.id = c.group_id
    LEFT JOIN phones AS p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || COALESCE(p_query, '') || '%'
       OR COALESCE(c.email, '') ILIKE '%' || COALESCE(p_query, '') || '%'
       OR EXISTS (
           SELECT 1
           FROM phones AS px
           WHERE px.contact_id = c.id
             AND px.phone ILIKE '%' || COALESCE(p_query, '') || '%'
       )
    GROUP BY c.id, c.first_name, c.email, c.birthday, g.name
    ORDER BY c.id;
$$;

-- Page through contacts using the Practice 8 pagination approach.
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit IS NULL OR p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'Limit must be between 1 and 100';
    END IF;
    IF p_offset IS NULL OR p_offset < 0 THEN
        RAISE EXCEPTION 'Offset cannot be negative';
    END IF;

    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;
