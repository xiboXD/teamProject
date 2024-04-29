// src/SearchBar.js
import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    // 调用后端 API，传递 query 参数
    // 例如使用 Axios 或 fetch
    // 这里只是一个示例，您需要根据实际情况进行调整
    onSearch(query);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Try 'Astronaut riding a dragon'"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchBar;
