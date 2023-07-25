 console.log("Content script is running.");

// document.addEventListener("DOMContentLoaded", function() {  
//     chrome.runtime.onConnect.addListener(function(port) {
//         port.onMessage.addListener(function(message) {
//           if (message.action === "getSelectedText") {
//             const selectedText = window.getSelection().toString().trim();
//             port.postMessage({ text: selectedText });
//           }
//         });
//       });
//   });

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "getSelectedText") {
      const selectedText = window.getSelection().toString().trim();
      sendResponse({ text: selectedText });
    }
  });
  