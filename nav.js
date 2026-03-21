(function () {
  var path = window.location.pathname;

  // Normalise: /index.html → /
  if (path === '/index.html') path = '/';

  var rules = [
    { href: 'index.html', match: function (p) { return p === '/' || p.endsWith('/index.html'); } },
    { href: 'blog.html',  match: function (p) { return p.endsWith('/blog.html') || p.includes('/blog/'); } },
    { href: 'about.html', match: function (p) { return p.endsWith('/about.html'); } },
  ];

  var links = document.querySelectorAll('.nav__link');
  links.forEach(function (link) {
    var href = link.getAttribute('href');
    rules.forEach(function (rule) {
      if (href && href.includes(rule.href) && rule.match(path)) {
        link.classList.add('active');
      }
    });
  });
})();
