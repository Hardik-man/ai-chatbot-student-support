document.addEventListener("DOMContentLoaded", () => {
  const chatScroll = document.getElementById("chatScroll");
  const form = document.getElementById("composerForm");
  const input = document.getElementById("messageInput");
  const quickTopics = document.getElementById("quickTopics");
  const deskTitle = document.getElementById("deskTitle");
  const ticketIntent = document.getElementById("ticketIntent");
  const ticketNo = document.getElementById("ticketNo");

  let count = 0;

  const DESK_NAMES = {
    admissions: "Admissions",
    exams: "Exams & Grades",
    fees: "Fees & Scholarships",
    library: "Library",
    hostel: "Hostel Services",
    courses: "Course Registration",
    faculty_contact: "Faculty Contact",
    timetable: "Timetable",
    counseling: "Wellness & Counseling",
    it_support: "IT Helpdesk",
    grievance: "Grievance Cell",
    greeting: "General Inquiries",
    goodbye: "General Inquiries",
    thanks: "General Inquiries",
    fallback: "General Inquiries",
  };

  function scrollToBottom() {
    chatScroll.scrollTop = chatScroll.scrollHeight;
  }

  function addMessage(text, sender) {
    const wrap = document.createElement("div");
    wrap.className = `msg ${sender}`;
    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.textContent = text;
    wrap.appendChild(bubble);
    chatScroll.appendChild(wrap);
    scrollToBottom();
    return wrap;
  }

  function showTyping() {
    const wrap = document.createElement("div");
    wrap.className = "msg bot typing";
    wrap.id = "typingIndicator";
    wrap.innerHTML = `
      <div class="msg-bubble">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>`;
    chatScroll.appendChild(wrap);
    scrollToBottom();
  }

  function removeTyping() {
    const el = document.getElementById("typingIndicator");
    if (el) el.remove();
  }

  async function sendMessage(text) {
    addMessage(text, "user");
    input.value = "";
    showTyping();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      removeTyping();

      if (!res.ok) {
        addMessage("Something went wrong reaching the support desk. Please try again.", "bot");
        return;
      }

      addMessage(data.reply, "bot");

      count += 1;
      ticketNo.textContent = String(count).padStart(4, "0");
      ticketIntent.textContent = (data.intent || "general").replace(/_/g, " ");
      deskTitle.textContent = DESK_NAMES[data.intent] || "General Inquiries";

      document.querySelectorAll(".directory-list li").forEach((li) => li.classList.remove("active"));
      const match = [...document.querySelectorAll(".directory-list li")].find(
        (li) => (DESK_NAMES[data.intent] || "") === li.textContent.replace(/^\d+/, "").trim()
      );
      if (match) match.classList.add("active");
    } catch (err) {
      removeTyping();
      addMessage("I couldn't reach the server. Please check your connection and try again.", "bot");
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    sendMessage(text);
  });

  quickTopics.addEventListener("click", (e) => {
    const li = e.target.closest("li[data-msg]");
    if (!li) return;
    sendMessage(li.dataset.msg);
  });

  input.focus();
});
