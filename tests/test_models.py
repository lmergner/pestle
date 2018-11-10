
from pytest_pgtap import tests

def test_w_pgtap_fixture(pgtap):
    assert pgtap("""
        SELECT tables_are(ARRAY['post', 'user', 'simple'], 'Should have 3 tables');
    """)

def test_schema_using_assertion_helpers():
    tests.assert_tables_are('post', 'user', 'simple', msg='blarg')
    tests.assert_columns_are('post', 'oid', 'created', 'modified', 'extras')