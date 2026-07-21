document.addEventListener('DOMContentLoaded', function () {

  // Loading state on form submit
  const form = document.querySelector('form');
  const btn = document.querySelector('.btn-predict');

  if (form && btn) {
    form.addEventListener('submit', function () {
      btn.classList.add('loading');
      btn.querySelector('.btn-text').textContent = 'Analysing...';
      btn.querySelector('.spinner').style.display = 'block';
      btn.querySelector('.btn-icon').style.display = 'none';
      btn.disabled = true;
    });
  }

  // Animate confidence bar on result page
  const bar = document.getElementById('confidence-bar');
  if (bar) {
    const target = bar.getAttribute('data-width');
    setTimeout(() => {
      bar.style.width = target + '%';
    }, 300);
  }

});