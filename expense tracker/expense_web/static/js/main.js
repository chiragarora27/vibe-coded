/* main.js — global UI interactions */

// ── Sidebar mobile toggle ─────────────────────────────────────
const sidebar     = document.getElementById('sidebar');
const menuToggle  = document.getElementById('menuToggle');

if (menuToggle && sidebar) {
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !menuToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ── Password visibility toggle ────────────────────────────────
document.querySelectorAll('.toggle-pw').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.closest('.input-wrap').querySelector('input');
    input.type  = input.type === 'password' ? 'text' : 'password';
  });
});

// ── Auto-dismiss flash messages after 4 s ────────────────────
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .3s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 300);
  }, 4000);
});
