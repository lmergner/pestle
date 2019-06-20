def test_w_pgtap_fixture(pgtap):
    assert pgtap("""
        SELECT tables_are(ARRAY['post', 'user', 'simple'], 'Should have 3 tables');
    """)