// ImageCreateForm.js

import React, { useState } from 'react';
import axios from 'axios';

function ImageCreateForm() {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5050/image/create', { prompt });
      setImage(response.data.image);
    } catch (error) {
      console.error('Error creating image:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Prompt:
          <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        </label>
        <button type="submit">Generate Image</button>
      </form>
      {image && <img src={`data:image/png;base64,${image}`} alt="Generated" />}
    </div>
  );
}

export default ImageCreateForm;
