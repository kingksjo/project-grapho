import { ChevronRight } from 'lucide-react';

const SectionHeader = ({ title }) => (
    <div className="flex items-center gap-1 mb-6">
      <h2 className="text-white text-2xl font-bold">{title}</h2>
      <ChevronRight className="text-gray-400 w-6 h-6 " />
    </div>
  );

export default SectionHeader;