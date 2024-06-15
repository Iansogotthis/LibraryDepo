
# Library Database Management System

Welcome to the Library Database Management System (LDMS), a comprehensive solution designed to streamline the management of library resources, including books and user accounts. This system is built with a focus on simplicity, efficiency, and scalability, making it an ideal choice for libraries of any size. Below, you will find detailed information about the system's features, technology stack, installation methods, usage instructions, and our future plans.

## Features

### User Management

- **Registration and Authentication**: Secure registration and login system for library users and administrators.
- **Role-Based Access Control**: Differentiated access levels for users and administrators to ensure system integrity.
- **Profile Management**: Users can view and update their personal information.

### Book Management

- **Cataloging**: Add, update, and delete book records, including title, author, year of publication, ISBN, and publisher information.
- **Search Functionality**: Advanced search options allowing users to find books by title, author, or publisher.
- **Borrowing System**: Users can borrow and return books, with the system tracking borrow dates and return dates.

### Administrative Features

- **User Role Management**: Admins can assign roles to users, controlling access to various parts of the system.
- **Book Inventory Management**: Comprehensive tools for managing the library's book inventory.
- **Borrowing Oversight**: Admins can view and manage all current and past borrowings.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQL (SQLite/PostgreSQL)
- **Authentication**: Flask-Login for session management and Werkzeug for password hashing

## Installation

### Prerequisites

- Python 3.6 or later
- pip (Python package installer)
- Virtual environment (recommended)

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-repository/library-database-management.git
    cd library-database-management
    ```

2. **Set Up a Virtual Environment (Optional)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the Database**

    ```bash
    flask db upgrade
    ```

5. **Run the Application**

    ```bash
    flask run
    ```

## Usage Instructions

- **Accessing the System**: Open your web browser and navigate to `http://127.0.0.1:5000/` to access the LDMS.
- **Registering a New User**: Click on the "Register" link and fill in the required information.
- **Logging In**: Use your credentials to log in and access the system.
- **Adding a New Book**: Navigate to the "Add Book" section and enter the book details.
- **Searching for Books**: Use the search bar to find books by title, author, or publisher.

## Future Plans

- **Mobile App**: Develop a mobile application to provide users with access on the go.
- **Recommendation System**: Implement a book recommendation system based on user preferences and borrowing history.
- **Internationalization**: Add support for multiple languages to cater to a global audience.

## Current Progress

- **Completed Features**: User registration, login, book addition, and basic search functionality.
- **In Development**: Borrowing system and administrative features.
- **Planned Features**: Mobile app and recommendation system.

## Contributing

We welcome contributions from the community! If you're interested in helping us improve the LDMS, please check out our contributing guidelines in the `CONTRIBUTING.md` file.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

For any queries or suggestions, please reach out to us at [mount88ian@gmail.com].

Thank you for considering the Library Database Management System for your library's needs. We're excited to work together with you to create a more organized and accessible library experience.

## Acknowledgments

We would like to thank the following individuals and organizations for their contributions to the development of this project:

- [Flask](https://flask.palletsprojects.com/) - The Python microframework that powers the LDMS.
- [SQLite](https://www.sqlite.org/) - The lightweight database engine used for local development.
- [Werkzeug](https://www.werkzeug.palletsprojects.com/) - The WSGI utility library that powers the LDMS.
  
