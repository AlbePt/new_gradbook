/**
 * Card – simple container with header and body.
 */
import React from 'react';

function Card({ title, children }) {
  return (
    <div className="card h-100 shadow-sm border-0">
      <div className="card-body">
        {title && <h6 className="card-title text-muted">{title}</h6>}
        {children}
      </div>
    </div>
  );
}

export default Card;
