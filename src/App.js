import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import CSS file for styling

function App() {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // State to track loading status
  const [error, setError] = useState(null); // State to track errors
  const [selectedStyle, setSelectedStyle] = useState('Pixel'); // Set default style to Pixel
  const [pastImages, setPastImages] = useState([]); // State to store past images
  const [showPastImages, setShowPastImages] = useState(false); // State to track visibility of past images

  useEffect(() => {
    if (showPastImages) {
      // Fetch past images when showPastImages state changes
      fetchPastImages();
    }
  }, [showPastImages]);

  const handleGenerateImage = async () => {
    setIsLoading(true); // Set loading state to true when image generation starts
    setError(null); // Reset error state
    try {
      // Append selected style to the prompt
      const promptWithStyle = `${prompt} with the style of ${selectedStyle}`;
      const response = await axios.post('http://localhost:5050/image/create', { prompt: promptWithStyle, style: selectedStyle });
      setImage(response.data.image);
    } catch (error) {
      console.error('Error generating image:', error);
      setError('An error occurred while generating the image. Please try again later.');
    } finally {
      setIsLoading(false); // Set loading state to false when image generation completes
    }
  };

  const handleSeeMore = () => {
    setShowPastImages(true);
  };

  const handleHidePastImages = () => {
    setShowPastImages(false); // Hide past images
  };

  const fetchPastImages = async () => {
    try {
      const response = await axios.get('http://localhost:5050/experiments/get-images');
      const pastImagesData = response.data;
      // Extract past images from the response and update state
      setPastImages(pastImagesData);
    } catch (error) {
      console.error('Error fetching past images:', error);
      // Handle error if needed
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Discover AI Creations</h1>
        <div className="input-container">
          <input
            className="prompt-input"
            type="text"
            placeholder="Enter your prompt here"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button className="generate-button" onClick={handleGenerateImage} disabled={isLoading || !selectedStyle}>
            {isLoading ? 'Generating Image...' : 'Create Artwork'}
          </button>
        </div>
      </header>
      <div className="style-section">
        <h2>Choose a Style</h2>
        <div className="style-buttons">
          <button className={`style-button ${selectedStyle === 'Pixel' ? 'selected' : ''}`} onClick={() => setSelectedStyle('Pixel')}>Pixel Style</button>
          <button className={`style-button ${selectedStyle === 'Disney' ? 'selected' : ''}`} onClick={() => setSelectedStyle('Disney')}>Disney Style</button>
          <button className={`style-button ${selectedStyle === 'Space' ? 'selected' : ''}`} onClick={() => setSelectedStyle('Space')}>Space</button>
          <button className={`style-button ${selectedStyle === 'Abstract' ? 'selected' : ''}`} onClick={() => setSelectedStyle('Abstract')}>Abstract</button>
          <button className={`style-button ${selectedStyle === 'Dark' ? 'selected' : ''}`} onClick={() => setSelectedStyle('Dark')}>Dark Theme</button>
        </div>
      </div>
      <div className="gallery-section">
        <h2>Inspiration Gallery</h2>
        {showPastImages ? (
          <button className="see-more-button" onClick={handleHidePastImages}>Hide</button>
        ) : (
          <button className="see-more-button" onClick={handleSeeMore}>See more</button>
        )}
      </div>
      <div className="image-container">
        {error && <div className="error-message">{error}</div>}
        {image && <img className="generated-image" src={`data:image/png;base64,${image}`} alt="Generated Image" />}
        {showPastImages && (
          <div className="image-grid">
            {/* Render past images in a grid */}
            {pastImages.length === 0 ? (
              // Render dummy boxes as placeholders
              Array.from({ length: 6 }, (_, index) => (
                <div className="image-grid-item placeholder" key={index}>
                  {/* Display placeholder text */}
                  Placeholder {index + 1}
                </div>
              ))
            ) : (
              // Render past images
              pastImages.map((imageBase64, index) => (
                <div className="image-grid-item" key={index}>
                  {/* Display past image */}
                  <img src={`data:image/png;base64,${imageBase64}`} alt={`Past Image ${index + 1}`} />
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
