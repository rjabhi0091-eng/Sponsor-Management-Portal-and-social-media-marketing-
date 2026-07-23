const sponsorSearch = document.getElementById("sponsor-search");
const clientSearch = document.getElementById("client-search");
const manageSponsorsBtn = document.getElementById("manage-sponsors-btn");
const manageClientsBtn = document.getElementById("manage-clients-btn");
const sponsorForm = document.getElementById("sponsor-form");
const clientForm = document.getElementById("client-form");
const sponsorStatus = document.getElementById("sponsor-status-message");
const clientStatus = document.getElementById("client-status-message");
const sponsorList = document.getElementById("sponsor-list");
const clientList = document.getElementById("client-list");
const sponsorRefresh = document.getElementById("sponsor-refresh");
const clientRefresh = document.getElementById("client-refresh");
const sponsorClear = document.getElementById("sponsor-clear");
const clientClear = document.getElementById("client-clear");
const heroSponsorCount = document.getElementById("hero-sponsor-count");
const heroClientCount = document.getElementById("hero-client-count");
const heroDashboardSponsors = document.getElementById("hero-dashboard-sponsors");
const heroDashboardClients = document.getElementById("hero-dashboard-clients");
const heroDashboardDate = document.getElementById("hero-dashboard-date");
const liveClockEl = document.getElementById("live-clock");
const heroRegistrationCount = document.getElementById("hero-dashboard-registrations");
const totalSponsorsEl = document.getElementById("total-sponsors");
const totalClientsEl = document.getElementById("total-clients");
const activeClientsEl = document.getElementById("active-clients");
const prospectSponsorsEl = document.getElementById("prospect-sponsors");
const lastUpdated = document.getElementById("last-updated");
const footerSponsors = document.getElementById("footer-sponsors");
const footerClients = document.getElementById("footer-clients");
const footerActive = document.getElementById("footer-active-clients");
const footerProspects = document.getElementById("footer-prospect-sponsors");
const footerRegistrations = document.getElementById("footer-total-registrations");
const footerDate = document.getElementById("footer-date");
const footerUpdated = document.getElementById("footer-last-updated");
const connectGoogleBtn = document.getElementById("connect-google");
const analyticsSheetId = document.getElementById("analytics-sheet-id");
const fetchSheetBtn = document.getElementById("fetch-sheet");
const exportSheetLink = document.getElementById("export-sheet");
const analyticsTableContainer = document.createElement("div");
analyticsTableContainer.id = "analytics-table-container";
analyticsTableContainer.style.marginTop = "1rem";
analyticsTableContainer.style.overflow = "auto";
analyticsTableContainer.style.maxHeight = "320px";
const openAdminLoginBtn = document.getElementById("open-admin-login");
const openAdminBtn = document.getElementById("open-admin-btn");
const adminSection = document.getElementById("admin");
const adminTotalSponsors = document.getElementById("admin-total-sponsors");
const adminTotalClients = document.getElementById("admin-total-clients");
const adminActiveClients = document.getElementById("admin-active-clients");
const adminProspectSponsors = document.getElementById("admin-prospect-sponsors");
const openAdminSponsorsBtn = document.getElementById("admin-sponsors");
const openAdminClientsBtn = document.getElementById("admin-clients");
const openAdminInsightsBtn = document.getElementById("admin-insights");

const sponsorFields = {
  id: document.getElementById("sponsor-id"),
  name: document.getElementById("sponsor-name"),
  email: document.getElementById("sponsor-email"),
  phone: document.getElementById("sponsor-phone"),
  status: document.getElementById("sponsor-status-select"),
  password: document.getElementById("sponsor-password"),
  notes: document.getElementById("sponsor-notes"),
};
const clientFields = {
  id: document.getElementById("client-id"),
  name: document.getElementById("client-name"),
  email: document.getElementById("client-email"),
  phone: document.getElementById("client-phone"),
  company: document.getElementById("client-company"),
  sponsor: document.getElementById("client-sponsor"),
  status: document.getElementById("client-status-select"),
  password: document.getElementById("client-password"),
  notes: document.getElementById("client-notes"),
};
const openSponsorLoginBtn = document.getElementById("open-sponsor-login");
const openClientLoginBtn = document.getElementById("open-client-login");
const loginModal = document.getElementById("login-modal");
const closeLoginBtn = document.getElementById("close-login");
const closeLoginSecondary = document.getElementById("close-login-secondary");
const loginForm = document.getElementById("login-form");
const loginTitle = document.getElementById("login-title");
const loginDescription = document.getElementById("login-description");
const loginRole = document.getElementById("login-role");
const loginEmail = document.getElementById("login-email");
const loginPassword = document.getElementById("login-password");
const loginStatus = document.getElementById("login-status");
const userWelcome = document.getElementById("user-welcome");
const tabSponsor = document.getElementById("tab-sponsor");
const tabClient = document.getElementById("tab-client");
const tabMarketing = document.getElementById("tab-marketing");
const tabInsights = document.getElementById("tab-insights");
const sponsorPanel = document.getElementById("management");
const clientPanel = document.getElementById("clients");
const marketingPanel = document.getElementById("marketing-window");
const insightsPanel = document.getElementById("insights-window");
const manageMarketingBtn = document.getElementById("manage-marketing-btn");
const viewInsightsBtn = document.getElementById("view-insights-btn");
const contactUsBtn = document.getElementById("contact-us-btn");
const insightSponsorsEl = document.getElementById("insight-sponsors");
const insightClientsEl = document.getElementById("insight-clients");
const insightActiveClientsEl = document.getElementById("insight-active-clients");
const insightProspectSponsorsEl = document.getElementById("insight-prospect-sponsors");
const contactForm = document.getElementById("contact-form");
const contactStatus = document.getElementById("contact-status");
const contactName = document.getElementById("contact-name");
const contactEmailInput = document.getElementById("contact-email");
const contactMessageInput = document.getElementById("contact-message-input");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");
const chatResponse = document.getElementById("chat-response");
const installAppBtn = document.getElementById("install-app-btn");
const sponsorGate = document.getElementById("sponsor-gate");
const clientGate = document.getElementById("client-gate");
const sponsorContent = document.querySelector(".sponsor-content");
const clientContent = document.querySelector(".client-content");
const ctaSponsorsBtn = document.getElementById("cta-sponsors-btn");
const ctaClientsBtn = document.getElementById("cta-clients-btn");
const openRegisterBtn = document.getElementById("open-register-btn");
const sectionSearchInput = document.getElementById("section-search");
const apiBase = "/";

let sponsorsCache = [];
let clientsCache = [];
let summaryCache = null;
let currentUser = null;
let installPromptEvent = null;

function setStatus(el, message, type = "success") {
  if (!el) return;
  el.textContent = message;
  el.style.color = type === "error" ? "#f87171" : "#a3e635";
}

function updateMetrics() {
  const totalRegistrations = sponsorsCache.length + clientsCache.length;
  const now = new Date();
  const currentTime = now.toLocaleTimeString();
  const currentDate = now.toLocaleDateString();

  if (totalSponsorsEl) totalSponsorsEl.textContent = sponsorsCache.length;
  if (totalClientsEl) totalClientsEl.textContent = clientsCache.length;
  if (heroSponsorCount) heroSponsorCount.textContent = sponsorsCache.length;
  if (heroClientCount) heroClientCount.textContent = clientsCache.length;
  if (heroDashboardSponsors) heroDashboardSponsors.textContent = sponsorsCache.length;
  if (heroDashboardClients) heroDashboardClients.textContent = clientsCache.length;
  if (heroRegistrationCount) heroRegistrationCount.textContent = totalRegistrations;
  if (heroDashboardDate) heroDashboardDate.textContent = currentDate;
  if (activeClientsEl) activeClientsEl.textContent = summaryCache?.active_clients ?? 0;
  if (prospectSponsorsEl) prospectSponsorsEl.textContent = summaryCache?.prospect_sponsors ?? 0;
  if (lastUpdated) lastUpdated.textContent = currentTime;

  if (footerSponsors) footerSponsors.textContent = sponsorsCache.length;
  if (footerClients) footerClients.textContent = clientsCache.length;
  if (footerActive) footerActive.textContent = summaryCache?.active_clients ?? 0;
  if (footerProspects) footerProspects.textContent = summaryCache?.prospect_sponsors ?? 0;
  if (footerRegistrations) footerRegistrations.textContent = totalRegistrations;
  if (footerDate) footerDate.textContent = currentDate;
  if (footerUpdated) footerUpdated.textContent = currentTime;

  if (insightSponsorsEl) insightSponsorsEl.textContent = sponsorsCache.length;
  if (insightClientsEl) insightClientsEl.textContent = clientsCache.length;
  if (insightActiveClientsEl) insightActiveClientsEl.textContent = summaryCache?.active_clients ?? 0;
  if (insightProspectSponsorsEl) insightProspectSponsorsEl.textContent = summaryCache?.prospect_sponsors ?? 0;

  if (adminTotalSponsors) adminTotalSponsors.textContent = sponsorsCache.length;
  if (adminTotalClients) adminTotalClients.textContent = clientsCache.length;
  if (adminActiveClients) adminActiveClients.textContent = summaryCache?.active_clients ?? 0;
  if (adminProspectSponsors) adminProspectSponsors.textContent = summaryCache?.prospect_sponsors ?? 0;
}

function updateLiveClock() {
  if (!liveClockEl) return;
  const now = new Date();
  liveClockEl.textContent = now.toLocaleTimeString();
}

async function fetchSummary() {
  try {
    const response = await fetch(`${apiBase}summary`, { headers: getAuthHeaders() });
    summaryCache = await response.json();
    updateMetrics();
  } catch (err) {
    console.warn("Summary load failed", err);
  }
}

function searchSection(term) {
  if (!term) return;
  const normalized = term.trim().toLowerCase();
  const sections = [
    { label: "overview", selector: "#overview" },
    { label: "sponsors", selector: "#management" },
    { label: "clients", selector: "#clients" },
    { label: "marketing", url: "/work" },
    { label: "register", url: "/registration" },
    { label: "about", url: "/about" },
    { label: "media", url: "/media" },
    { label: "team", url: "/about#team" },
    { label: "contact", url: "/contact" },
  ];
  const match = sections.find((section) => section.label.includes(normalized));
  if (match) {
    if (match.url) {
      window.location.href = match.url;
    } else if (match.selector) {
      const el = document.querySelector(match.selector);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }
}

function updateAccessControls() {
  const sponsorLoggedIn = currentUser?.role === "sponsor";
  const clientLoggedIn = currentUser?.role === "client";
  const adminLoggedIn = currentUser?.role === "admin";
  const canUseSponsorTools = sponsorLoggedIn || adminLoggedIn;
  const canUseClientTools = clientLoggedIn || adminLoggedIn;
  if (sponsorGate) sponsorGate.style.display = canUseSponsorTools ? "none" : "block";
  if (clientGate) clientGate.style.display = canUseClientTools ? "none" : "block";
  if (sponsorContent) sponsorContent.style.display = canUseSponsorTools ? "block" : "none";
  if (clientContent) clientContent.style.display = canUseClientTools ? "block" : "none";
  if (adminSection) adminSection.hidden = !adminLoggedIn;
  if (openAdminBtn) openAdminBtn.hidden = !adminLoggedIn;
  if (currentUser) {
    if (adminLoggedIn) {
      if (userWelcome) userWelcome.textContent = `Admin logged in: ${currentUser.name}`;
    } else {
      if (userWelcome) userWelcome.textContent = `Logged in as ${currentUser.role}: ${currentUser.name}`;
    }
  } else {
    if (userWelcome) userWelcome.textContent = "Login as a sponsor, client, or admin to personalize your portal experience.";
  }
}

function saveCurrentUser() {
  try {
    if (currentUser) {
      localStorage.setItem("sponsorPortalCurrentUser", JSON.stringify(currentUser));
    } else {
      localStorage.removeItem("sponsorPortalCurrentUser");
    }
  } catch (err) {
    console.warn("Unable to save user state", err);
  }
}

function loadCurrentUser() {
  try {
    const params = new URLSearchParams(window.location.search);
    const socialToken = params.get('social_token');
    
    if (socialToken) {
      currentUser = {
        role: params.get('role') || 'sponsor',
        name: params.get('name') || 'User',
        token: socialToken
      };
      saveCurrentUser();
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else {
      const stored = localStorage.getItem("sponsorPortalCurrentUser");
      if (stored) {
        currentUser = JSON.parse(stored);
      }
    }
  } catch (err) {
    console.warn("Unable to restore user state", err);
    currentUser = null;
  }
}

function getAuthHeaders(includeJson = false) {
  const headers = {};
  if (includeJson) headers["Content-Type"] = "application/json";
  if (currentUser && currentUser.token) headers["Authorization"] = `Bearer ${currentUser.token}`;
  return headers;
}

function requireRole(role) {
  if (!currentUser || currentUser.role !== role) {
    openLogin(role);
    return false;
  }
  return true;
}

function showWindow(windowType) {
  if (windowType === "sponsor" || windowType === "client") {
    const adminCanAccess = currentUser?.role === "admin";
    if (!adminCanAccess && !requireRole(windowType)) return;
  }

  const windowMap = {
    sponsor: sponsorPanel,
    client: clientPanel,
    marketing: marketingPanel,
    insights: insightsPanel,
  };
  const tabMap = {
    sponsor: tabSponsor,
    client: tabClient,
    marketing: tabMarketing,
    insights: tabInsights,
  };

  Object.values(windowMap).forEach((panel) => panel?.classList.remove("active"));
  Object.values(tabMap).forEach((tab) => tab?.classList.remove("active"));

  const target = windowMap[windowType];
  const activeTab = tabMap[windowType];
  if (target) target.classList.add("active");
  if (activeTab) activeTab.classList.add("active");
  if (target) target.scrollIntoView({ behavior: "smooth" });
}

function switchTab(tab) {
  showWindow(tab);
}

function escapeText(value) {
  return String(value || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function renderSponsors(sponsors) {
  if (!sponsorList) return;
  sponsorList.innerHTML = sponsors
    .map(
      (sponsor) => `
      <tr>
        <td data-label="Name">${escapeText(sponsor.name)}</td>
        <td data-label="Email">${escapeText(sponsor.email)}</td>
        <td data-label="Phone">${escapeText(sponsor.phone || "—")}</td>
        <td data-label="Status">${escapeText(sponsor.status)}</td>
        <td data-label="Actions">
          <button class="action-button" data-icon="✏️" onclick="editSponsor(${sponsor.id})">Edit</button>
          <button class="action-button" data-icon="🗑️" onclick="deleteSponsor(${sponsor.id})">Delete</button>
        </td>
      </tr>
    `,
    )
    .join("");
}

function renderSponsorOptions() {
  if (!clientFields.sponsor) return;
  clientFields.sponsor.innerHTML = [
    `<option value="">Unassigned</option>`,
    ...sponsorsCache.map((sponsor) => `<option value="${sponsor.id}">${escapeText(sponsor.name)}</option>`),
  ].join("");
}

function renderClients(clients) {
  if (!clientList) return;
  clientList.innerHTML = clients
    .map(
      (client) => `
      <tr>
        <td data-label="Name">${escapeText(client.name)}</td>
        <td data-label="Email">${escapeText(client.email)}</td>
        <td data-label="Company">${escapeText(client.company || "—")}</td>
        <td data-label="Assigned Sponsor">${escapeText(client.sponsor_name || "—")}</td>
        <td data-label="Status">${escapeText(client.status)}</td>
        <td data-label="Actions">
          <button class="action-button" data-icon="✏️" onclick="editClient(${client.id})">Edit</button>
          <button class="action-button" data-icon="🗑️" onclick="deleteClient(${client.id})">Delete</button>
        </td>
      </tr>
    `,
    )
    .join("");
}

async function fetchSponsors() {
  try {
    const response = await fetch(`${apiBase}sponsors/`, { headers: getAuthHeaders() });
    sponsorsCache = await response.json();
    renderSponsors(sponsorsCache);
    renderSponsorOptions();
    updateMetrics();
    setStatus(sponsorStatus, `Loaded ${sponsorsCache.length} sponsors.`);
  } catch (err) {
    setStatus(sponsorStatus, "Unable to load sponsors.", "error");
  }
}

async function fetchClients() {
  try {
    const response = await fetch(`${apiBase}clients/`, { headers: getAuthHeaders() });
    clientsCache = await response.json();
    renderClients(clientsCache);
    updateMetrics();
    setStatus(clientStatus, `Loaded ${clientsCache.length} clients.`);
  } catch (err) {
    setStatus(clientStatus, "Unable to load clients.", "error");
  }
}

function openLogin(role) {
  const roleName = role === "admin" ? "Admin" : role === "sponsor" ? "Sponsor" : "Client";
  if (loginRole) loginRole.value = role;
  if (loginEmail) loginEmail.value = "";
  if (loginPassword) loginPassword.value = "";
  if (loginStatus) loginStatus.textContent = "";
  if (loginTitle) loginTitle.textContent = `${roleName} Login`;
  if (loginDescription) loginDescription.textContent = `Use your ${roleName.toLowerCase()} account to access the portal and manage your ${roleName.toLowerCase()} profile.`;
  if (loginModal) loginModal.classList.remove("hidden");
}

function closeLogin() {
  loginModal?.classList.add("hidden");
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeLogin();
});
function updateWelcome() {
  if (currentUser) {
    if (userWelcome) userWelcome.textContent = `Logged in as ${currentUser.role}: ${currentUser.name}`;
  } else {
    if (userWelcome) userWelcome.textContent = "Login as a sponsor or client to personalize your portfolio experience.";
  }
}

async function login(event) {
  event.preventDefault();
  const role = loginRole.value;
  const endpoint = `${apiBase}auth/${role}-login`;
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: loginEmail.value.trim(),
        password: loginPassword.value.trim(),
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Login failed");
    }
    currentUser = { role: payload.role, name: payload.name, token: payload.token };
    saveCurrentUser();
    updateAccessControls();
    setStatus(loginStatus, payload.message);
    closeLogin();
    if (payload.role === "admin") {
      window.location.href = "/admin";
    } else {
      showWindow(payload.role);
    }
  } catch (err) {
    setStatus(loginStatus, err.message, "error");
  }
}

async function submitContact(event) {
  event.preventDefault();
  const name = contactName?.value.trim();
  const email = contactEmailInput?.value.trim();
  const message = contactMessageInput?.value.trim();
  if (!name || !email || !message) {
    setStatus(contactStatus, "Please complete all fields.", "error");
    return;
  }
  try {
    const response = await fetch(`${apiBase}contact/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Unable to send message");
    setStatus(contactStatus, payload.message || "Thanks for your message! We'll reach out soon.");
    contactForm?.reset();
  } catch (err) {
    setStatus(contactStatus, err.message, "error");
  }
}

async function askAssistant() {
  const message = chatInput?.value?.trim();
  if (!message) {
    setStatus(chatResponse, "Please enter a message.", "error");
    return;
  }
  try {
    const response = await fetch(`${apiBase}chat/assistant`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Assistant request failed");
    setStatus(chatResponse, payload.reply || "Thanks for asking.");
  } catch (err) {
    setStatus(chatResponse, err.message, "error");
  }
}

function applySponsorFilter() {
  const query = sponsorSearch.value.trim().toLowerCase();
  const filtered = sponsorsCache.filter((sponsor) => {
    return [sponsor.name, sponsor.email, sponsor.phone, sponsor.status, sponsor.notes]
      .filter(Boolean)
      .some((field) => field.toLowerCase().includes(query));
  });
  renderSponsors(filtered);
}

function applyClientFilter() {
  const query = clientSearch.value.trim().toLowerCase();
  const filtered = clientsCache.filter((client) => {
    return [client.name, client.email, client.company, client.phone, client.status, client.notes]
      .filter(Boolean)
      .some((field) => field.toLowerCase().includes(query));
  });
  renderClients(filtered);
}

async function editSponsor(id) {
  try {
    const response = await fetch(`${apiBase}sponsors/${id}`, { headers: getAuthHeaders() });
    if (!response.ok) throw new Error("Sponsor not found");
    const sponsor = await response.json();
    sponsorFields.id.value = sponsor.id;
    sponsorFields.name.value = sponsor.name;
    sponsorFields.email.value = sponsor.email;
    sponsorFields.phone.value = sponsor.phone || "";
    sponsorFields.status.value = sponsor.status;
    sponsorFields.notes.value = sponsor.notes || "";
    setStatus(sponsorStatus, "Editing sponsor. Save to update.");
    document.getElementById("management").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    setStatus(sponsorStatus, "Unable to load sponsor.", "error");
  }
}

async function editClient(id) {
  try {
    const response = await fetch(`${apiBase}clients/${id}`, { headers: getAuthHeaders() });
    if (!response.ok) throw new Error("Client not found");
    const client = await response.json();
    clientFields.id.value = client.id;
    clientFields.name.value = client.name;
    clientFields.email.value = client.email;
    clientFields.phone.value = client.phone || "";
    clientFields.company.value = client.company || "";
    clientFields.sponsor.value = client.sponsor_id || "";
    clientFields.status.value = client.status;
    clientFields.notes.value = client.notes || "";
    setStatus(clientStatus, "Editing client. Save to update.");
    document.getElementById("clients").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    setStatus(clientStatus, "Unable to load client.", "error");
  }
}

async function deleteSponsor(id) {
  if (!confirm("Delete this sponsor?")) return;
  try {
    const response = await fetch(`${apiBase}sponsors/${id}`, { method: "DELETE", headers: getAuthHeaders() });
    if (!response.ok) throw new Error("Delete failed");
    setStatus(sponsorStatus, "Sponsor deleted.");
    await fetchSponsors();
    applySponsorFilter();
  } catch (err) {
    setStatus(sponsorStatus, "Unable to delete sponsor.", "error");
  }
}

async function deleteClient(id) {
  if (!confirm("Delete this client?")) return;
  try {
    const response = await fetch(`${apiBase}clients/${id}`, { method: "DELETE", headers: getAuthHeaders() });
    if (!response.ok) throw new Error("Delete failed");
    setStatus(clientStatus, "Client deleted.");
    await fetchClients();
    applyClientFilter();
  } catch (err) {
    setStatus(clientStatus, "Unable to delete client.", "error");
  }
}

async function submitSponsor(event) {
  event.preventDefault();
  const payload = {
    name: sponsorFields.name.value.trim(),
    email: sponsorFields.email.value.trim(),
    phone: sponsorFields.phone.value.trim() || null,
    status: sponsorFields.status.value,
    notes: sponsorFields.notes.value.trim() || null,
  };
  const sponsorPassword = sponsorFields.password.value.trim();
  if (sponsorPassword) {
    payload.password = sponsorPassword;
  }
  const id = sponsorFields.id.value;
  const url = id ? `${apiBase}sponsors/${id}` : `${apiBase}sponsors/`;
  const method = id ? "PUT" : "POST";
  try {
    const response = await fetch(url, {
      method,
      headers: getAuthHeaders(true),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.detail || "Request failed");
    }
    setStatus(sponsorStatus, `Sponsor ${id ? "updated" : "created"} successfully.`);
    clearSponsorForm();
    await fetchSponsors();
    applySponsorFilter();
  } catch (err) {
    setStatus(sponsorStatus, err.message, "error");
  }
}

async function submitClient(event) {
  event.preventDefault();
  const sponsorIdValue = clientFields.sponsor.value;
  const payload = {
    name: clientFields.name.value.trim(),
    email: clientFields.email.value.trim(),
    phone: clientFields.phone.value.trim() || null,
    company: clientFields.company.value.trim() || null,
    sponsor_id: sponsorIdValue ? Number(sponsorIdValue) : null,
    status: clientFields.status.value,
    notes: clientFields.notes.value.trim() || null,
  };
  const clientPassword = clientFields.password.value.trim();
  if (clientPassword) {
    payload.password = clientPassword;
  }
  const id = clientFields.id.value;
  const url = id ? `${apiBase}clients/${id}` : `${apiBase}clients/`;
  const method = id ? "PUT" : "POST";
  try {
    const response = await fetch(url, {
      method,
      headers: getAuthHeaders(true),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.detail || "Request failed");
    }
    setStatus(clientStatus, `Client ${id ? "updated" : "created"} successfully.`);
    clearClientForm();
    await fetchClients();
    applyClientFilter();
  } catch (err) {
    setStatus(clientStatus, err.message, "error");
  }
}

function clearSponsorForm() {
  sponsorFields.id.value = "";
  sponsorFields.name.value = "";
  sponsorFields.email.value = "";
  sponsorFields.phone.value = "";
  sponsorFields.status.value = "prospect";
  sponsorFields.password.value = "";
  sponsorFields.notes.value = "";
}

function clearClientForm() {
  clientFields.id.value = "";
  clientFields.name.value = "";
  clientFields.email.value = "";
  clientFields.phone.value = "";
  clientFields.company.value = "";
  clientFields.sponsor.value = "";
  clientFields.status.value = "active";
  clientFields.password.value = "";
  clientFields.notes.value = "";
}

function clearRegisterSponsorForm() {
  const form = document.getElementById("register-sponsor-form");
  if (form) form.reset();
  const status = document.getElementById("register-sponsor-feedback");
  if (status) status.textContent = "";
}

function clearRegisterClientForm() {
  const form = document.getElementById("register-client-form");
  if (form) form.reset();
  const status = document.getElementById("register-client-feedback");
  if (status) status.textContent = "";
}

async function submitRegisterSponsor(event) {
  event.preventDefault();
  const statusEl = document.getElementById("register-sponsor-feedback");
  const payload = {
    name: document.getElementById("register-sponsor-name").value.trim(),
    email: document.getElementById("register-sponsor-email").value.trim(),
    phone: document.getElementById("register-sponsor-phone").value.trim(),
    status: document.getElementById("register-sponsor-status").value,
    password: document.getElementById("register-sponsor-password").value.trim(),
    notes: document.getElementById("register-sponsor-notes").value.trim(),
  };
  try {
    const response = await fetch(`${apiBase}sponsors/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.detail || "Registration failed");
    }
    clearRegisterSponsorForm();
    if (statusEl) setStatus(statusEl, "Sponsor account registered successfully.");
    await fetchSponsors();
  } catch (err) {
    if (statusEl) setStatus(statusEl, err.message, "error");
  }
}

async function submitRegisterClient(event) {
  event.preventDefault();
  const statusEl = document.getElementById("register-client-feedback");
  const payload = {
    name: document.getElementById("register-client-name").value.trim(),
    email: document.getElementById("register-client-email").value.trim(),
    company: document.getElementById("register-client-company").value.trim(),
    phone: document.getElementById("register-client-phone").value.trim(),
    status: document.getElementById("register-client-status").value,
    password: document.getElementById("register-client-password").value.trim(),
    notes: document.getElementById("register-client-notes").value.trim(),
  };
  try {
    const response = await fetch(`${apiBase}clients/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.detail || "Registration failed");
    }
    clearRegisterClientForm();
    if (statusEl) setStatus(statusEl, "Client account registered successfully.");
    await fetchClients();
  } catch (err) {
    if (statusEl) setStatus(statusEl, err.message, "error");
  }
}

manageSponsorsBtn?.addEventListener("click", () => showWindow("sponsor"));
manageClientsBtn?.addEventListener("click", () => showWindow("client"));
manageMarketingBtn?.addEventListener("click", () => {
  showWindow("marketing");
  document.querySelector(".management-window")?.scrollIntoView({ behavior: "smooth" });
});
viewInsightsBtn?.addEventListener("click", () => {
  showWindow("insights");
  document.querySelector(".management-window")?.scrollIntoView({ behavior: "smooth" });
});
// Registration logic is now handled via href="/registration"
ctaSponsorsBtn?.addEventListener("click", () => {
  showWindow("sponsor");
  document.querySelector(".management-window")?.scrollIntoView({ behavior: "smooth" });
});
ctaClientsBtn?.addEventListener("click", () => {
  showWindow("client");
  document.querySelector(".management-window")?.scrollIntoView({ behavior: "smooth" });
});
openSponsorLoginBtn?.addEventListener("click", () => openLogin("sponsor"));
openClientLoginBtn?.addEventListener("click", () => openLogin("client"));
openAdminLoginBtn?.addEventListener("click", () => openLogin("admin"));
openAdminBtn?.addEventListener("click", () => {
  window.location.href = "/admin";
});
openAdminSponsorsBtn?.addEventListener("click", () => showWindow("sponsor"));
openAdminClientsBtn?.addEventListener("click", () => showWindow("client"));
openAdminInsightsBtn?.addEventListener("click", () => showWindow("insights"));
closeLoginBtn?.addEventListener("click", closeLogin);
closeLoginSecondary?.addEventListener("click", closeLogin);
loginModal?.addEventListener("click", (event) => {
  if (event.target === loginModal) closeLogin();
});
// Contact logic is now handled via href="/contact"
contactForm?.addEventListener("submit", submitContact);
chatSend?.addEventListener("click", askAssistant);
chatInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    askAssistant();
  }
});

sectionSearchInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    searchSection(sectionSearchInput.value);
  }
});

if (tabSponsor) tabSponsor.addEventListener("click", () => showWindow("sponsor"));
if (tabClient) tabClient.addEventListener("click", () => showWindow("client"));
if (tabMarketing) tabMarketing.addEventListener("click", () => showWindow("marketing"));
if (tabInsights) tabInsights.addEventListener("click", () => showWindow("insights"));

const navLinks = document.querySelectorAll(".site-nav a");
navLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    const href = link.getAttribute("href");
    if (href === "#management" || href === "#clients") {
      event.preventDefault();
      showWindow(href === "#management" ? "sponsor" : "client");
    }
  });
});

const adminNavLinks = document.querySelectorAll(".admin-nav a");
function updateAdminNavActiveLink() {
  const currentHash = window.location.hash || "#admin-summary";
  adminNavLinks.forEach((link) => {
    if (link.getAttribute("href") === currentHash) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
}
if (adminNavLinks.length) {
  adminNavLinks.forEach((link) => {
    link.addEventListener("click", () => {
      adminNavLinks.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
  window.addEventListener("hashchange", updateAdminNavActiveLink);
  updateAdminNavActiveLink();
}

// Team carousel controls (responsive)
document.addEventListener("DOMContentLoaded", () => {
  const teamCarousel = document.querySelector(".team-carousel");
  if (!teamCarousel) return;
  const container = teamCarousel.querySelector(".team-grid");
  const prev = teamCarousel.querySelector(".team-prev");
  const next = teamCarousel.querySelector(".team-next");
  const scrollAmount = () => Math.min(container.clientWidth * 0.8, 900);
  prev.addEventListener("click", () => container.scrollBy({ left: -scrollAmount(), behavior: "smooth" }));
  next.addEventListener("click", () => container.scrollBy({ left: scrollAmount(), behavior: "smooth" }));
  // enable keyboard navigation
  prev.addEventListener("keyup", (e) => { if (e.key === "Enter") prev.click(); });
  next.addEventListener("keyup", (e) => { if (e.key === "Enter") next.click(); });

  document.querySelectorAll(".attachment-upload").forEach((attachmentUpload) => {
    const attachmentFileList = attachmentUpload
      .closest(".upload-box")
      ?.querySelector(".attachment-file-list");
    if (!attachmentFileList) return;

    attachmentUpload.addEventListener("change", () => {
      const files = Array.from(attachmentUpload.files || []);
      if (!files.length) {
        attachmentFileList.textContent = "No files selected.";
        return;
      }

      attachmentFileList.innerHTML = files
        .map(file => `<div>${file.name} (${Math.round(file.size / 1024)} KB)</div>`)
        .join("");
    });
  });
});

async function fetchSheetAndDisplay() {
  const sheetId = analyticsSheetId?.value?.trim();
  if (!sheetId) {
    alert("Please enter a Google Sheet ID.");
    return;
  }
  try {
    const resp = await fetch(`${apiBase}google/sheets/${encodeURIComponent(sheetId)}?range=A1:Z500`);
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(err.detail || "Unable to fetch sheet");
    }
    const payload = await resp.json();
    const values = payload.values || [];

    // Build table
    analyticsTableContainer.innerHTML = "";
    if (values.length === 0) {
      analyticsTableContainer.textContent = "No data in sheet.";
    } else {
      const table = document.createElement("table");
      table.style.width = '100%';
      table.style.borderCollapse = 'collapse';
      const thead = document.createElement("thead");
      const tbody = document.createElement("tbody");
      const headerRow = document.createElement("tr");
      values[0].forEach(h => {
        const th = document.createElement("th");
        th.textContent = h;
        th.style.textAlign = 'left';
        th.style.padding = '6px 8px';
        th.style.color = 'var(--muted)';
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      for (let r = 1; r < values.length; r++) {
        const row = document.createElement("tr");
        values[r].forEach(c => {
          const td = document.createElement("td");
          td.textContent = c || "";
          td.style.padding = '6px 8px';
          td.style.borderTop = '1px solid rgba(255,255,255,0.04)';
          row.appendChild(td);
        });
        tbody.appendChild(row);
      }
      table.appendChild(thead);
      table.appendChild(tbody);
      analyticsTableContainer.appendChild(table);

      // Infer simple metrics
      const headers = values[0].map(h => (h || "").toString().toLowerCase());
      const sponsorIdx = headers.findIndex(h => h.includes('sponsor'));
      const clientIdx = headers.findIndex(h => h.includes('client'));
      let sponsorsCount = 0;
      let clientsCount = 0;
      if (sponsorIdx >= 0) {
        const set = new Set();
        for (let i = 1; i < values.length; i++) if (values[i][sponsorIdx]) set.add(values[i][sponsorIdx]);
        sponsorsCount = set.size;
      }
      if (clientIdx >= 0) {
        const set = new Set();
        for (let i = 1; i < values.length; i++) if (values[i][clientIdx]) set.add(values[i][clientIdx]);
        clientsCount = set.size;
      }
      const totalRegs = Math.max(0, values.length - 1);
      if (!sponsorsCount) sponsorsCount = totalRegs;
      if (!clientsCount) clientsCount = 0;

      if (heroDashboardSponsors) heroDashboardSponsors.textContent = sponsorsCount;
      if (heroDashboardClients) heroDashboardClients.textContent = clientsCount;
      if (heroRegistrationCount) heroRegistrationCount.textContent = totalRegs;
      if (footerSponsors) footerSponsors.textContent = sponsorsCount;
      if (footerClients) footerClients.textContent = clientsCount;
      if (footerRegistrations) footerRegistrations.textContent = totalRegs;

      // wire export link
      if (exportSheetLink) {
        exportSheetLink.href = `${apiBase}google/sheets/${encodeURIComponent(sheetId)}/export.xlsx`;
        exportSheetLink.setAttribute('download', `sheet_${sheetId}.xlsx`);
      }
    }

    // attach container into live analytics area
    const liveArea = document.querySelector('#live-analytics .hero-dashboard');
    if (liveArea && !liveArea.contains(analyticsTableContainer)) liveArea.appendChild(analyticsTableContainer);
  } catch (err) {
    alert(err.message || 'Failed to load sheet');
  }
}

connectGoogleBtn?.addEventListener('click', () => {
  // open OAuth flow in a new window/tab
  window.open(`${apiBase}google/login`, '_blank');
});

fetchSheetBtn?.addEventListener('click', fetchSheetAndDisplay);

if (sponsorSearch) sponsorSearch.addEventListener("input", applySponsorFilter);
if (clientSearch) clientSearch.addEventListener("input", applyClientFilter);
sponsorForm?.addEventListener("submit", submitSponsor);
clientForm?.addEventListener("submit", submitClient);
document.getElementById("register-sponsor-form")?.addEventListener("submit", submitRegisterSponsor);
document.getElementById("register-client-form")?.addEventListener("submit", submitRegisterClient);
document.getElementById("register-sponsor-clear")?.addEventListener("click", clearRegisterSponsorForm);
document.getElementById("register-client-clear")?.addEventListener("click", clearRegisterClientForm);
loginForm?.addEventListener("submit", login);
sponsorRefresh?.addEventListener("click", fetchSponsors);
clientRefresh?.addEventListener("click", fetchClients);
sponsorClear?.addEventListener("click", () => {
  clearSponsorForm();
  setStatus(sponsorStatus, "Sponsor form cleared.");
});
clientClear?.addEventListener("click", () => {
  clearClientForm();
  setStatus(clientStatus, "Client form cleared.");
});

window.addEventListener("load", async () => {
  loadCurrentUser();
  registerServiceWorker();
  if (sponsorList || sponsorForm) await fetchSponsors();
  if (clientList || clientForm) await fetchClients();
  await fetchSummary();
  updateAccessControls();
  updateLiveClock();
  setInterval(updateLiveClock, 1000);

  setupBottomNavigation();
  setupMarketingWorkflowUI();
});


function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("/static/sw.js")
      .then(() => console.log("Service worker registered."))
      .catch((error) => console.warn("Service worker registration failed:", error));
  }
}

function setupMarketingWorkflowUI() {
  const campaignForm = document.getElementById("campaign-form");
  const listEl = document.getElementById("marketing-campaign-list");

  // We render the list only if present.
  // If listEl doesn't exist yet, we still update counters & allow adding campaigns.

  // Dynamic counters for the marketing window.
  const counterActive = document.getElementById("m-active-campaigns");
  const counterContent = document.getElementById("m-content-pieces");
  const counterInfluencer = document.getElementById("m-influencer-actions");

  let campaigns = [];
  try {
    // marketing_data.js uses ES modules export, but we are not importing it.
    // So we use a graceful fallback: keep empty campaigns unless you wire modules later.
    // For now we seed with DOM defaults.
  } catch (e) {
    // ignore
  }

  const recalcCounters = () => {
    const active = campaigns.filter((c) => c.status === "active").length;
    // Simple placeholders: content pieces and influencer actions derived from campaigns count.
    const contentPieces = campaigns.length * 7;
    const influencerActions = campaigns.length * 3;

    // Make sure counters exist and never render undefined.
    if (counterActive) counterActive.textContent = String(active);
    if (counterContent) counterContent.textContent = String(contentPieces);
    if (counterInfluencer) counterInfluencer.textContent = String(influencerActions);
  };

  const renderCampaignList = () => {
    if (!listEl) return;
    if (!campaigns.length) {
      listEl.innerHTML = `<div class="status-message" style="color:var(--muted)">No campaigns yet. Add one above.</div>`;
      return;
    }

    listEl.innerHTML = campaigns
      .map(
        (c) =>
          `<div class="campaign-row" data-campaign-id="${c.id}" style="display:flex;justify-content:space-between;gap:0.75rem;padding:0.85rem 0;border-bottom:1px solid rgba(148,163,184,0.12)">
            <div>
              <div style="font-weight:800">${escapeText(c.name)}</div>
              <div style="color:var(--muted);font-size:0.9rem">${escapeText(c.channel)} • ${escapeText(c.status)}</div>
              <div style="color:var(--muted-soft);font-size:0.9rem">Next: ${escapeText(c.nextStep)}</div>
            </div>
            <div style="white-space:nowrap;color:var(--muted-soft);font-weight:700">#${c.id}</div>
          </div>`
      )
      .join("");
  };

  campaignForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    const nameEl = document.getElementById("campaign-name");
    const channelEl = document.getElementById("campaign-channel");
    const statusEl = document.getElementById("campaign-status");
    const nextStepEl = document.getElementById("campaign-next-step");

    const name = nameEl?.value?.trim();
    const channel = channelEl?.value?.trim();
    const status = statusEl?.value;
    const nextStep = nextStepEl?.value?.trim();

    if (!name || !channel || !status || !nextStep) return;

    const nextId = campaigns.length ? Math.max(...campaigns.map((x) => x.id)) + 1 : 1;
    campaigns.push({ id: nextId, name, channel, status, nextStep });

    // reset
    campaignForm.reset();

    renderCampaignList();
    recalcCounters();
  });

  // Initial counters
  recalcCounters();
  renderCampaignList();
}


window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  installPromptEvent = event;
  if (installAppBtn) installAppBtn.hidden = false;
});

window.addEventListener("appinstalled", () => {
  installPromptEvent = null;
  if (installAppBtn) installAppBtn.hidden = true;
  console.log("App installed successfully.");
});

installAppBtn?.addEventListener("click", async () => {
  if (!installPromptEvent) return;
  installPromptEvent.prompt();
  const choiceResult = await installPromptEvent.userChoice;
  if (choiceResult.outcome === "accepted") {
    installAppBtn.hidden = true;
  }
  installPromptEvent = null;
});

window.editSponsor = editSponsor;
window.deleteSponsor = deleteSponsor;
window.editClient = editClient;
window.deleteClient = deleteClient;
window.submitRegisterSponsor = submitRegisterSponsor;
window.submitRegisterClient = submitRegisterClient;
window.clearRegisterSponsorForm = clearRegisterSponsorForm;
window.clearRegisterClientForm = clearRegisterClientForm;
