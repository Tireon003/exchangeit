// components/ContactModal.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ContactModal_style.css';


function ContactModal({ isOpen, onClose, adId }) {
  const [contactInfo, setContactInfo] = useState({
    telegram: '',
    email: '',
    phone_number: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen && adId) {
      fetchData(adId);
    }
  }, [isOpen, adId]);

  const fetchData = async (adId) => {
    try {
      setIsLoading(true);
      const response = await axios.get(`http://localhost:8008/api/ads/${adId}/contact`);
      setContactInfo({
        telegram: response.data.telegram || 'No Telegram',
        email: response.data.email || 'No email',
        phone_number: response.data.phone_number || 'No phone number'
      });
    } catch (err) {
      console.error('Error fetching contact info:', err);
      setError('Error loading contact information');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={`fixed inset-0 flex items-center justify-center ${isOpen ? 'z-50' : '-z-50'}`}>
      <div className={`absolute inset-0 ${isOpen ? 'bg-black opacity-50' : 'bg-white opacity-0'}`}></div>
      <div className={`modal-content ${isOpen ? 'scale-y-100 transform scale-y-100' : 'scale-y-0 transform scale-y-0'}`} onClick={handleClose}>
        <div className="bg-white rounded-lg w-full max-w-xs md:max-w-sm lg:max-w-md xl:max-w-lg">
          <header className="border-b flex items-center justify-between">
            <h2 className="text-xl font-semibold mt-0">Contact Information</h2>
            <button className="text-gray-400 hover:text-gray-500 focus:outline-none" onClick={onClose}>
              &times;
            </button>
          </header>
          <main className="space-y-4">
            {isLoading ? (
              <p>Loading...</p>
            ) : error ? (
              <p className="text-red-500">{error}</p>
            ) : (
              <>
                <p className="font-medium">Telegram: {contactInfo.telegram}</p>
                <p className="font-medium">Email: {contactInfo.email}</p>
                <p className="font-medium">Phone Number: {contactInfo.phone_number}</p>
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};


export default ContactModal;
