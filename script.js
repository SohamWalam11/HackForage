// Login functionality
let isLoggedIn = false;
let username = '';

// Create the login modal and add it to the DOM
const loginModalHTML = `
  <div class="login-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.7); display: flex; justify-content: center; align-items: center; z-index: 1000;">
    <div style="background: #fff; padding: 25px; border-radius: 8px; width: 300px; text-align: center; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
      <h2>Login</h2>
      <input type="text" id="username" placeholder="Enter your name" style="padding: 12px; width: 100%; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ddd;">
      <button id="login-btn" style="padding: 12px; width: 100%; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Login</button>
      <p style="margin-top: 10px;">Please enter your username to continue.</p>
    </div>
  </div>
`;

document.body.insertAdjacentHTML('beforeend', loginModalHTML);

// Function to handle login
const loginBtn = document.getElementById('login-btn');
loginBtn.addEventListener('click', () => {
  const enteredUsername = document.getElementById('username').value.trim();
  if (enteredUsername) {
    username = enteredUsername;
    isLoggedIn = true;
    document.querySelector('.login-modal').remove(); // Remove login modal after successful login
    alert(`Welcome, ${username}!`);
    showNavLinks();
  } else {
    alert('Please enter a valid username.');
  }
});

// Function to show navigation links after login
function showNavLinks() {
  // Add class or functionality to show nav links if needed
  const navLinks = document.querySelectorAll('.navbar a');
  navLinks.forEach(link => {
    link.style.pointerEvents = 'auto';  // Enable navigation links
    link.style.opacity = '1';  // Make links visible
  });
}

// Smooth scroll for nav links, but only if the user is logged in
document.querySelectorAll('.navbar a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();

    // If the user is not logged in, show the login modal
    if (!isLoggedIn) {
      alert('Please log in to access this feature.');
      return;
    }

    // Scroll to section after login
    const section = document.querySelector(link.getAttribute('href'));
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// JavaScript to handle page switching logic
function switchPage(page) {
  const iframe = document.getElementById('streamlitFrame');
  let url = "http://localhost:8501/";

  // Dynamically set the iframe src based on the page
  if (page === 'home') {
    url += "?page=home";
  } else if (page === 'tracker') {
    url += "?page=tracker";
  } else if (page === 'about') {
    url += "?page=about";
  }
  iframe.src = url; // Update iframe URL
}
