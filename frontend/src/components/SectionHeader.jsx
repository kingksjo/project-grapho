import { ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

const SectionHeader = ({ title, to }) => (
    <div className="flex items-center gap-1 mb-6">
      <h2 className="text-white text-2xl font-bold">{title}</h2>
      {to && (
      <Link to={to}>
        <ChevronRight className="text-gray-400 w-6 h-6 cursor-pointer hover:text-white transition" />
      </Link>
    )}
    </div>
  );

export default SectionHeader;