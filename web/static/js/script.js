const profileBtn = document.querySelector(".profile-btn");
const profileDiv = document.querySelector(".profile-div");
profileBtn.addEventListener("click", () => {
  if(profileDiv.classList.contains("hide")) {
    profileDiv.classList.remove("hide");
  } else {
    profileDiv.classList.add("hide")
  }
});

const createBidModal = (bid) => {
  return `
    <div class="bid-modal">
      <div style="display: flex; justify-content: end;">
        <button onclick="document.querySelector('.bid-modal-container').classList.add('hide'); document.body.style = 'overflow: auto;'">X</button>
      </div>
      <div style="display: flex; gap: 10px;">
        <div style="max-width: 300px;"><img src="/uploads/${bid.image}" style="width: 100%;" /></div>
        <div style>
          <h3>${bid.title}</h3>
          <br />
          <div>${bid.description}</div>
          <br />
          <div>
            <input type="number" min="${bid.price}" value="${bid.price}" style="height: 30px;" />
            <button class="button" style="width: 70px; height: 30px; font-size: 18px;">Bid</button>
          </div>
        </div>
      </div>
    </div>
  `;
};

const showBidModal = (bid) => {
  if(isUserLoggedIn) {
    const bidModal = document.querySelector(".bid-modal-container");
    const bidObj = JSON.parse(bid);
    bidModal.innerHTML = createBidModal(bidObj);
    bidModal.classList.remove("hide");
    document.body.style = "overflow: hidden;"
  } else {
    window.location = "/login?next=/";
  }
};
