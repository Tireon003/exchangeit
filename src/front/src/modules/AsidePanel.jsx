import {useState, useEffect} from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import {SignupModal} from '../components/SignupModal'


const AsidePanel = () => {

    const [userData, setUserData] = useState(null);
    const [isModal, setIsModal] = useState(false);

    const closeModal = () => {
        setIsModal(false);
    }

    const openModal = () => {
        setIsModal(true);
    }

    const getUserData = async () => {
        try {
            const token = Cookies.get('access_token');
            if (!token) {
                throw new Error('Access token not found in cookies');
            }

            const response = await axios.get(
                'http://localhost:8008/api/users/user',
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            setUserData(response.data);
        } catch (error) {
            console.error("Ошибка при получении данных пользователя:", error);
        }
    };

    useEffect(() => {
        getUserData();
    }, []);

    return (
        <div className="flex flex-col items-center w-64 min-w-64 shadow-lg h-full p-4 box-border">
            {userData ? (
                <>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    {userData.username}
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    Main
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    My ads
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    Wish list
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    Profile
                  </div>
                </>

            ) : (
                <>
                    <div>You are not logged in. Sign up or log in to open all features</div>
                    <button
                        className="mt-2 w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors duration-300"
                        onClick={openModal}
                    >
                      Sign Up
                    </button>

                    <button className="mt-2 w-full border border-blue-500 bg-transparent px-4 py-2 rounded-md text-blue-500 hover:bg-blue-100 transition-all duration-300">
                      Log In
                    </button>
                </>
            )}
            <SignupModal isOpen={isModal} onClose={closeModal}/>
        </div>
    );
};

export default AsidePanel;