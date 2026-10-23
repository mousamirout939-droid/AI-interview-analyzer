/**
 * main.js
 * =========
 * Small progressive-enhancement script shared across pages: flash message
 * auto-dismiss, upload drag-and-drop UX, and animated score bar fill.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss flash messages after 5 seconds
  document.querySelectorAll(".flash").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity 0.4s ease";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 400);
    }, 5000);
  });

  // Animate score bars from 0 to their target width on load
  document.querySelectorAll(".score-fill").forEach(function (bar) {
    var target = bar.getAttribute("data-width") || "0%";
    bar.style.width = "0%";
    requestAnimationFrame(function () {
      setTimeout(function () { bar.style.transition = "width 0.9s cubic-bezier(.2,.8,.2,1)"; bar.style.width = target; }, 80);
    });
  });

  // Upload drag-and-drop enhancement
  var dropZone = document.querySelector(".upload-drop");
  var fileInput = document.querySelector("#media_file");
  var fileLabel = document.querySelector("#file-chosen-label");

  if (dropZone && fileInput) {
    ["dragenter", "dragover"].forEach(function (evt) {
      dropZone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropZone.classList.add("dragover");
      });
    });
    ["dragleave", "drop"].forEach(function (evt) {
      dropZone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropZone.classList.remove("dragover");
      });
    });
    dropZone.addEventListener("drop", function (e) {
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        updateFileLabel();
      }
    });
    fileInput.addEventListener("change", updateFileLabel);

    function updateFileLabel() {
      if (fileLabel && fileInput.files.length) {
        fileLabel.textContent = "Selected: " + fileInput.files[0].name;
      }
    }
  }

  // Show a processing overlay on upload form submit (analysis can take a few seconds)
  var uploadForm = document.querySelector("#upload-form");
  var submitBtn = document.querySelector("#upload-submit-btn");
  if (uploadForm && submitBtn) {
    uploadForm.addEventListener("submit", function () {
      submitBtn.disabled = true;
      submitBtn.textContent = "Analyzing your interview...";
    });
  }
});
