import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './BorrowedBooks.css';

const BorrowedBooks = ({ user, logout }) => {
  const [borrows, setBorrows] = useState([]);

  useEffect(() => {
    loadBorrows();
  }, []);

  const loadBorrows = () => {
    axios.get('/api/borrows')
      .then(response => setBorrows(response.data))
      .catch(err => console.error(err));
  };

  const handleReturnBook = (borrowId) => {
    axios.post(`/api/return/${borrowId}`)
      .then(() => loadBorrows())
      .catch(err => alert('Failed to return book'));
  };

  return (
    <div className="borrowed-books-container">
      <div className="borrowed-books-content">
        <h2>Borrowed Books</h2>
        <button onClick={logout} className="logout-button">Logout</button>
        <ul className="borrowed-books-list">
          {borrows.map(borrow => (
            <li key={borrow.id} className="borrowed-book-item">
              <div className="borrowed-book-details">
                <strong>{borrow.book.title}</strong> borrowed on {new Date(borrow.borrow_date).toLocaleDateString()}
              </div>
              <button onClick={() => handleReturnBook(borrow.id)} className="return-button">Return</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default BorrowedBooks;
