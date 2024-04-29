// src/StyleSelector.js
import React from 'react';

const StyleSelector = ({ styles, onSelectStyle }) => {
  return (
    <div>
      <h2>Choose a Style</h2>
      {styles.map((style, index) => (
        <div key={index} onClick={() => onSelectStyle(style)}>
          <img src={style.thumbnail} alt={`Style ${index}`} />
          <p>{style.title}</p>
        </div>
      ))}
    </div>
  );
};

export default StyleSelector;
