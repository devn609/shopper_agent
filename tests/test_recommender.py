from app.recommender import recommend
def test_recommendations_return_products():
    r=recommend("road running shoes", "c001"); assert r and all("current_price" in x for x in r)
def test_preferences_change_ranking():
    assert recommend("shoes","c001")[0]["category"] in {"running","training"}
    assert recommend("shoes","c002")[0]["category"] in {"walking","sneakers"}
