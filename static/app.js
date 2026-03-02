// event listener
const signUpBtn = document.getElementById("signUpBtn");
const logInBtn = document.getElementById("logInBtn");
signUpBtn.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/signup";
});
logInBtn.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/create_destination";
});
//# sourceMappingURL=app.js.map