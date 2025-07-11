/**
 * DataTable – responsive table wrapper with horizontal scroll.
 */
import React from 'react';

function DataTable({ children }) {
  return (
    <div className="table-responsive" style={{ overflowX: 'auto' }}>
      <table className="table table-sm mb-0">{children}</table>
    </div>
  );
}

export default DataTable;
