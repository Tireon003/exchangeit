import { useState } from 'react';
import axios from 'axios';

export const SignupModal = ({ isOpen, onClose }) => {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const validateUsername = (value) => {
    const regex = /^[A-Za-z0-9_-]{6,}$/;
    return regex.test(value);
  };

  const validatePassword = (value) => {
    const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d_\-\.+\*]{8,}$/;
    return regex.test(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateUsername(username)) {
      alert('Имя пользователя должно содержать только буквы, цифры, подчеркивания, дефисы, точки или звездочки и иметь длину не менее 6 символов.');
      return;
    }
    if (!validatePassword(password)) {
      alert('Пароль должен содержать хотя бы одну букву, одну цифру и иметь длину не менее 8 символов.');
      return;
    }
    if (password !== confirmPassword) {
      alert('Пароли не совпадают.');
      return;
    }

    try {
      await axios.post('http://localhost:8008/api/auth/signup', {
          username: username,
          password: password,
          }, {
          headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      ).then(res => {
          if (res.status === 201) {
              alert('Регистрация успешна!');
              onClose();
          } else {
              alert('Ошибка при регистрации:', res.data.detail.msg);
              onClose();
          }
      });

    } catch (error) {
      alert('Ошибка при регистрации:', error.message);
    } finally {
        setUsername('');
      setPassword('');
      setConfirmPassword('');
    }
  };

  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-10 rounded-lg shadow-xl w-full max-w-md">
            <h2 className="text-2xl font-bold mb-6">Sign Up</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="username" className="block mb-2">Username:</label>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="password" className="block mb-2">Password:</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="confirmPassword" className="block mb-2">Confirm password:</label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300">
                Submit
              </button>
            </form>
            <button onClick={onClose} className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition duration-300">
              Cancel
            </button>
          </div>
        </div>
      )}
    </>
  );
}

