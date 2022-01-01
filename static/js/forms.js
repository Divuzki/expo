let state = false;
let FirstLastName = document.querySelector(".first_and_last_name");
let username = document.querySelector("#id_Username");
let email = document.querySelector(".email");
let password = document.querySelector("#pwd input");
let password2 = document.querySelector("#pwd2");
let stateText = document.getElementById("stateChar");
let passwordStrength = document.getElementById("password-strength");
let similarInfo = document.querySelector(".similar-to-username div");
let lowUpperCase = document.querySelector(".low-upper-case div");
let number = document.querySelector(".one-number div");
let notFullNumber = document.querySelector(".not-full-number div");
let specialChar = document.querySelector(".one-special-char div");
let eightChar = document.querySelector(".eight-character div");
let submitBtn = document.querySelector(".submit-btn");
let BackBtn = document.querySelector(".back-btn");
let NextBtn = document.querySelector(".next-btn");

function NextFunc() {
  NextBtn.classList.add("none");
  FirstLastName.classList.add("none");
  document.querySelector(".username").classList.add("none");

  BackBtn.classList.remove("none");
  email.classList.remove("none");
  submitBtn.classList.remove("none");
  document.querySelector("#pwd").classList.remove("none");
  document.querySelector("#pwd2").classList.remove("none");
  window.location.hash = "#next";
}

function BackFunc() {
  NextBtn.classList.remove("none");
  FirstLastName.classList.remove("none");
  document.querySelector(".username").classList.remove("none");

  submitBtn.classList.add("none");
  BackBtn.classList.add("none");
  email.classList.add("none");
  document.querySelector("#pwd").classList.add("none");
  document.querySelector("#pwd2").classList.add("none");
  window.location.hash = "#back";
}

function UsernameToLower() {
  username.value = document.getElementById("id_Username").value.toLowerCase();
}
UsernameToLower();

if (NextBtn) {
  NextBtn.addEventListener("click", NextFunc);
  UsernameToLower();
}
if (BackBtn) {
  BackBtn.addEventListener("click", BackFunc);
  UsernameToLower();
}
if (window.location.hash === "#next") {
  BackFunc();
} else if (window.location.hash === "#back") {
  NextFunc();
} else {
  BackFunc();
  NextBtn.classList.add("none");
}
if (password2) {
  NextBtn.removeAttribute("disabled");
  NextBtn.classList.add("none");
  username.addEventListener("keyup", function () {
    UsernameToLower();
    if (username.value.length > 0) {
      document.querySelector("#pwd").classList.remove("disabled");
      document.querySelector("#pwd2").classList.remove("disabled");
      NextBtn.classList.remove("none");
    } else {
      document.querySelector("#pwd").classList.add("disabled");
      document.querySelector("#pwd2").classList.add("disabled");
      NextBtn.classList.add("none");
    }
    UsernameToLower();
  });
  password.addEventListener("keyup", function () {
    checkStrength(password.value);
    if (
      document.querySelector("#pwd").className.indexOf("none") < 0 &&
      document.querySelector("#pwd input").value.length > 0
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
    document.querySelector("#pwd2 input").setAttribute("type", "password");
    state = false;
  } else {
    document.getElementById("id_Password").setAttribute("type", "text");
    document.querySelector("#pwd2 input").setAttribute("type", "text");
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
    lowUpperCase.classList.replace("hide-svg", "show-svg");
    lowUpperCase.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".low-upper-case").classList.remove("none");
  } else {
    lowUpperCase.classList.replace("bg-green-400", "bg-gray-400");
    lowUpperCase.classList.replace("show-svg", "hide-svg");
  }

  //If it has numbers and characters
  if (
    !(password.match(/([0-9])/) && !password.match(/([A-Za-zA])/)) === true &&
    password.length > 0
  ) {
    strength += 1;
    notFullNumber.classList.replace("hide-svg", "show-svg");
    notFullNumber.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".not-full-number").classList.remove("none");
  } else {
    notFullNumber.classList.replace("bg-green-400", "bg-gray-400");
    notFullNumber.classList.replace("show-svg", "hide-svg");
  }

  //If it has numbers
  if (password.match(/([0-9])/)) {
    strength += 0.5;
    number.classList.replace("hide-svg", "show-svg");
    number.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".one-number").classList.remove("none");
  } else {
    number.classList.replace("bg-green-400", "bg-gray-400");
    number.classList.replace("show-svg", "hide-svg");
  }

  //If it has one special character
  if (password.match(/([!,%,&,@,#,$,^,*,?,_,~,₦])/)) {
    strength += 1.5;
    specialChar.classList.replace("hide-svg", "show-svg");
    specialChar.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".one-special-char").classList.remove("none");
  } else {
    specialChar.classList.replace("bg-green-400", "bg-gray-400");
    specialChar.classList.replace("show-svg", "hide-svg");
  }

  // If password is greater than 8
  if (password.length >= 8) {
    strength += 1.5;
    eightChar.classList.replace("hide-svg", "show-svg");
    eightChar.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".eight-character").classList.remove("none");
  } else {
    eightChar.classList.replace("bg-green-400", "bg-gray-400");
    eightChar.classList.replace("show-svg", "hide-svg");
  }
  //If password is greater than 11
  if (password.length > 11) {
    strength += 1;
  }

  // if password has similar text with username
  if (username.value.length > 0 && password.indexOf(username.value) === -1) {
    strength += 1;
    similarInfo.classList.replace("hide-svg", "show-svg");
    similarInfo.classList.replace("bg-gray-400", "bg-green-400");
    document.querySelector(".similar-to-username").classList.remove("none");
  } else {
    similarInfo.classList.replace("bg-green-400", "bg-gray-400");
    similarInfo.classList.replace("show-svg", "hide-svg");
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
  } else if (strength === 6) {
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
  } else if (strength > 6 || strength === 6.5) {
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
}
