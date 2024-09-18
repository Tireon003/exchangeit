import { useState } from 'react';
import ContactModal from './ContactModal';

const AdCard = ({ adData }) => {
  const { id, by_user, category, item_give, item_get, description, location, created_at } = adData;

  const [isExpanded, setIsExpanded] = useState(false);

  const truncatedDescription = isExpanded ? description : `${description.slice(0, 100)}...`;

  const formattedTitle = `${item_give} to ${item_get}`;

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentAdData, setCurrentAdData] = useState(null);

  const handleContactClick = () => {
    // Открываем модальное окно с текущими данными ада
    setCurrentAdData(adData);
    setIsModalOpen(!isModalOpen);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h2 className="text-xl font-bold mb-2">{formattedTitle}</h2>

      <div className="flex justify-between items-center mb-3">
        <span className="text-gray-600">Published on: {new Date(created_at).toLocaleDateString()}</span>
      </div>

      <p className="mb-3 text-gray-700 line-clamp-3">{truncatedDescription}</p>

      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-300"
      >
        {isExpanded ? 'Show less' : 'Read more'}
      </button>

      <div className="mt-4 flex justify-between items-center border-t pt-2">
        <span className="text-sm text-gray-600">{location}</span>

        <div className="flex space-x-2">
          <button
            className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition duration-300"
            onClick={handleContactClick}
          >
            Contact
          </button>
          <button className="px-3 py-1 bg-purple-500 text-white rounded hover:bg-purple-600 transition duration-300">
            Add to wishlist
          </button>
        </div>
      </div>
      <ContactModal isOpen={isModalOpen} onClose={handleContactClick} adId={currentAdData?.id ?? null} />
    </div>
  );
};

export default AdCard;
