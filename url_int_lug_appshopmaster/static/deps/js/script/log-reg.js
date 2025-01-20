// Variable Declaration
const loginBtn = document.querySelector("#login");
const registerBtn = document.querySelector("#register");
const loginForm = document.querySelector(".login__form__log");
const registerForm = document.querySelector(".register__form__log");


// Login button function
loginBtn.addEventListener('click', () => {
	loginBtn.style.backgroundColor = "rgba(44, 70, 129, 0.89)"
	registerBtn.style.backgroundColor = "hsla(222, 47%, 11%, 1)";

	loginForm.style.left = "50%";
	registerForm.style.left = "-50%";

	loginForm.style.opacity = 1;
	registerForm.style.opacity = 0;

	document.querySelector(".col__1").style.borderRadius = "0 30% 20% 0";
})

registerBtn.addEventListener('click', () => {
	loginBtn.style.backgroundColor = "hsla(222, 47%, 11%, 1)";
	registerBtn.style.backgroundColor = "rgba(44, 70, 129, 0.89)"

	loginForm.style.left = "150%";
	registerForm.style.left = "50%";

	loginForm.style.opacity = 0;
	registerForm.style.opacity = 1;

	document.querySelector(".col__1").style.borderRadius = "0 20% 30% 0";
})



// Register button function


