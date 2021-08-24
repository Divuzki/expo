let state = false;
let FirstLastName = document.querySelector(".first_and_last_name");
let username = document.querySelector("#id_Username");
let email = document.querySelector(".email");
let password = document.querySelector("#pwd input");
let password2 = document.querySelector("#pwd2");
let stateText = document.getElementById("stateChar");
let passwordStrength = document.getElementById("password-strength");
let similarInfo = document.querySelector(".similar-to-username i");
let lowUpperCase = document.querySelector(".low-upper-case i");
let number = document.querySelector(".one-number i");
let notFullNumber = document.querySelector(".not-full-number i");
let specialChar = document.querySelector(".one-special-char i");
let eightChar = document.querySelector(".eight-character i");
let submitBtn = document.querySelector(".submit-btn");
let BackBtn = document.querySelector(".back-btn");
let NextBtn = document.querySelector(".next-btn");

function NextFunc() {
  BackBtn.classList.remove("none");
  NextBtn.classList.add("none");
  FirstLastName.classList.add("none");
  document.querySelector(".username").classList.add("none");
  email.classList.remove("none");
  submitBtn.classList.remove("none");
  document.querySelector("#pwd").classList.remove("none");
  window.location.hash = "#next";
}

function BackFunc() {
  BackBtn.classList.add("none");
  NextBtn.classList.remove("none");
  submitBtn.classList.add("none");
  FirstLastName.classList.remove("none");
  document.querySelector(".username").classList.remove("none");
  email.classList.add("none");
  document.querySelector("#pwd").classList.add("none");
  window.location.hash = "#back";
}
if (NextBtn) {
  NextBtn.addEventListener("click", NextFunc);
}
if (BackBtn) {
  BackBtn.addEventListener("click", BackFunc);
}
if (window.location.hash === "#back" || window.location.hash === "#next") {
  if (window.location.hash === "#next") {
    BackFunc();
  } else {
    NextFunc();
  }
}
if (password2) {
  document.querySelector("#pwd").classList.add("disabled");
  NextBtn.removeAttribute("disabled");
  NextBtn.classList.add("none");
  username.addEventListener("keyup", function () {
    if (username.value.length > 0) {
      document.querySelector("#pwd").classList.remove("disabled");
      document.querySelector("#pwd2").classList.remove("disabled");
      NextBtn.classList.remove("none");
    } else {
      document.querySelector("#pwd").classList.add("disabled");
      document.querySelector("#pwd2").classList.add("disabled");
      NextBtn.classList.add("none");
    }
  });
  password.addEventListener("keyup", function () {
    let pass = password.value;
    checkStrength(pass);
    if (
      password.value.length > 0 &&
      document.querySelector("#pwd").className.indexOf("none") !== 19
    ) {
      document.querySelector(".progress").classList.remove("none");
      stateText.classList.remove("none");
      password2.classList.remove("none");
    } else {
      stateText.classList.add("none");
      password2.classList.add("none");
    }
  });
}

function toggle() {
  if (state) {
    document.getElementById("id_Password").setAttribute("type", "password");
    state = false;
  } else {
    document.getElementById("id_Password").setAttribute("type", "text");
    state = true;
  }
}

function ShowmyPwdFunction(show) {
  hide = document.querySelector(".hide-pwd");
  show.classList.toggle("none");
  hide.classList.remove("none");
}
function HidemyPwdFunction(hide) {
  show = document.querySelector(".show-pwd");
  hide.classList.toggle("none");
  show.classList.remove("none");
}

function checkStrength(password) {
  let strength = 0;

  //If password contains both lower and uppercase characters
  if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
    strength += 1;
    lowUpperCase.classList.remove("fi-sr-circle");
    lowUpperCase.classList.add("fi-sr-check");
  } else {
    lowUpperCase.classList.add("fi-sr-circle");
    lowUpperCase.classList.remove("fi-sr-check");
  }

  if (username.value.length > 0 && password.indexOf(username.value) === -1) {
    strength += 0.5;
    similarInfo.classList.remove("fi-sr-circle");
    similarInfo.classList.add("fi-sr-check");
  } else {
    similarInfo.classList.add("fi-sr-circle");
    similarInfo.classList.remove("fi-sr-check");
  }

  //If it has numbers and characters
  if (
    !(password.match(/([0-9])/) && !password.match(/([A-Za-zA])/)) === true &&
    password.length > 0
  ) {
    strength += 1;
    notFullNumber.classList.remove("fi-sr-circle");
    notFullNumber.classList.add("fi-sr-check");
  } else {
    notFullNumber.classList.add("fi-sr-circle");
    notFullNumber.classList.remove("fi-sr-check");
  }

  //If it has numbers and characters
  if (password.match(/([0-9])/)) {
    strength += 0.5;
    number.classList.remove("fi-sr-circle");
    number.classList.add("fi-sr-check");
  } else {
    number.classList.add("fi-sr-circle");
    number.classList.remove("fi-sr-check");
  }

  //If it has one special character
  if (password.match(/([!,%,&,@,#,$,^,*,?,_,~,₦])/)) {
    strength += 1.5;
    specialChar.classList.remove("fi-sr-circle");
    specialChar.classList.add("fi-sr-check");
  } else {
    specialChar.classList.add("fi-sr-circle");
    specialChar.classList.remove("fi-sr-check");
  }

  // If password is greater than 8
  if (password.length > 8) {
    strength += 1.5;
    eightChar.classList.remove("fi-sr-circle");
    eightChar.classList.add("fi-sr-check");
  } else {
    eightChar.classList.add("fi-sr-circle");
    eightChar.classList.remove("fi-sr-check");
  }
  //If password is greater than 8
  if (password.length > 11) {
    strength += 1;
  }
  // If value is less than 2
  if (password.length < 1) {
    passwordStrength.classList.remove("progress-bar-warning");
    passwordStrength.classList.remove("progress-bar-success");
    passwordStrength.classList.add("progress-bar-danger");
    passwordStrength.style = "width: 0px";
  } else if (strength < 2.5) {
    passwordStrength.classList.remove("progress-bar-warning");
    passwordStrength.classList.remove("progress-bar-success");
    passwordStrength.classList.add("progress-bar-danger");
    stateText.innerText = "Weak";
    stateText.classList.add("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.remove("bg-green-400");
    stateText.classList.remove("bg-green-800");
    stateText.classList.remove("bg-yellow-900");
    stateText.classList.remove("bg-green");
    passwordStrength.style = "width: 10%";
  } else if (strength <= 3.5) {
    passwordStrength.classList.remove("progress-bar-warning");
    passwordStrength.classList.remove("progress-bar-success");
    passwordStrength.classList.remove("progress-bar-danger");
    stateText.innerText = "Less Weak";
    stateText.classList.add("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.remove("bg-green-400");
    stateText.classList.remove("bg-green-800");
    stateText.classList.remove("bg-yellow-900");
    stateText.classList.remove("bg-green");
    passwordStrength.style = "width: 35%";
  } else if (strength === 4 || strength === 4.5) {
    passwordStrength.classList.remove("progress-bar-success");
    passwordStrength.classList.remove("progress-bar-danger");
    passwordStrength.classList.add("progress-bar-warning");
    stateText.innerText = "Medium";
    stateText.classList.remove("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.remove("bg-green-400");
    stateText.classList.remove("bg-green-900");
    stateText.classList.add("bg-yellow-900");
    stateText.classList.remove("bg-green");
    passwordStrength.style = "width: 60%";
  } else if (strength === 5 || strength === 5.5) {
    passwordStrength.classList.add("progress-bar-success");
    passwordStrength.classList.remove("progress-bar-danger");
    passwordStrength.classList.remove("progress-bar-warning");
    stateText.innerText = "Strong";
    stateText.classList.remove("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.add("bg-green-400");
    stateText.classList.remove("bg-green-800");
    stateText.classList.remove("bg-yellow-900");
    stateText.classList.remove("bg-green");
    passwordStrength.style = "width: 70%";
  } else if (strength === 6 || strength === 6.5) {
    passwordStrength.classList.add("progress-bar-success");
    passwordStrength.classList.remove("progress-bar-danger");
    passwordStrength.classList.remove("progress-bar-warning");
    stateText.innerText = "Stronger";
    stateText.classList.remove("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.add("bg-green-400");
    stateText.classList.remove("bg-green-800");
    stateText.classList.remove("bg-yellow-900");
    stateText.classList.remove("bg-green");
    passwordStrength.style = "width: 80%";
  } else if (strength === 7) {
    passwordStrength.classList.remove("progress-bar-warning");
    passwordStrength.classList.remove("progress-bar-danger");
    passwordStrength.classList.add("progress-bar-success");
    stateText.innerText = "Very Strong";
    stateText.classList.remove("bg-red-900");
    stateText.classList.remove("bg-green-900");
    stateText.classList.add("bg-green-400");
    stateText.classList.remove("bg-green-800");
    stateText.classList.remove("bg-yellow-900");
    stateText.classList.add("bg-green");
    passwordStrength.style = "width: 100%";
  }
  console.log(strength);
}
