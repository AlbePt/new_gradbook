import React from 'react';

const info = {
  students: {
    icon: 'bi bi-people',
    title: 'Раздел «Ученики» в разработке',
    text: 'Здесь появится каталог учеников с фильтрами, поиском и импортом/экспортом данных.',
  },
  subjects: {
    icon: 'bi bi-book',
    title: 'Раздел «Предметы» в разработке',
    text: 'Управление учебными дисциплинами и назначением преподавателей.',
  },
  grades: {
    icon: 'bi bi-pencil',
    title: 'Раздел «Оценки» в разработке',
    text: 'Здесь будет электронный журнал для выставления и анализа оценок.',
  },
  teachers: {
    icon: 'bi bi-person-video',
    title: 'Раздел «Педагоги» в разработке',
    text: 'Здесь появятся отчёты для педагогов.',
  },
  admin: {
    icon: 'bi bi-building',
    title: 'Раздел «Администрация» в разработке',
    text: 'Здесь будут административные отчёты.',
  },
  ahc: {
    icon: 'bi bi-tools',
    title: 'Раздел «АХЧ» в разработке',
    text: 'Отчёты для хозяйственного отдела пока недоступны.',
  },
};

function PagePlaceholder({ page }) {
  const p = info[page] || {};
  return (
    <div className="placeholder">
      <i className={`${p.icon} fs-1`}></i>
      <h2>{p.title}</h2>
      <p>{p.text}</p>
    </div>
  );
}

export default PagePlaceholder;
