const version = "1.2";
const CACHE_NAME = "pwa-cache-v1";
const urlsToCache = [
    "/hsnc_logo.78d9159f.png",
    "/sas_logo.6225b57f.png",
    "/r_logo.e040c57e.png"
];
self.addEventListener("install", (event)=>{
    event.waitUntil(caches.open(CACHE_NAME).then((cache)=>{
        return cache.addAll(urlsToCache);
    }));
});
self.addEventListener("fetch", (event)=>{
    event.respondWith(caches.match(event.request).then((response)=>{
        return response || fetch(event.request);
    }));
});
self.addEventListener("activate", (event)=>{
    const cacheWhitelist = [
        CACHE_NAME
    ];
    event.waitUntil(caches.keys().then((cacheNames)=>{
        return Promise.all(cacheNames.map((cacheName)=>{
            if (!cacheWhitelist.includes(cacheName)) return caches.delete(cacheName);
        }));
    }));
});

//# sourceMappingURL=service-worker.js.map
