/**
 * Placeholder – skeleton element used while data is loading.
 */
import React from 'react';

function Placeholder({ width = '100%', height = '1rem' }) {
  return <span className="placeholder" style={{ display: 'block', width, height }} />;
}

export default Placeholder;
