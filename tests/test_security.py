from app.security import action_hash
def test_hash_stable():assert action_hash({"b":2,"a":1})==action_hash({"a":1,"b":2})
