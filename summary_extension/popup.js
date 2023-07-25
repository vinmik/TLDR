// Add event listener to the "copyButton" once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("copyButton").addEventListener("click", copyText);
  });
  
  function copyText() {
    // Send a message to the content script to get the selected text
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const activeTab = tabs[0];
      if (!activeTab || !activeTab.id) {
        // Handle error when active tab is not available
        console.error("Error: Unable to access the active tab.");
        return;
      }
  
      // Send a message to the content script
      chrome.tabs.sendMessage(activeTab.id, { action: "getSelectedText" }, function(response) {
        if (!response || !response.text) {
          console.error("Error: No text received from the content script.");
          return;
        }
  
        // Send the selected text to the backend server
        fetch("http://localhost:5000/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ text: response.text })
        })
          .then(response => response.json())
          .then(data => {
            // Handle the response from the backend server and update the "keyPhrases" and "summary" elements with the analyzed data
            if (data && data.summary) {
              document.getElementById("summary").textContent = data.summary;
            } else {
              console.error("Error: Unable to get analyzed data from the backend.");
            }
          })
          .catch(error => {
            console.error("Error fetching data from the backend:", error);
          });
      });
    });
  }
  