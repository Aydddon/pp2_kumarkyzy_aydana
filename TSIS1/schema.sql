-- Idempotent extension of the Practice 8 PhoneBook schema.
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups(name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20), -- legacy primary phone from Practice 7/8; data is migrated below
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE contacts ALTER COLUMN phone DROP NOT NULL;

UPDATE contacts SET group_id = (SELECT id FROM groups WHERE name = 'Other')
WHERE group_id IS NULL;
DO $$
DECLARE other_id INTEGER;
BEGIN
    SELECT id INTO other_id FROM groups WHERE name = 'Other';
    EXECUTE format('ALTER TABLE contacts ALTER COLUMN group_id SET DEFAULT %s', other_id);
END;
$$;

-- Remove the old single-phone uniqueness constraint so contacts can own multiple phones.
DO $$
DECLARE r RECORD;
BEGIN
    FOR r IN
        SELECT con.conname
        FROM pg_constraint con
        WHERE con.conrelid = 'contacts'::regclass
          AND con.contype = 'u'
          AND (SELECT array_agg(att.attname ORDER BY att.attname)
               FROM unnest(con.conkey) AS key(attnum)
               JOIN pg_attribute att ON att.attrelid = con.conrelid AND att.attnum = key.attnum)
              = ARRAY['phone']::name[]
    LOOP
        EXECUTE format('ALTER TABLE contacts DROP CONSTRAINT %I', r.conname);
    END LOOP;
END;
$$;

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

-- Migrate existing Practice 7/8 phone values once into the new one-to-many table.
INSERT INTO phones(contact_id, phone, type)
SELECT c.id, c.phone, 'mobile'
FROM contacts c
WHERE c.phone IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM phones p WHERE p.contact_id = c.id AND p.phone = c.phone
  );

-- Keep legacy Python add/update operations compatible while recording their phone in phones.
CREATE OR REPLACE FUNCTION sync_legacy_phone()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND OLD.phone IS DISTINCT FROM NEW.phone AND OLD.phone IS NOT NULL THEN
        DELETE FROM phones WHERE contact_id = OLD.id AND phone = OLD.phone AND type = 'mobile';
    END IF;
    IF NEW.phone IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (NEW.id, NEW.phone, 'mobile')
        ON CONFLICT (contact_id, phone) DO NOTHING;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS contacts_sync_legacy_phone ON contacts;
CREATE TRIGGER contacts_sync_legacy_phone
AFTER INSERT OR UPDATE OF phone ON contacts
FOR EACH ROW EXECUTE FUNCTION sync_legacy_phone();
