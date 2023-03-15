const profileBtn = document.querySelector(".profile-btn");
const profileDiv = document.querySelector(".profile-div");
profileBtn.addEventListener("click", () => {
  if(profileDiv.classList.contains("hide")) {
    profileDiv.classList.remove("hide");
  } else {
    profileDiv.classList.add("hide")
  }
});

const showBidModal = (divId) => {
  if(isUserLoggedIn) {
    const bidModal = document.querySelector(`#${divId}`);
    bidModal.classList.remove("hide");
    document.body.style = "overflow: hidden;"
  } else {
    window.location = "/login?next=/";
  }
};
