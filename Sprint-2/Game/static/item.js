var itemPrice = "0";
var itemID = "";
  document.addEventListener('DOMContentLoaded', function () {
  const itemImages = document.querySelectorAll('.image-item');
  const itemName = document.getElementById('itemName');
  const itemDescription = document.getElementById('itemDescription');
  const itemDetails = document.getElementById('shopItemDetails');

  // Function to handle item click and fetch data
  function handleItemClick(event) {
    const imageId = event.currentTarget.getAttribute('id');
    itemID = imageId;
    const fetchURL = `/get_item_info?image_id=${encodeURIComponent(imageId)}`;

    fetch(fetchURL) // Send GET request with image_id
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Update name and description elements
        itemName.textContent = imageId;
        itemDescription.textContent = data.description;

        // Update itemDetails list
        itemDetails.innerHTML = ''; // Clear existing content
        for (const key in data) {
          if (key !== 'name' && key !== 'description' && data.hasOwnProperty(key)) {
            if (key == 'price'){
                itemPrice = data[key]
            }
            const value = data[key];
            const listItem = document.createElement('li');
            listItem.textContent = `${key}: ${value}`;
            itemDetails.appendChild(listItem);
          }
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Attach click event listener to each item image
  itemImages.forEach(itemImage => {
    itemImage.addEventListener('click', handleItemClick);
  });
});

function Confirm(){
if(playerCurrency >=  itemPrice){
    document.getElementById('funds').textContent = "How many would you like to buy?";
    const updateCurrency = playerCurrency - itemPrice;
    console.log("Confirm")
    const requestData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ currency: updateCurrency, item: itemID }),
    };

  // Make the fetch request
  fetch('/update_currency', requestData)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Server response:', data);
      playerCurrency = data.currency;
      console.log(playerCurrency);
      if (data && data.success && typeof data.currency !== 'undefined') {
          const receivedCurrency = data.currency; // Extract currency value
          console.log('Received Currency:', receivedCurrency);

          // Now you can use 'receivedCurrency' variable as needed
          // For example, update UI with the new currency value
          document.getElementById('currencyDisplay').textContent = "Player Currency: " + receivedCurrency;
        } else {
          throw new Error('Invalid server response');
        }
      // Handle success response as needed
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      // Handle errors
    });
  }
  else{
    document.getElementById('funds').textContent = "Insufficient Funds";
  }
}
