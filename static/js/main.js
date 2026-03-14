
// Lógica do Tema Dark/Light
const themeHtml = document.getElementById('theme-html');
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const savedTheme = localStorage.getItem('theme') || 'light';
themeHtml.setAttribute('data-bs-theme', savedTheme);

themeToggle.addEventListener('click', () => {
  const currentTheme = themeHtml.getAttribute('data-bs-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  themeHtml.setAttribute('data-bs-theme', newTheme);
  localStorage.setItem('theme', newTheme);
});

// Lógica de Expandir/Recolher Sidebar
const toggleBtn = document.getElementById('toggleSidebar');
const body = document.body;
const toggleIcon = document.getElementById('toggleIcon');

toggleBtn.addEventListener('click', () => {
  body.classList.toggle('sidebar-collapsed');
  if (body.classList.contains('sidebar-collapsed')) {
    toggleIcon.classList.replace('bi-chevron-left', 'bi-chevron-right');
  } else {
    toggleIcon.classList.replace('bi-chevron-right', 'bi-chevron-left');
  }
});