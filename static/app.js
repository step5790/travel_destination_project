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

// 1. Add 'ev' (or 'event') to the parameters
async function updateTravel(ev, travel_id) {
    // 2. Use ev.target instead of just 'event.target'
    const btn = ev.target;
    const form = btn.closest('form');
    
    // Now 'form' will be correctly defined
    const titleInput = form.querySelector('input[name="travel_title"]');
    const descInput = form.querySelector('textarea[name="travel_description"]');
    const travelInput = form.querySelector('input[name="travel_location"]')
    const countryInput = form.querySelector('input[name="travel_country"]')
    const fromInput = form.querySelector('input[name="travel_from_date"]')
    const toInput = form.querySelector('input[name="travel_to_date"]')

    const newTitle = titleInput.value;
    const newDescription = descInput.value;
    const newLocation = travelInput.value;
    const newCountry = countryInput.value;
    const newFromDate = fromInput.value;
    const newToDate = toInput.value;

    try {
        const response = await fetch(`/travels/${travel_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "travel_title": newTitle,
                "travel_description": newDescription ,
                "travel_location": newLocation,
                "travel_country": newCountry,
                "travel_from_date": newFromDate,
                "travel_to_date": newToDate
            })
        });

        if (response.ok) {
            console.log("Updated!");
            // Success feedback all input
            [titleInput, descInput, travelInput, countryInput, fromInput, toInput].forEach(el => {
                el.style.backgroundColor = "#d4edda";
                setTimeout(() => el.style.backgroundColor = "white", 1000);
            });
        }
    } catch (err) {
        console.error("Update failed:", err);
    }
}