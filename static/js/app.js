var csrf = (document.querySelector('meta[name="csrf"]') || {}).content;

// like / unlike without reloading the page
document.addEventListener("click", function (e) {
  var b = e.target.closest("button.like[data-url]");
  if (!b) return;
  e.preventDefault();
  fetch(b.dataset.url, {
    method: "POST",
    headers: {"X-CSRFToken": csrf, "X-Requested-With": "XMLHttpRequest"}
  }).then(function (r) { return r.json(); }).then(function (d) {
    b.classList.toggle("on", d.liked);
    b.setAttribute("aria-pressed", d.liked);
    b.querySelector(".n").textContent = d.count;
  });
});

// confirm before deleting
document.querySelectorAll("[data-confirm]").forEach(function (el) {
  el.addEventListener("click", function (e) {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// live character counter on post / comment boxes
document.querySelectorAll(".composer").forEach(function (f) {
  var t = f.querySelector("textarea"), c = f.querySelector(".count");
  var upd = function () { c.textContent = 280 - t.value.length; };
  t.addEventListener("input", upd); upd();
});

// hide flash messages after 5 seconds
setTimeout(function () {
  document.querySelectorAll(".msg").forEach(function (m) { m.style.display = "none"; });
}, 5000);
