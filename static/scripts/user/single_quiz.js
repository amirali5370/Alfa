document.addEventListener("DOMContentLoaded", () => {
    const questions = document.querySelectorAll(".question-card");
    const markedCountEl = document.getElementById("markedCount");
    const answeredCountEl = document.getElementById("answeredCount");
    const allCountEl = document.getElementById("allCount");

    let markedCount = 0;
    let answeredCount = 0;
    allCountEl.textContent = questions.length;

    function renderCounters() {
      markedCountEl.textContent = markedCount;
      answeredCountEl.textContent = answeredCount;
    }

    questions.forEach(q => {
      const markBtn = q.querySelector(".mark-btn");
      const clearBtn = q.querySelector(".clear-btn");
      const radios = q.querySelectorAll("input[type=radio]");

      let isMarked = false;
      let hasAnswer = false;

      markBtn.addEventListener("click", () => {
        isMarked = !isMarked;
        q.classList.toggle("marked", isMarked);
        markedCount += isMarked ? 1 : -1;
        renderCounters();
      });

      clearBtn.addEventListener("click", () => {
        const wasAnswered = hasAnswer;
        radios.forEach(r => r.checked = false);
        if (wasAnswered) {
          hasAnswer = false;
          answeredCount--;
          renderCounters();
        }
      });

      radios.forEach(r => {
        r.addEventListener("change", () => {
          if (!hasAnswer) {
            hasAnswer = true;
            answeredCount++;
            renderCounters();
          }
        });
      });
    });

    renderCounters();
  });