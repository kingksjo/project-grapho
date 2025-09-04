import { tvShows, movies, mustSeeHits } from "./data";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SectionHeader from "./components/SectionHeader";
import ContentCard from "./components/ContentCard";
import FullListPage from "./components/FullListPage";

const App = () => {
  
  
  return (
    <Router>
      <div className="bg-black min-h-screen p-8">
        <div className="max-w-7xl mx-auto">
          <Routes>

          {/* TV Shows Section */}
          <Route path="/"
            element={
              <>
              <section className="mb-12">
            <SectionHeader title="Top 10 TV Shows" to="/tvshows" />
            <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
              {tvShows.map((show, index) => (
                <ContentCard
                  key={show.id}
                  item={show}
                  index={index + 1}
                  isMovie={false}
                />
              ))}
            </div>
          </section>

          {/* Movies Section */}
          <section>
            <SectionHeader title="Top 10 Movies" to="/movies"/>
            <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
              {movies.map((movie, index) => (
                <ContentCard
                  key={movie.id}
                  item={movie}
                  index={index + 1}
                  isMovie={true}
                />
              ))}
            </div>
          </section>

          {/* Must-See Hits */}
          <section>
            <SectionHeader title="Must-See Hits" to="/must-see"/>
            <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
              {mustSeeHits.map((item, index) => (
                <ContentCard
                  key={item.id + "-mustsee"}
                  item={item}
                  index={index + 1}
                />
              ))}
            </div>
          </section>
              </>
            }
          />
          {/* Full lists */}
            <Route path="/tvshows" element={<FullListPage title="All TV Shows" items={tvShows} />} />
            <Route path="/movies" element={<FullListPage title="All Movies" items={movies} />} />
            <Route path="/mustsee" element={<FullListPage title="Must-See Hits" items={mustSeeHits} />} />
          </Routes>
          </div>
        <style jsx>{`
          .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
          }
          .scrollbar-hide::-webkit-scrollbar {
            display: none;
          }
        `}</style>
      </div>
    </Router>
  );
};

export default App;

{
  /** 
function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-background text-text-primary">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-8">
            🎬 Grapho
          </h1>
          <p className="text-text-secondary mb-8">
            Your personalized movie recommendation engine
          </p>
          
          <div className="glass-card p-8 max-w-md mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Setup Test</h2>
            <p className="mb-4">Tailwind CSS is working! 🎉</p>
            
            <button 
              className="btn-primary mr-4"
              onClick={() => setCount((count) => count + 1)}
            >
              Count: {count}
            </button>
            
            <button className="btn-ghost">
              Reset
            </button>
          </div>

          <div className="mt-8 text-sm text-text-secondary">
            Ready to start building the movie recommendation frontend!
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
*/
}
