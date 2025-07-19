const CACHE_NAME = "lims-v3";
const urlsToCache = [
  "/",
  "/static/css/styles.css",
  "/static/js/pwa.js",
  "/offline.html"
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(urlsToCache)));
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});