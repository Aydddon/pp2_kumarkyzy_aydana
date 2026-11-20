-- Remove obsolete unsafe Practice 8 overloads, if they still exist.
DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS delete_contact(VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL,
    p_contact_id INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_match_count INTEGER;
    v_match_id INTEGER;
BEGIN
    IF p_contact_id IS NOT NULL THEN
        DELETE FROM contacts WHERE id = p_contact_id;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Contact ID % was not found', p_contact_id;
        END IF;
        RETURN;
    END IF;

    IF (p_name IS NULL OR BTRIM(p_name) = '')
       AND (p_phone IS NULL OR BTRIM(p_phone) = '') THEN
        RAISE EXCEPTION 'Provide a name or phone number';
    END IF;

    SELECT COUNT(*), MIN(id)
    INTO v_match_count, v_match_id
    FROM contacts
    WHERE (p_name IS NOT NULL AND first_name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);

    IF v_match_count = 0 THEN
        RAISE EXCEPTION 'No matching contact found';
    ELSIF v_match_count > 1 THEN
        RAISE EXCEPTION 'Several contacts match; specify the contact ID';
    ELSE
        DELETE FROM contacts WHERE id = v_match_id;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_count INTEGER;
    v_contact_id INTEGER;
BEGIN
    IF p_contact_name IS NULL OR BTRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;
    IF p_phone IS NULL OR p_phone !~ '^\+?[0-9]{7,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number';
    END IF;
    IF p_type IS NULL OR p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile';
    END IF;

    SELECT COUNT(*), MIN(id)
    INTO v_contact_count, v_contact_id
    FROM contacts
    WHERE first_name = BTRIM(p_contact_name);

    IF v_contact_count = 0 THEN
        RAISE EXCEPTION 'Contact not found';
    ELSIF v_contact_count > 1 THEN
        RAISE EXCEPTION 'Several contacts have this name; use a unique name';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_count INTEGER;
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    IF p_contact_name IS NULL OR BTRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;
    IF p_group_name IS NULL OR BTRIM(p_group_name) = '' THEN
        RAISE EXCEPTION 'Group name cannot be empty';
    END IF;

    SELECT COUNT(*), MIN(id)
    INTO v_contact_count, v_contact_id
    FROM contacts
    WHERE first_name = BTRIM(p_contact_name);

    IF v_contact_count = 0 THEN
        RAISE EXCEPTION 'Contact not found';
    ELSIF v_contact_count > 1 THEN
        RAISE EXCEPTION 'Several contacts have this name; use a unique name';
    END IF;

    INSERT INTO groups(name) VALUES (INITCAP(BTRIM(p_group_name)))
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = INITCAP(BTRIM(p_group_name));

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;
