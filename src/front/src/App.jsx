import { useState, useEffect, createContext } from 'react';
import AdList from './modules/AdList';
import SearchPanel from './modules/SearchPanel';
import AsidePanel from './modules/AsidePanel';
import axios from 'axios';

const SearchContext = createContext();

const App = () => {

  const [searchResult, setSearchResult] = useState(["", ""]);
  const [ads, setAds] = useState([]);

  useEffect(() => {
    fetchAds();
  }, [searchResult]);

  async function fetchAds() {
    try {
      const response = await axios.post(
          'http://localhost:8008/api/ads/',
          {
              itemGet: searchResult[1],
              itemGive: searchResult[0],
          }
      );
      setAds(response.data);
    } catch (error) {
      console.log('Ошибка при получении объявлений:', error);
    }
  }

  return (
  <SearchContext.Provider value={[searchResult, setSearchResult]}>
    <div className="flex h-screen">
      <main className="flex-1">
        <div className="mx-auto px-24 overflow-y-auto max-h-screen">
          <SearchPanel />
          <AdList ads={ads}/>
        </div>
      </main>
      <aside className="top-0 right-0 w-64 h-full bg-white">
        <AsidePanel />
      </aside>
    </div>
  </SearchContext.Provider>
);

};

export default App;
export { SearchContext };
