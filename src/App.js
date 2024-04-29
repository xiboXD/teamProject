// App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState(null);

  const handleGenerateImage = async () => {
    try {
      const response = await axios.post('http://localhost:5050/image/create', { prompt });
      setImage(response.data.image);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Discover AI Creations</h1>
        <div>
          <input
            id="promptInput"
            type="text"
            placeholder="Try 'Astronaut riding a dragon'"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>
        <button onClick={handleGenerateImage}>Create Artwork</button>
      </header>
      <div className="Style-section">
        <h2>Choose a Style</h2>
        {/* Add your style images here */}
      </div>
      <div className="Gallery-section">
        <h2>Inspiration Gallery</h2>
        {/* Add your gallery images here */}
      </div>
      <button>See more</button>
      <div className="Image-container">
        {image && <img src={`data:image/png;base64,${image}`} alt="Generated Image" />}
      </div>
    </div>
  );
}

export default App;
