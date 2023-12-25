// popup.js
document.addEventListener('DOMContentLoaded', function() {
    var closeButton = document.getElementById('closeButton');
    var scrapButton = document.getElementById('scrapButton');
    var urlDisplay = document.getElementById('urlDisplay');
    var predictedProduct = document.getElementById('predictedProduct');
    var exstatus = document.getElementById('status');
    var initial = document.getElementById('ini')
  
    closeButton.addEventListener('click', function() {
      window.close(); // Close the popup when the button is clicked
    });
  
    scrapButton.addEventListener('click', function() {
      // Send a message from popup to content script
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getURL' }, function(response) {
          // Display the response in the popup
          if (chrome.runtime.lastError) {
            console.error('Error in chrome.tabs.sendMessage:', chrome.runtime.lastError.message);
            alert('Failed to send test message from popup script.');
          } else if (response && response.url) {
            initial.textContent='Processing Starts...'
            predictedProduct.textContent='Verifying..';
            fetch('http://127.0.0.1:5000/receive-url', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url: response.url }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Handle the response from the Flask app if needed
                        console.log(data);
                        if (data.status === 'success') {
                          exstatus.textContent=`Product and Logo Verified Successfully!`;
                          predictedProduct.textContent = `Verified - Product : ${data.predicted_product} , Its Probability : ${probprod}*100 and Logo Probability : ${problogo}`;
                        }
                        else if (data.status === 'partial1') {
                          exstatus.textContent=`Logo Verification Failed!!`;
                          predictedProduct.textContent = `Not Verified - Fake Logo or Logo doesn't exist!`;
                        }
                        else if (data.status === 'partial2') {
                          exstatus.textContent=`Logo Verification Failed!! `;
                          predictedProduct.textContent = `Not Verified - Product and Logo Mismatched!!`;
                        }
                        else if (data.status === 'partial3') {
                          exstatus.textContent=`Description Verification Failed!!`;
                          predictedProduct.textContent = `Verified -  Product and Description Mismatched!!`;
                        }
                        else if(data.status === 'failed'){
                          exstatus.textContent=`Product Verification Failed`;
                          predictedProduct.textContent = `Verified - Wrong Product `;
                        } 
                        else {
                          predictedProduct.textContent = 'Failed to predict product.';
                        }
                        initial.textContent='Process Finished...'
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
          } else {
            urlDisplay.textContent = 'Failed to receive URL from content script.';
          }
        });
      });
    });
  });
  