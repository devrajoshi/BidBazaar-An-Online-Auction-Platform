const showToast = (message) => {
  const toast = document.getElementById("toast");
  const toastText = document.getElementById("toast-text");

  // Set the text of the toast
  toastText.innerText = message;

  // Remove the 'hidden' class to show the toast
  toast.classList.remove("hidden");

  // Hide the toast after 3 seconds
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}

const displayMessages = () => {
  // Check if there are any messages to display
  if (toastMessages.length > 0) {
    // Get the first message from the array
    const message = toastMessages.shift();

    // Display the message as a toast notification
    showToast(message);

    // Wait for the toast to disappear, then display the next message
    setTimeout(displayMessages, 3000);
  }
}

displayMessages();
