(function () {
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  var form = document.getElementById('bookingForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = form.elements;
    var err = form.querySelector('.form-error');
    if (!f.name.value.trim() || !f.phone.value.trim()) {
      err.classList.remove('d-none');
      return;
    }
    err.classList.add('d-none');
    var msg = 'Hi Krishna Aircons, I want to book a service.\n' +
      'Name: ' + f.name.value.trim() + '\n' +
      'Phone: ' + f.phone.value.trim() + '\n' +
      'Service: ' + f.service.value + '\n' +
      'Area: ' + f.area.value + '\n' +
      (f.message.value.trim() ? 'Details: ' + f.message.value.trim() : '');
    window.open('https://wa.me/918200937699?text=' + encodeURIComponent(msg), '_blank', 'noopener');
  });
})();
