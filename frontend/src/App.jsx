import { useState } from 'react'
import SectionHeader from './components/SectionHeader';
import ContentCard from './components/ContentCard';

const App = () => {

  const tvShows = [
    {
      id: 1,
      title: "Platonic",
      genre: "Comedy",
      image: "https://is1-ssl.mzstatic.com/image/thumb/rBI93Qq60YpBP60maTBNbg/680x382.webp"
    },
    {
      id: 2,
      title: "Invasion",
      genre: "Sci-Fi",
      image: "https://is1-ssl.mzstatic.com/image/thumb/hH3rVWDItz3USIX5bBSEcw/680x382.webp"
    },
    {
      id: 3,
      title: "Chief of War",
      genre: "Drama",
      image: "https://is1-ssl.mzstatic.com/image/thumb/twLCcLLXmcLBqEf3Af3vww/680x382.webp"
    },
    {
      id: 4,
      title: "Foundation",
      genre: "Sci-Fi",
      image: "https://is1-ssl.mzstatic.com/image/thumb/Xye2zsX5gxLetoLRdTgNLA/680x382.webp"
    },
    {
      id: 5,
      title: "Ted Lasso",
      genre: "Comedy",
      image: "https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/680x382.webp"
    },
    {
        id: 6,
        title: "Acapulco",
        genre: "Comdey",
        image: "https://is1-ssl.mzstatic.com/image/thumb/Ec4GedDwtKAxOrCp_VOF-g/680x382.webp"
    },
    {
        id: 7,
        title: "Severance",
        genre: "Thriller",
        image: "https://is1-ssl.mzstatic.com/image/thumb/EUeDAPovZrBtOcrP2Da5Lw/680x382.webp"
    },
    {
        id: 8,
        title: "Slow Horses",
        genre: "Thriller",
        image: "https://is1-ssl.mzstatic.com/image/thumb/S2T1FMcov5a0GzmninlU4Q/680x382.webp"
    },
    {
        id: 9,
        title: "Shrinking",
        genre: "Comedy",
        image: "https://is1-ssl.mzstatic.com/image/thumb/C34jADlGtR5wObjPAMbW4w/680x382.webp"
    },
    {
        id: 10,
        title: "Stick",
        genre: "Comdey",
        image: "https://is1-ssl.mzstatic.com/image/thumb/Axf6fFibiK2puSTzKXvgpA/680x382.webp"
    }
  ];

  const movies = [
    {
      id: 1,
      title: "The Gorge",
      year: "2025",
      genre: "Thriller",
      image: "https://is1-ssl.mzstatic.com/image/thumb/3pfG0GJkoI0OFlPiIDdvUQ/680x382.webp"
    },
    {
      id: 2,
      title: "Fountain of Youth",
      year: "2025",
      genre: "Action",
      image: "https://is1-ssl.mzstatic.com/image/thumb/4UEcdeb6Xoc40fhFSAr3Og/680x382.webp"
    },
    {
      id: 3,
      title: "Echo Valley",
      year: "2025",
      genre: "Thriller",
      image: "https://is1-ssl.mzstatic.com/image/thumb/gy_-HeK7Awo48x2fPuAy_w/680x382.webp"
    },
    {
      id: 4,
      title: "Greyhound",
      year: "2020",
      genre: "Action",
      image: "https://is1-ssl.mzstatic.com/image/thumb/oANBVngpEJDvHRhdyozySA/680x382.webp"
    },
    {
      id: 5,
      title: "Wolfs",
      year: "2024",
      genre: "Action",
      image: "https://is1-ssl.mzstatic.com/image/thumb/2eBqvT3JXPbdzHWj6HM5_w/680x382.webp"
    },
    {
        id: 6,
        title: "The Family Plan",
        year: "2023",
        genre: "Comdey",
        image: "https://is1-ssl.mzstatic.com/image/thumb/tPJwMGtsAr_psAVlyf2Rzg/680x382.webp"
    },
    {
        id: 7,
        title: "Killers of the Moon",
        year: "2023",
        genre: "Crime",
        image: "https://is1-ssl.mzstatic.com/image/thumb/rss8pF-klNy76S-NWFue-A/680x382.webp"
    },
    {
        id: 8,
        title: "Ghosted",
        year: "2023",
        genre: "Action",
        image: "https://is1-ssl.mzstatic.com/image/thumb/Ze8uZ-TWJ2JMbqmtcz8_BA/680x382.webp"
    },
    {
        id: 9,
        title: "A Summer Musical",
        year: "2025",
        genre: "Animation",
        image: "https://is1-ssl.mzstatic.com/image/thumb/qnArJ6qO8I8hoZv2OhnO5A/680x382.webp"
    },
    {
        id: 10,
        title: "Luck",
        year: "2022",
        genre: "Animation",
        image: "https://is1-ssl.mzstatic.com/image/thumb/gHMoyFnOUJLH6d0rSgyIbg/680x382.webp"
    }
  ];

  return (
    <div className="bg-black min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* TV Shows Section */}
        <section className="mb-12">
          <SectionHeader title="Top 10 TV Shows" />
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
          <SectionHeader title="Top 10 Movies" />
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
  );
};

export default App;


{/** 
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
*/}