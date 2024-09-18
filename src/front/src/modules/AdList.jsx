import AdCard from '../components/AdCard';
import {useContext} from 'react';
import {SearchContext} from '../App';

const AdList = ({ads}) => {

    const [searchResult, setSearchResult] = useContext(SearchContext);

    return (
        <div className="w-full mx-auto">
            <h1 className="text-2xl font-bold mb-4">Ads</h1>
            <div className="">
                {ads.map((ad, index) => (
                <AdCard key={index} adData={ad} />
                ))}
            </div>
        </div>
    );
}


export default AdList;