import pandas as pd
from sqlalchemy.orm import Session
from . import models

# The function now accepts the DataFrame and the DB session as arguments
def seed_movies_table(db: Session, movies_df: pd.DataFrame):
    """
    Populates the 'movies' table using a pre-loaded DataFrame.
    """
    try:
        movie_count = db.query(models.Movie).count()
        if movie_count > 0:
            print(f"The 'movies' table is not empty ({movie_count} rows found). Aborting seed.")
            return

        print(f"Seeding database with {len(movies_df)} movies...")
        
        new_movies = []
        for index, row in movies_df.iterrows():
            movie_data = models.Movie(
                tconst=row['tconst'],
                primaryTitle=row['primaryTitle'],
                startYear=int(row['startYear']), # Ensure startYear is an integer
                genres=row['genres']
            )
            new_movies.append(movie_data)
        
        db.add_all(new_movies)
        db.commit()
        
        print("✅ Seeding complete. The 'movies' table has been populated.")

    except Exception as e:
        print(f"❌ An error occurred during seeding: {e}")
        db.rollback()
    finally:
        # The session will be closed by the code that calls this function.
        pass