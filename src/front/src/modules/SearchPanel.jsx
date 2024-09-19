import { useState, useContext } from 'react';
import { SearchContext } from "../App"

const SearchComponent = () => {

  const [searchResult, setSearchResult] = useContext(SearchContext)

  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');

  const handleInputChange = (index, value) => {
    switch(index) {
      case 0:
        setInput1(value);
        break;
      case 1:
        setInput2(value);
        break;
    }
  };

  const handleSearch = () => {
    const searchValues = [input1.trim(), input2.trim()];
    setSearchResult(searchValues);
  };

  return (
    <div className="mt-4 flex flex-wrap items-center justify-between gap-x-2 gap-y-2 grow-2">
        <div className="flex flex-nowrap justify-between grow">
          <div className="">
            <input
              type="text"
              value={input1}
              onChange={(e) => handleInputChange(0, e.target.value)}
              placeholder="give"
              className="min-w-fit px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="my-auto mx-4">
            to
          </div>

          <div className="">
            <input
              type="text"
              value={input2}
              onChange={(e) => handleInputChange(1, e.target.value)}
              placeholder="get"
              className="min-w-fit px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      <button
        onClick={handleSearch}
        className="grow my-auto bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
      >
        Search
      </button>
    </div>
  );
};

export default SearchComponent;
