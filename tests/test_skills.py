from app.skills import get_skill
def test_skill():assert get_skill("repo.inspect").role=="research"
