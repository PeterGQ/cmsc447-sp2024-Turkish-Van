//document.addEventListener('DOMContentLoaded', function () {
//    const items = document.querySelectorAll('.item');
//    const itemDetails = document.getElementById('itemDetails');
//
//    items.forEach(item => {
//        item.addEventListener('click', async function () {
//            const itemId = this.getAttribute('data-id');
//            try {
//                const response = await fetch('/get_item_info', {
//                    method: 'POST',
//                    headers: {
//                        'Content-Type': 'application/json'
//                    },
//                    body: JSON.stringify({ id: itemId })
//                });
//                if (!response.ok) {
//                    throw new Error('Network response was not ok');
//                }
//                const itemInfo = await response.json();
//                // Update itemDetails box content
//                itemDetails.innerHTML = `
//                    <p>Price: ${itemInfo.price}</p>
//                    <p>Buffs: ${itemInfo.buffs}</p>
//                    <p>Side Effects: ${itemInfo.sideEffects}</p>
//                `;
//                itemDetails.style.display = 'block'; // Show the box
//            } catch (error) {
//                console.error('Error:', error);
//            }
//        });
//    });
//
//    // Close the itemDetails box when clicking outside of it
//    document.addEventListener('click', function (event) {
//        if (!itemDetails.contains(event.target)) {
//            itemDetails.style.display = 'none'; // Hide the box
//        }
//    });
//});'

document.addEventListener('DOMContentLoaded', function () {
  const itemImages = document.querySelectorAll('.image-item');
  const itemName = document.getElementById('itemName');
  const itemDescription = document.getElementById('itemDescription');
  const itemDetails = document.getElementById('shopItemDetails');

  // Function to handle item click and fetch data
  function handleItemClick(event) {
    const imageId = event.currentTarget.getAttribute('data-imageid');
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
        itemName.textContent = data.name;
        itemDescription.textContent = data.description;

        // Update itemDetails list
        itemDetails.innerHTML = ''; // Clear existing content
        for (const key in data) {
          if (key !== 'name' && key !== 'description' && data.hasOwnProperty(key)) {
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


//document.addEventListener('DOMContentLoaded', function () {
//  const itemImage = document.getElementById('Potion of Healing');
//  const itemDetails = document.getElementById('shopItemDetails');
//  const itemName = document.getElementById('itemName');
//  const itemDescription = document.getElementById('itemDescription');
//
//  itemImage.addEventListener('click', function () {
//    const fetchURL = `/get_item_info?image_id=${encodeURIComponent(itemImage.id)}`;
//
//    fetch(fetchURL) // Send GET request with image_id
//      .then(response => {
//        if (!response.ok) {
//          throw new Error('Network response was not ok');
//        }
//        return response.json();
//      })
//      .then(data => {
//        // Update itemDetails with received data
//        itemName.textContent = "Name:"+data.name;
//        itemDescription.textContent = "Description:"+data.description;
//        itemDetails.innerHTML = ''; // Clear existing content
//        for (const key in data) {
//          if (key !== 'name' && key !== 'description' && data.hasOwnProperty(key)) {
//            const value = data[key];
//            const listItem = document.createElement('li');
//            listItem.textContent = `${key}: ${value}`;
//            itemDetails.appendChild(listItem);
//          }
//        }
//      })
//      .catch(error => {
//        console.error('Error:', error);
//      });
//  });
//
//});
