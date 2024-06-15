import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ user, logout }) => {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [year, setYear] = useState('');
  const [isbn, setIsbn] = useState('');
  const [publisher, setPublisher] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = () => {
    axios.get('/api/books')
      .then(response => setBooks(response.data))
      .catch(err => console.error(err));
  };

  const handleAddBook = (e) => {
    e.preventDefault();
    axios.post('/api/book', { title, author, year, isbn, publisher, description })
      .then(() => {
        loadBooks();
        setTitle('');
        setAuthor('');
        setYear('');
        setIsbn('');
        setPublisher('');
        setDescription('');
      })
      .catch(err => alert('Failed to add book'));
  };

  const handleBorrowBook = (bookId) => {
    axios.post(`/api/borrow/${bookId}`)
      .then(() => loadBooks())
      .catch(err => alert('Failed to borrow book'));
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <h2>Dashboard</h2>
        <button onClick={logout} className="logout-button">Logout</button>
        {user.role === 'admin' && (
          <form onSubmit={handleAddBook} className="add-book-form">
            <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
            <input type="text" placeholder="Author" value={author} onChange={(e) => setAuthor(e.target.value)} required />
            <input type="number" placeholder="Year" value={year} onChange={(e) => setYear(e.target.value)} required />
            <input type="text" placeholder="ISBN" value={isbn} onChange={(e) => setIsbn(e.target.value)} required />
            <input type="text" placeholder="Publisher" value={publisher} onChange={(e) => setPublisher(e.target.value)} />
            <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)}></textarea>
            <button type="submit" className="submit-button">Add Book</button>
          </form>
        )}
        <ul className="book-list">
          {books.map(book => (
            <li key={book.id} className="book-item">
              <div className="book-details">
                <strong>{book.title}</strong> by {book.author} ({book.year}) <br />
                ISBN: {book.isbn} <br />
                Publisher: {book.publisher} <br />
                Description: {book.description}
              </div>
              {user.role === 'user' && <button onClick={() => handleBorrowBook(book.id)} className="borrow-button">Borrow</button>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
