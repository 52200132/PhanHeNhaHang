import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({
    placeholder = 'Search...',
    onSearch,
    className = '',
    initialValue = '',
    autoFocus = false,
    disabled = false,
}) => {
    const [searchTerm, setSearchTerm] = useState(initialValue);

    const handleChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);

        if (onSearch) {
            onSearch(value);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (onSearch) {
            onSearch(searchTerm);
        }
    };

    return (
        <div className={`search-bar ${className}`}>
            <form onSubmit={handleSubmit}>
                <div className="search-bar__container">
                    <span className="search-bar__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                        </svg>
                    </span>
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={handleChange}
                        placeholder={placeholder}
                        className="search-bar__input"
                        autoFocus={autoFocus}
                        disabled={disabled}
                    />
                    {searchTerm && (
                        <button
                            type="button"
                            className="search-bar__clear"
                            onClick={() => {
                                setSearchTerm('');
                                if (onSearch) {
                                    onSearch('');
                                }
                            }}
                            aria-label="Clear search"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                            </svg>
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
};

// export { SearchBar };
export default SearchBar;
