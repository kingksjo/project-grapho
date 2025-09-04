const ContentCard = ({ item, index, isMovie = false }) => (
    <div className="flex-shrink-0 group cursor-pointer">
      <div className="relative overflow-hidden rounded-lg bg-gray-800 transition-transform duration-300 group-hover:scale-105">
        <img
          src={item.image}
          alt={item.title}
          className="w-64 h-36 object-cover"
        />
        
        <div className="absolute bottom-4 left-4 right-4">
          <div className="flex items-center gap-2">
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          </div>
        </div>
      </div>
      <div className="mt-3 flex items-center">
        <div className="bg-gray-700 rounded-full w-11 h-11 flex items-center justify-center text-white font-bold text-3xl mr-3">
          {index}
        </div>
        <div>
          <h4 className="text-white font-medium">{item.title}</h4>
          <p className="text-gray-400 text-sm">
            {isMovie ? `${item.year} · ${item.genre}` : item.genre}
          </p>
        </div>
      </div>
    </div>
  );

export default ContentCard;