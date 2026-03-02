// event listener
const signUpBtn = document.getElementById("signUpBtn");
const logInBtn = document.getElementById("logInBtn");
signUpBtn.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "page_signup.html";
});
logInBtn.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "page_create_destination.html";
});
//# sourceMappingURL=app.js.map