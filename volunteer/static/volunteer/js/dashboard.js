document.addEventListener("DOMContentLoaded", function () {
  // Xử lý nút Yêu thích
  document.querySelectorAll(".like-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const eventId = this.getAttribute("data-event-id");
      const likeUrl = this.getAttribute("data-like-url"); // Lấy URL từ data-like-url
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content"); // Lấy CSRF token từ meta tag
      fetch(likeUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const likeCount = this.querySelector(".like-count");
          likeCount.textContent = data.like_count;
          if (data.liked) {
            this.classList.add("liked");
          } else {
            this.classList.remove("liked");
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Xử lý nút Chia sẻ
  document.querySelectorAll(".share-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const eventId = this.getAttribute("data-event-id");
      const shareUrl = this.getAttribute("data-share-url"); // Lấy URL từ data-share-url
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content"); // Lấy CSRF token từ meta tag
      fetch(shareUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const shareCount = this.querySelector(".share-count");
          shareCount.textContent = data.shares;
          const eventUrl = `${window.location.origin}/events/${eventId}/`;
          // Hiển thị liên kết trong modal
          const shareLinkInput = document.getElementById("shareLink");
          shareLinkInput.value = eventUrl;
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Xử lý nút Sao chép trong modal
  document
    .getElementById("copyLinkButton")
    .addEventListener("click", function () {
      const shareLinkInput = document.getElementById("shareLink");
      shareLinkInput.select();
      navigator.clipboard
        .writeText(shareLinkInput.value)
        .then(() => {
          alert("Liên kết đã được sao chép!");
        })
        .catch((error) => {
          console.error("Error copying link:", error);
        });
    });
});
