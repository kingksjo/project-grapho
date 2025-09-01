import { useState } from 'react'

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