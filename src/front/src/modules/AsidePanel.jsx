import {useState, useEffect} from 'react';
import axios from 'axios';


const AsidePanel = () => {

    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userData, setUserData] = useState(null);

    const authenticate = async () => {
        axios.post(
            'http://localhost:8008/api/auth/check'
        )
    };

    useEffect(() => {
        //authenticate();
        }
    );

    return (
        <div className="flex flex-col items-center w-64 min-w-64 shadow-lg h-full p-4">
            <div>
                aside 1
            </div>
            <div>
                aside 2
            </div>
            <div>
                aside 3
            </div>
        </div>
    );
};

export default AsidePanel;