Apple TV design language. It's clean, modern, and content-forward, which is perfect for a movie recommendation app. The image you provided, while for a news app, captures that aesthetic perfectly: a dark, immersive theme, high-quality background imagery, clean typography, and a focus on the content with minimal UI "chrome."

We will build the frontend with this design philosophy at its core.

---

### **Frontend Technology Stack**

This stack is the modern industry standard for building fast, interactive, and maintainable user interfaces.

1.  **Framework: React**
    *   **Why:** It's the most popular frontend library in the world, with a massive ecosystem and community. It uses a component-based architecture, which is perfect for building a complex UI like ours from small, reusable "Lego blocks."

2.  **Build Tool: Vite**
    *   **Why:** Vite is the modern successor to tools like Create React App. It offers a lightning-fast development server and an optimized build process. It's the standard for starting new React projects today.

3.  **Styling: Tailwind CSS**
    *   **Why:** This is the perfect tool to achieve the Apple TV aesthetic. Tailwind is a "utility-first" CSS framework. Instead of writing custom CSS files, you build designs directly in your HTML/JSX by applying pre-existing utility classes (e.g., `bg-black`, `text-white`, `p-4`). This approach makes it incredibly fast to build consistent, clean designs and is perfect for creating a dark-mode theme.

4.  **API Communication: Axios**
    *   **Why:** While you can use the built-in `fetch` API, `axios` is a library that makes working with APIs simpler. It has a cleaner syntax, better error handling, and makes it easy to set up "interceptors"—code that can automatically attach your JWT to every outgoing request.

---

### **Frontend Development Plan (Phase 3)**

This plan will guide you from an empty folder to a fully functional React application connected to your backend.

#### **Phase 3.1: Project Setup & Styling Foundation**

**Goal:** Create the React project and establish the core visual theme (colors, fonts, layout) that matches the Apple TV aesthetic.

**Action Plan:**
1.  **Initialize the React Project with Vite:**
    *   In your WSL terminal, navigate to the root of your `project-grapho` directory (the one containing the `backend` folder).
    *   Run the Vite command to create a new `frontend` folder:
        ```bash
        npm create vite@latest frontend -- --template react
        ```
2.  **Install Dependencies:** Navigate into the new `frontend` directory (`cd frontend`) and install the necessary packages:
    ```bash
    npm install
    npm install tailwindcss postcss autoprefixer --save-dev
    npm install axios
    ```
3.  **Configure Tailwind CSS:** Run the Tailwind init command to generate the configuration files:
    ```bash
    npx tailwindcss init -p
    ```
    You will then need to configure `tailwind.config.js` and `index.css` to enable Tailwind's styles.
4.  **Define the Apple TV Theme:** In your `tailwind.config.js`, we will define our core color palette.
    ```javascript
    // tailwind.config.js
    module.exports = {
      // ...
      theme: {
        extend: {
          colors: {
            'background': '#000000',
            'text-primary': '#FFFFFF',
            'text-secondary': '#a1a1aa', // A muted gray for secondary text
            'accent': '#007aff',       // Apple's classic blue
          },
        },
      },
      // ...
    }
    ```
5.  **Create a Global Layout:** Create a `Layout.jsx` component that wraps your entire application with the black background and sets up the basic structure.

#### **Phase 3.2: Building the UI Components**

**Goal:** Create all the reusable "Lego blocks" for our user interface.

**Action Plan:**
1.  **`Navbar.jsx`:** A persistent navigation bar at the top showing the app logo and a "Login" or "Logout" button.
2.  **`MovieCard.jsx`:** The most important component. It will display a movie's poster. We will add subtle hover effects (like a slight scale-up and a soft shadow) to give it the premium Apple TV feel.
3.  **`RecommendationCarousel.jsx`:** A horizontal scrolling container that will hold a list of `MovieCard` components. It will have a title, like "Because you liked Oppenheimer" or "Trending Now."
4.  **`LoginForm.jsx` & `RegisterForm.jsx`:** The forms for user authentication.
5.  **`Modal.jsx` (for "More Info"):** A popup modal that displays a movie's backdrop image, overview, and other details. We can use Tailwind's `backdrop-blur` utility to create the "frosted glass" effect seen in Apple's UI.

#### **Phase 3.3: Page Assembly & API Integration**

**Goal:** Connect the components together into pages and make them communicate with our live backend API.

**Action Plan:**
1.  **Create an API Service Module:** Create a file like `api.js` that uses `axios`. This module will contain all our functions for talking to the backend (`loginUser`, `registerUser`, `getRecommendations`, `postInteraction`). We'll configure it to automatically add the JWT from `localStorage` to the headers of protected requests.
2.  **Implement the Authentication Flow:**
    *   Create `LoginPage.jsx` and `RegisterPage.jsx`.
    *   When a user submits the form, call the appropriate function from your API service.
    *   On successful login, save the returned JWT to the browser's `localStorage` and redirect the user to the home page.
    *   Implement a global state (using React's Context API) to manage the user's login status across the entire application.
3.  **Build the Home Page (`HomePage.jsx`):**
    *   This page will be protected. If a user is not logged in, they will be redirected to the login page.
    *   When the page loads, it will use a `useEffect` hook to call the `getRecommendations` function from your API service.
    *   The returned list of movies will be stored in the component's state.
    *   The component will then render one or more `RecommendationCarousel` components, passing the movie data to them.
4.  **Implement the Interaction Flow:**
    *   Add "Like" and "Dislike" buttons to the `MovieCard.jsx` component.
    *   When a user clicks a button, an `onClick` handler will call the `postInteraction` function from your API service, sending the movie's `tconst` and the interaction type.

---

This plan will take you from an empty folder to a beautiful, functional, and interactive frontend that brings your recommendation engine to life.

