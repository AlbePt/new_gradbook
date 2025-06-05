import React from 'react';

const data = [
  { id: 1, name: 'Объект α', status: 'Активен', description: '…' },
  { id: 2, name: 'Объект β', status: 'Черновик', description: '…' },
];

export default function DataTable() {
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>№</th>
          <th>Название</th>
          <th>Статус</th>
          <th>Описание</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, idx) => (
          <tr key={item.id}>
            <td>{idx + 1}</td>
            <td>{item.name}</td>
            <td>{item.status}</td>
            <td>{item.description}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
