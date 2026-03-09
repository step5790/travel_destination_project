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