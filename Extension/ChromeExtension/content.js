// content.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getURL') {
      console.log('Test message received in content script!');
      sendResponse({ url: window.location.href });
    }
  });
  