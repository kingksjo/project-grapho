
---

### **Analysis of Your User Flow vs. Our Technical Plan**

Your flow is logical, user-centric, and provides a clear path from a "cold start" user to a fully engaged one.

**1. User Creates Account**
*   **Your Flow:** User signs up.
*   **Our Plan:** **Perfectly aligned.** We are currently building the `POST /users/register` endpoint to handle exactly this.

**2. Onboarding: Top 5 Genres & Picking 5+5 Movies/Shows**
*   **Your Flow:** User selects 5 genres, then is shown trending movies/shows from the last 3 years and picks 5 movies and 5 shows they've liked.
*   **Our Plan:** **This is an excellent addition and aligns perfectly.**
    *   **"Top 5 Genres":** Our backend will need a way to store this. The simplest way is to add a `favorite_genres` column (e.g., as a comma-separated string or a JSON field) to our `users` table in `models.py`. We'll need a new Alembic migration for this.
    *   **"Trending in the past 3 years":** Our backend will need an endpoint like `GET /onboarding/trending` that returns a list of popular, recent movies/shows. It will use our `movies` table, filtering by `startYear` and sorting by `numVotes`.
    *   **"Picking 5 movies and 5 shows":** When the user makes these selections, the frontend will call our `POST /interactions` endpoint 10 times, saving each "like" to the database. This is a brilliant way to seed the user's taste profile immediately.

**3. The Home Screen: Weekly Recommendations (Movies & TV Shows)**
*   **Your Flow:** The main screen shows two sections of recommendations: one for movies, one for TV shows.
*   **Our Plan:** **Aligns perfectly with a small tweak.** Our main `GET /recommendations` endpoint can easily handle this. We can add an optional query parameter to the request, like:
    *   `GET /recommendations?type=movie`
    *   `GET /recommendations?type=tvSeries`
    *   The backend logic will get the user's taste profile as planned, but when it generates the final candidate pool, it will apply an extra filter for `titleType` before returning the results.

**4. Item Card: More Info, Like/Dislike**
*   **Your Flow:** User can click a card for more info and can like or dislike it.
*   **Our Plan:** **Perfectly aligned.**
    *   **"More Info":** The frontend will have all the info it needs from the `GET /recommendations` call (which includes the TMDb enrichment). Alternatively, we could build a `GET /movies/{tconst}` endpoint for even more detailed data.
    *   **"Like/Dislike":** This directly maps to our planned `POST /interactions` endpoint.

**5. The Hybrid Model Future**
*   **Your Flow:** The interaction data will be used for collaborative filtering later.
*   **Our Plan:** **Perfectly aligned.** The `interactions` table is being designed specifically to be the fuel for our future SVD (Collaborative Filtering) model.

---

### **Clarity on Combining the Hybrid Model (The Future Vision)**

You asked for clarity on this again, which is great. Here is the most concrete explanation of how the final hybrid system will work inside the `GET /recommendations` endpoint in Phase 4:

Let's say a user has liked 100 movies.

1.  **Get Two Separate Lists:**
    *   **Content List:** The backend runs the **profile-based content model** we are building now. It takes the user's last 15 likes, creates a profile vector, and generates a ranked list of the top 50 most similar movies.
    *   **Collaborative List:** The backend takes the user's `user_id` and feeds it into the **trained SVD model**. The SVD model, having learned from *all* users' interactions, predicts and returns a ranked list of the top 50 movies it thinks this user will like, including potentially surprising "serendipitous" recommendations.

2.  **Merge and Re-Rank:**
    *   The backend now has two lists of 50 movies. It creates a combined "master list."
    *   It then calculates a final "hybrid score" for each movie in the master list. A simple but effective way to do this is:
        *   Give each movie a "content score" based on its rank in the content list.
        *   Give each movie a "collaborative score" based on its rank in the collaborative list.
        *   The **Final Hybrid Score** = `(w1 * content_score) + (w2 * collaborative_score)`.
        *   A movie that appears high up on **both lists** will get a massive final score and will be ranked at the very top of the user's feed.

This two-pronged approach ensures you get recommendations that are both **relevant** (from the content model) and **discovered** (from the collaborative model).

**Conclusion:** Your user flow is excellent and aligns beautifully with our technical plan. It gives us a clear product vision to build towards. We just need to remember to add the `favorite_genres` column to our `users` table when we get a moment.





Here is the revised and comprehensive implementation plan for finishing the backend. This plan incorporates your user flow and all our technical decisions.

---

### **Revised Backend Implementation Plan (Phase 2.3 - Final)**

**Goal:** To build all remaining endpoints required to support the full application user flow, from onboarding to receiving personalized, profile-based recommendations.

#### **Step 1: Update the Database Schema**

**Concept:** Our user flow introduced a new requirement: storing a user's favorite genres. We must update our database schema first, using Alembic to manage the change.

**Action Plan:**
1.  **Modify `models.py`:** Add a `favorite_genres` column to the `User` model class. We can use a `String` type to store a comma-separated list.
2.  **Generate a New Migration:** Run `docker compose exec api alembic revision --autogenerate -m "Add favorite_genres to users table"`.
3.  **Apply the Migration:** Run `docker compose exec api alembic upgrade head`. This will safely add the new column to our `users` table without losing any existing data.

---

#### **Step 2: Create All Necessary Pydantic Schemas**

**Concept:** Define the data contracts for all new API inputs and outputs in one go to ensure consistency.

**Methodology:** We will update our `backend/app/schemas.py` file.

**Action Plan:**
1.  **`UserUpdateGenres` Schema:** A simple schema for the onboarding step, containing a list of strings (e.g., `{"genres": ["Action", "Drama", "Sci-Fi"]}`).
2.  **`InteractionCreate` Schema:** To handle a user liking/disliking a movie. Will contain `tconst` and `interaction_type`.
3.  **`MovieRecommendation` Schema:** The final, enriched movie object we return to the frontend. Will include fields like `tconst`, `primaryTitle`, `startYear`, `poster_url`, and `overview`.

---

#### **Step 3: Expand CRUD Functions**

**Concept:** Add all the necessary database interaction logic to our `crud.py` file to support the new features.

**Methodology:** We will add three new functions to `backend/app/crud.py`.

**Action Plan:**
1.  **`update_user_genres()` function:** Takes a `user_id` and a list of genres and updates the user's record in the database.
2.  **`create_or_update_interaction()` function:** Takes a `user_id`, `movie_id`, and `interaction_type`. It will create a new interaction or update an existing one (e.g., if a user changes from 'like' to 'dislike').
3.  **`get_user_liked_movies()` function:** Takes a `user_id` and returns a list of the `title_year` IDs for their last 10-15 liked movies. This is the "taste profile" builder.

---

#### **Step 4: Build the Onboarding and Core Logic Endpoints**

**Concept:** Implement all the remaining API endpoints in our `routers.py` file, ensuring they are protected where necessary.

**Methodology:** We will build out a user/interactions router and a dedicated recommendations router to keep things organized.

**Action Plan:**
1.  **`GET /onboarding/trending` Endpoint (New):**
    *   An unprotected endpoint that returns a list of popular movies and TV shows from the last 3 years, sorted by `numVotes`. This will be used to populate the movie selection screen during onboarding.
2.  **`POST /users/me/genres` Endpoint (New):**
    *   A protected endpoint. It will take the `UserUpdateGenres` schema as input and use our `crud.update_user_genres()` function to save the user's genre preferences.
3.  **`POST /interactions` Endpoint (As Planned):**
    *   A protected endpoint. It will receive an `InteractionCreate` object, find the movie's internal ID, and save the interaction using `crud.create_or_update_interaction()`.
4.  **`GET /recommendations` Endpoint (The Main Event):**
    *   A protected endpoint that orchestrates the entire recommendation logic.
    *   **Logic:**
        a. Get the current user via `Depends(auth.get_current_user)`.
        b. Call `crud.get_user_liked_movies()` to get their taste profile (list of `title_year` IDs).
        c. **Handle Cold Start:** If the list is too short (e.g., fewer than 5 movies), implement a fallback: get their `favorite_genres` and recommend popular movies from those genres instead.
        d. **Call the Profile Engine:** If the profile is sufficient, pass the list of IDs to our `get_recommendations_from_profile()` function.
        e. **Enrich with TMDb:** Take the top 10 `tconst`s from the engine's output and call the TMDb API to get poster URLs and overviews. (We'll add our TMDb API key to `.env`).
        f. **Return the Response:** Send back the final, enriched list of movies, formatted according to our `MovieRecommendation` schema.

This detailed plan covers every requirement from your user flow. It is a complete blueprint for finishing the backend. Once we have implemented all these steps, Phase 2 will be officially complete, and you will have a fully functional, feature-rich backend API.

