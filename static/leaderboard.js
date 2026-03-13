const CHALLENGES = ["reachable", "cors_origin", "options_supported", "methods_allowed", "headers_allowed", "post_success"];
const TOTAL = CHALLENGES.length;

function progressBar(score) {
  const filled = "█".repeat(score);
  const empty = "░".repeat(TOTAL - score);
  return filled + empty;
}

function check(val) {
  return val
    ? '<span class="pass">✓</span>'
    : '<span class="fail">✗</span>';
}

function fetchAndRender() {
  fetch("/teams")
    .then(r => r.json())
    .then(teams => {
      const tbody = document.getElementById("tbody");
      if (teams.length === 0) {
        tbody.innerHTML = '<tr><td class="empty" colspan="10">No teams registered yet.</td></tr>';
        return;
      }
      tbody.innerHTML = teams.map((team, i) => {
        const s = team.status;
        return `<tr>
          <td>${i + 1}</td>
          <td class="team-name">${escapeHtml(team.name)}</td>
          <td>${check(s.reachable)}</td>
          <td>${check(s.cors_origin)}</td>
          <td>${check(s.options_supported)}</td>
          <td>${check(s.methods_allowed)}</td>
          <td>${check(s.headers_allowed)}</td>
          <td>${check(s.post_success)}</td>
          <td class="score">${team.score}/${TOTAL}</td>
          <td class="progress">${progressBar(team.score)}</td>
        </tr>`;
      }).join("");
      document.getElementById("updated").textContent =
        "Last updated: " + new Date().toLocaleTimeString();
    })
    .catch(() => {
      document.getElementById("updated").textContent = "Error fetching data.";
    });
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

fetchAndRender();
setInterval(fetchAndRender, 3000);
