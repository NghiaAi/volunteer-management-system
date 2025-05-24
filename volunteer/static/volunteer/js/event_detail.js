document.addEventListener("DOMContentLoaded", function () {
  // Hàm tiện ích để hiển thị modal thông báo
  function showResultModal(message, isSuccess) {
    const resultModal = new bootstrap.Modal(
      document.getElementById("resultModal"),
      { backdrop: "static", keyboard: false }
    );
    const resultMessage = document.getElementById("result-message");
    resultMessage.className = "";
    resultMessage.innerText = message;
    resultMessage.classList.add(isSuccess ? "text-success" : "text-danger");
    resultModal.show();
  }

  // Hàm tiện ích để đóng modal và xóa backdrop
  function closeModal(modalElement) {
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
      modal.hide();
    }
    document.body.classList.remove("modal-open");
    document
      .querySelectorAll(".modal-backdrop")
      .forEach((backdrop) => backdrop.remove());
  }

  // Xử lý nút Yêu thích
  const likeBtn = document.getElementById("like-btn");
  if (likeBtn) {
    likeBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const likeUrl = this.getAttribute("data-like-url");
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content");
      if (!csrfToken) {
        console.error("CSRF token not found");
        showResultModal("Có lỗi xảy ra. Vui lòng thử lại.", false);
        return;
      }
      fetch(likeUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            console.error("Error:", data.error);
            showResultModal(data.error, false);
            return;
          }
          console.log("Like response:", data);
          document.getElementById("like-count").innerText = data.like_count;
          this.querySelector("i").classList.toggle("bi-heart-fill", data.liked);
          this.querySelector("i").classList.toggle("bi-heart", !data.liked);
          this.classList.toggle("liked", data.liked);
        })
        .catch((error) => {
          console.error("Fetch error:", error);
          showResultModal(
            "Có lỗi khi thực hiện yêu thích. Vui lòng thử lại.",
            false
          );
        });
    });
  } else {
    console.error("Like button not found");
  }

  // Xử lý nút Chia sẻ
  const shareBtn = document.getElementById("share-btn");
  if (shareBtn) {
    shareBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const shareUrl = this.getAttribute("data-share-url");
      const eventPk = this.getAttribute("data-event-pk");
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content");
      if (!csrfToken) {
        console.error("CSRF token not found");
        showResultModal("Có lỗi xảy ra. Vui lòng thử lại.", false);
        return;
      }
      fetch(shareUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            console.error("Error:", data.error);
            showResultModal(data.error, false);
            return;
          }
          console.log("Share response:", data);
          document.getElementById("share-count").innerText = data.shares;
          const eventUrl = `${window.location.origin}/events/${eventPk}/`;
          const shareLinkInput = document.getElementById("shareLink");
          if (shareLinkInput) {
            shareLinkInput.value = eventUrl;
            console.log("Share link set to:", eventUrl);
            const shareModal = new bootstrap.Modal(
              document.getElementById("shareModal"),
              { backdrop: "static", keyboard: false }
            );
            shareModal.show();
          } else {
            console.error("Share link input not found");
            showResultModal("Không tìm thấy ô nhập liên kết chia sẻ.", false);
          }
        })
        .catch((error) => {
          console.error("Fetch error:", error);
          showResultModal(
            "Có lỗi khi tạo liên kết chia sẻ. Vui lòng thử lại.",
            false
          );
        });
    });
  } else {
    console.error("Share button not found");
  }

  // Xử lý nút Sao chép liên kết
  const copyLinkButton = document.getElementById("copyLinkButton");
  if (copyLinkButton) {
    copyLinkButton.addEventListener("click", function () {
      const shareLinkInput = document.getElementById("shareLink");
      const copySuccessMessage = document.getElementById("copySuccessMessage");
      if (shareLinkInput && copySuccessMessage) {
        shareLinkInput.select();
        navigator.clipboard
          .writeText(shareLinkInput.value)
          .then(() => {
            copySuccessMessage.classList.remove("d-none");
            setTimeout(() => {
              copySuccessMessage.classList.add("d-none");
            }, 3000); // Ẩn sau 3 giây
          })
          .catch((error) => {
            console.error("Error copying link:", error);
            showResultModal("Có lỗi khi sao chép liên kết.", false);
          });
      } else {
        console.error("Share link input or success message not found");
        showResultModal("Không tìm thấy ô nhập liên kết chia sẻ.", false);
      }
    });
  }

  // Xử lý khi đóng modal chia sẻ
  const shareModal = document.getElementById("shareModal");
  if (shareModal) {
    shareModal.addEventListener("hidden.bs.modal", function () {
      document.body.classList.remove("modal-open");
      document
        .querySelectorAll(".modal-backdrop")
        .forEach((backdrop) => backdrop.remove());
      // Đảm bảo thông báo sao chép bị ẩn khi đóng modal
      const copySuccessMessage = document.getElementById("copySuccessMessage");
      if (copySuccessMessage) {
        copySuccessMessage.classList.add("d-none");
      }
    });
  }

  // Xử lý nút Đăng ký
  const joinBtn = document.getElementById("join-btn");
  if (joinBtn) {
    joinBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const confirmJoinModal = new bootstrap.Modal(
        document.getElementById("confirmJoinModal"),
        { backdrop: "static", keyboard: false }
      );
      confirmJoinModal.show();
    });
  }

  // Xử lý xác nhận đăng ký
  const confirmJoinBtn = document.getElementById("confirm-join");
  if (confirmJoinBtn) {
    confirmJoinBtn.addEventListener("click", function () {
      const joinUrl = this.getAttribute("data-join-url");
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content");
      if (!csrfToken) {
        console.error("CSRF token not found");
        showResultModal("Có lỗi xảy ra. Vui lòng thử lại.", false);
        return;
      }
      fetch(joinUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          closeModal(document.getElementById("confirmJoinModal"));
          if (data.error) {
            showResultModal(data.error, false);
            return;
          }
          showResultModal(data.success, true);
          const joinBtn = document.getElementById("join-btn");
          joinBtn.outerHTML = `
            <button class="btn btn-danger" id="leave-btn" data-bs-toggle="modal" data-bs-target="#confirmLeaveModal" data-leave-url="${joinUrl.replace(
              "join",
              "leave"
            )}">
              <i class="bi bi-x-circle"></i> Rời khỏi
            </button>
          `;
          document.getElementById("participant-count").innerText =
            data.participant_count;

          // Gắn lại trình xử lý sự kiện cho nút "Rời khỏi"
          const leaveBtn = document.getElementById("leave-btn");
          if (leaveBtn) {
            leaveBtn.addEventListener("click", function (e) {
              e.preventDefault();
              const confirmLeaveModal = new bootstrap.Modal(
                document.getElementById("confirmLeaveModal"),
                { backdrop: "static", keyboard: false }
              );
              confirmLeaveModal.show();
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          closeModal(document.getElementById("confirmJoinModal"));
          showResultModal("Có lỗi khi đăng ký. Vui lòng thử lại.", false);
        });
    });
  }

  // Xử lý nút Rời khỏi
  const leaveBtn = document.getElementById("leave-btn");
  if (leaveBtn) {
    leaveBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const confirmLeaveModal = new bootstrap.Modal(
        document.getElementById("confirmLeaveModal"),
        { backdrop: "static", keyboard: false }
      );
      confirmLeaveModal.show();
    });
  }

  // Xử lý xác nhận hủy đăng ký
  const confirmLeaveBtn = document.getElementById("confirm-leave");
  if (confirmLeaveBtn) {
    confirmLeaveBtn.addEventListener("click", function () {
      const leaveUrl = this.getAttribute("data-leave-url");
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content");
      if (!csrfToken) {
        console.error("CSRF token not found");
        showResultModal("Có lỗi xảy ra. Vui lòng thử lại.", false);
        return;
      }
      fetch(leaveUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          closeModal(document.getElementById("confirmLeaveModal"));
          if (data.error) {
            showResultModal(data.error, false);
            return;
          }
          showResultModal(data.success, true);
          const leaveBtn = document.getElementById("leave-btn");
          leaveBtn.outerHTML = `
            <button class="btn btn-success" id="join-btn" data-bs-toggle="modal" data-bs-target="#confirmJoinModal" data-join-url="${leaveUrl.replace(
              "leave",
              "join"
            )}">
              <i class="bi bi-check-circle"></i> Đăng ký
            </button>
          `;
          document.getElementById("participant-count").innerText =
            data.participant_count;

          // Gắn lại trình xử lý sự kiện cho nút "Đăng ký"
          const joinBtn = document.getElementById("join-btn");
          if (joinBtn) {
            joinBtn.addEventListener("click", function (e) {
              e.preventDefault();
              const confirmJoinModal = new bootstrap.Modal(
                document.getElementById("confirmJoinModal"),
                { backdrop: "static", keyboard: false }
              );
              confirmJoinModal.show();
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          closeModal(document.getElementById("confirmLeaveModal"));
          showResultModal("Có lỗi khi hủy đăng ký. Vui lòng thử lại.", false);
        });
    });
  }

  // Xử lý khi đóng modal thông báo
  const resultModal = document.getElementById("resultModal");
  if (resultModal) {
    resultModal.addEventListener("hidden.bs.modal", function () {
      document.body.classList.remove("modal-open");
      document
        .querySelectorAll(".modal-backdrop")
        .forEach((backdrop) => backdrop.remove());
    });
  }

  // Cập nhật số người tham gia động
  const eventDetailUrl = document
    .getElementById("event-detail-script")
    ?.getAttribute("data-event-detail-url");
  if (eventDetailUrl) {
    fetch(eventDetailUrl, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.participant_count !== undefined) {
          document.getElementById("participant-count").innerText =
            data.participant_count;
        }
      })
      .catch((error) =>
        console.error("Error updating participant count:", error)
      );
  }
});
