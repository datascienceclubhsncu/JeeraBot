function showOfflinePopup() {
    const offlinePopup = document.getElementById('offlinePopup');
    offlinePopup.classList.remove('hidden');
    document.body.style.pointerEvents = 'none';
 }
 
 function hideOfflinePopup() {
    const offlinePopup = document.getElementById('offlinePopup');
    offlinePopup.classList.add('hidden');
    document.body.style.pointerEvents = 'auto';
 }
 
 
 if (!navigator.onLine) {
     showOfflinePopup();
 }
 
 window.addEventListener('offline', () => {
     showOfflinePopup();
 });
 
 window.addEventListener('online', () => {
     hideOfflinePopup();
 });
 
 
 
 let deferredPrompt;
 
 window.addEventListener('beforeinstallprompt', (e) => {
   e.preventDefault();
   deferredPrompt = e;
   document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
         document.getElementById('pwa-banner').style.opacity = '0';
         document.getElementById('pwa-banner').style.bottom = '-200px';
      }
   })
   document.getElementById('pwa-banner').style.opacity = '1';
   document.getElementById('pwa-banner').style.bottom = '0';
 });
 
 document.getElementById('install-btn').addEventListener('click', () => {
   if (deferredPrompt) {
     deferredPrompt.prompt();
     deferredPrompt.userChoice.then((choiceResult) => {
       if (choiceResult.outcome === 'accepted') {
         console.log('User accepted the A2HS prompt');
       } else {
         console.log('User dismissed the A2HS prompt');
       }
       deferredPrompt = null;
     });
     document.getElementById('pwa-banner').style.display = 'none';
   }
 });
 
 document.getElementById('close-btn').addEventListener('click', () => {
   document.getElementById('pwa-banner').style.opacity = '0';
   document.getElementById('pwa-banner').style.bottom = '-200px';
 });
 
 
 document.addEventListener('contextmenu', event => event.preventDefault());
 
 document.onkeydown = function (e) {
     if (e.key === "F12" ||
         (e.ctrlKey && e.shiftKey && e.key === "I") ||
         (e.ctrlKey && e.key === "U")) {
         e.preventDefault();
         return false;
     }
 };
 
 /*window.addEventListener("blur", () => {
     window.open("", "_self");
     window.close();
 });*/
 
 
 if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/assets/service-worker.js')
      .then(registration => {
          console.log('Service Worker registered with scope:', registration.scope);
       })
       .catch(error => {
          console.error('Service Worker registration failed:', error);
       });
   });
 }
