document.addEventListener("DOMContentLoaded", function() {
    const btn1 = document.getElementById("btn1");
    const btn2 = document.getElementById("btn2");

    btn1.addEventListener("click", function() {
        sendDataToFlask("btn1_clicked");
    });

    btn2.addEventListener("click", function() {
        sendDataToFlask("btn2_clicked");
    });

    function sendDataToFlask(buttonId) {
        // Make an AJAX request to Flask
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/handle_button_click", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Request successful
                    window.location.href = xhr.responseText; // Redirect to the rendered HTML file
                } else {
                    // Handle error
                    console.error("Error:", xhr.statusText);
                }
            }
        };
        const data = JSON.stringify({ buttonId: buttonId });
        xhr.send(data);
    }
});
