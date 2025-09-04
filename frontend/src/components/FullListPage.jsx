import ContentCard from "../components/ContentCard";

const FullListPage = ({ title, items }) => {
  return (
    <div>
      <h1 className="text-white text-3xl font-bold mb-8">{title}</h1>
      <div className="grid grid-cols-1 sm:grid-cols- md:grid-cols-4 lg:grid-cols-5 gap-4">
        {items.map((item, index) => (
          <ContentCard
            key={item.id}
            item={item}
            index={index + 1}
            isMovie={!!item.year} // detect if it's a movie
          />
        ))}
      </div>
    </div>
  );
};

export default FullListPage;
