
def get_fixtures_from_DB(db) -> list:
    """
    Get fixtures with caching
    
    Args:
        db: Firebase database instance
        cache: FirebaseCache instance
    """

        
    # If no cache, fetch from Firebase
    print("Fetching fresh fixtures data from Firebase")
    fixtures = db.collection('fixtures').stream()
    fixtures_data = [fixture.to_dict() for fixture in fixtures]

    
    return fixtures_data