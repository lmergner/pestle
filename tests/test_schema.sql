SELECT plan(12);
SELECT tables_are(ARRAY['post', 'user', 'simple'], 'Should have 3 tables');

-- simple columns
SELECT columns_are('simple', ARRAY['oid', 'created', 'modified', 'extras'], 'table simple should have 4 basic colums');
SELECT col_type_is('simple', 'extras', 'json');

-- searchable text columns
SELECT has_column('post', 'text', 'table post should have a text column');
SELECT has_column('post', 'tsvector', 'table post should have a tsvector column');
SELECT col_type_is('post', 'tsvector', 'tsvector', 'table post shouldhave a tsvector column with type tsvector');
SELECT has_index('post', 'tsvector_idx_post', 'table post should have an index on the tsvector column');
SELECT has_trigger('post', 'ts_update', 'table post should have a trigger');

-- admin / user colums
SELECT has_column('user', 'password', 'table user should have a password column');
SELECT has_column('user', 'password_updated', 'table user should have a password updated column');
SELECT col_type_is('user', 'password_updated', 'timestamp with time zone');

SELECT * from finish();