const API_URL = 'http://localhost:8000';
let token = localStorage.getItem('token');

function showLogin(show) {
  document.getElementById('loginPane').classList.toggle('d-none', !show);
  document.getElementById('contentPane').classList.toggle('d-none', show);
}

async function login(username, password) {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: form.toString()
  });
  if (!res.ok) throw new Error('Login failed');
  const data = await res.json();
  token = data.access_token;
  localStorage.setItem('token', token);
}

async function fetchGrades() {
  const res = await fetch(`${API_URL}/grades`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch grades');
  return await res.json();
}

function calcStats(grades) {
  let sum = 0;
  const byStudent = {};
  for (const g of grades) {
    const v = parseFloat(g.value);
    sum += v;
    byStudent[g.student_id] = (byStudent[g.student_id] || []).concat(v);
  }
  const avg = grades.length ? (sum / grades.length).toFixed(2) : '–';
  let excellent = 0;
  let failing = 0;
  Object.values(byStudent).forEach(arr => {
    const avgG = arr.reduce((a,b)=>a+b,0)/arr.length;
    if (avgG >= 4.5) excellent++;
    if (avgG < 3) failing++;
  });
  return { avg, excellent, failing };
}

async function updateDashboard() {
  try {
    const grades = await fetchGrades();
    const stats = calcStats(grades);
    document.getElementById('avgGrade').textContent = stats.avg;
    document.getElementById('excellentCount').textContent = stats.excellent;
    document.getElementById('failingCount').textContent = stats.failing;
  } catch (e) {
    console.error(e);
  }
}

if (token) {
  showLogin(false);
  updateDashboard();
} else {
  showLogin(true);
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const u = document.getElementById('username').value;
  const p = document.getElementById('password').value;
  try {
    await login(u, p);
    showLogin(false);
    updateDashboard();
  } catch (err) {
    alert('Ошибка входа');
  }
});

document.getElementById('logoutBtn').addEventListener('click', () => {
  localStorage.removeItem('token');
  token = null;
  showLogin(true);
});
