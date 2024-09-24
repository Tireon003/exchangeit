import {useState, useEffect, useMemo} from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import {SignupModal} from '../components/SignupModal'
import {LoginModal} from '../components/LoginModal'
import { jwtDecode } from 'jwt-decode';


const AsidePanel = () => {

    const [userData, setUserData] = useState(null);
    const [isSignupModal, setIsSignupModal] = useState(false);
    const [isLoginModal, setIsLoginModal] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const setLoggedParam = () => {
        setIsLoggedIn(true);
    }

    const closeSignupModal = () => {
        setIsSignupModal(false);
    }

    const openSignupModal = () => {
        setIsSignupModal(true);
    }

    const closeLoginModal = () => {
        setIsLoginModal(false);
    }

    const openLoginModal = () => {
        setIsLoginModal(true);
    }

    const getUserFromToken = (token) => {
        try {
            return jwtDecode(token);
        } catch {
            setIsLoggedIn(false);
        }
    }

    const checkUserLoggedIn = () => {
        try {
            const token = Cookies.get('access_token');
            if (!token) {
                setIsLoggedIn(false);
                setUserData(null);
                return;
            }
            const data = getUserFromToken(token);
            setUserData(data);
            setIsLoggedIn(true);
        } catch {
            setIsLoggedIn(false);
            setUserData(null);
        };
    };

    const logOutUser = () => {
        Cookies.remove('access_token');
        setUserData(null);
        setIsLoggedIn(false);
    };

    const getUserWishList = async () => {
        try {
            const token = Cookies.get('access_token');
            if (!token) {
                alert('Your token is missing. Check if you are logged in or try again');
                return null;
            }

            const response = await axios.get('http://localhost:8008/api/users/me/wishlist', {
                withCredentials: true,
                headers: {
                    'Authorization': 'Bearer ' + token,
                }
            });

            if (response.status === 200) {
                console.log(response.data); // Для проверки, можно оставить
                return response.data;
            } else {
                throw new Error('Something went wrong while getting wishlist. Try again later.');
            }
        } catch (error) {
            alert(error.message || 'An unknown error occurred');
            return null;
        }
    };

    useEffect(() => {
        checkUserLoggedIn();
    }, [isLoggedIn]);

    return (
        <div className="flex flex-col items-center w-64 min-w-64 shadow-lg h-full p-4 box-border">
            {userData ? (
                <>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    {userData.name}
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    Main
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    My ads
                  </div>
                  <div
                    className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer"
                    onClick={getUserWishList}
                  >
                    Wish list
                  </div>
                  <div className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer">
                    Profile
                  </div>
                  <div
                    className="p-2 mb-2 rounded-md hover:bg-gray-200 cursor-pointer"
                    onClick={logOutUser}
                  >
                    Log out
                  </div>
                </>

            ) : (
                <>
                    <div>You are not logged in. Sign up or log in to open all features</div>
                    <button
                        className="mt-2 w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors duration-300"
                        onClick={openSignupModal}
                    >
                      Sign Up
                    </button>

                    <button
                        className="mt-2 w-full border border-blue-500 bg-transparent px-4 py-2 rounded-md text-blue-500 hover:bg-blue-100 transition-all duration-300"
                        onClick={openLoginModal}
                    >
                      Log In
                    </button>
                </>
            )}
            <SignupModal isOpen={isSignupModal} onClose={closeSignupModal}/>
            <LoginModal isOpen={isLoginModal} onClose={closeLoginModal} setLogged={setLoggedParam}/>
        </div>
    );
};

export default AsidePanel;