// event listener
const signUpBtn = document.getElementById("signUpBtn");
const logInBtn = document.getElementById("logInBtn");
signUpBtn.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/signup";
});
// logInBtn.addEventListener("click", function (event) {
//     event.preventDefault();
//     window.location.href = "/create_destination";
// });

async function deleteTravel(travelId) {
    if (!confirm("Are you sure you want to delete this?")) return;

    try {
        const response = await fetch(`/travels/${travelId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            // Remove the element from the HTML immediately
            const element = document.getElementById(`travel-${travelId}`);
            if (element) {
                element.style.transition = "opacity 0.5s";
                element.style.opacity = "0";
                setTimeout(() => element.remove(), 500);
            }
        } else {
            alert("Failed to delete from database.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function updateTravel(travel_id) {
    // 1. Find the button that was clicked
    const btn = event.target;
    // 2. Find the input field named 'travel_title' inside the same form
    const input = btn.closest('form').querySelector('input[name="travel_title"]');
    const newTitle = input.value;

    try {
        const response = await fetch(`/travels/${travel_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "travel_title": newTitle })
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Success:", data);
            // Visual feedback: briefly highlight the input green
            input.style.backgroundColor = "#d4edda";
            setTimeout(() => input.style.backgroundColor = "white", 1000);
        } else {
            alert("Update failed on server.");
        }
    } catch (ex) {
        console.error("External error:", ex);
    }
}