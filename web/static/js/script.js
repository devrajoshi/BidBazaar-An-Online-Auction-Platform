const profileBtn = document.querySelector(".profile-btn");
const profileDiv = document.querySelector(".profile-div");
profileBtn.addEventListener("click", () => {
  if(profileDiv.classList.contains("hide")) {
    profileDiv.classList.remove("hide");
  } else {
    profileDiv.classList.add("hide")
  }
});
