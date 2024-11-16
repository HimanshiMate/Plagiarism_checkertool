//=======================home page=====================
// document.querySelector('.btn-hero').addEventListener('click', function() {
//     alert("You clicked the Buy Credits button!");
// });

//===========registration page js=============================
// document.getElementById('registrationForm').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const username = document.getElementById('username').value;
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const confirmPassword = document.getElementById('confirmPassword').value;
//     const errorMessage = document.getElementById('errorMessage');

//     errorMessage.textContent = '';

//     // Basic validation
//     if (password !== confirmPassword) {
//         errorMessage.textContent = 'Passwords do not match.';
//         return;
//     }

//     // Here you can add further validation or send the form data to a server
//     alert(`Registration successful for ${username}!`);
//     document.getElementById('registrationForm').reset();
// });

// =======================login page==========
// document.getElementById('loginForm').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const errorMessage = document.getElementById('errorMessage');

//     errorMessage.textContent = '';

//     // Basic validation
//     if (email === '' || password === '') {
//         errorMessage.textContent = 'Please fill out all fields.';
//         return;
//     }

//     // Further validation or server-side authentication
//     if (email === 'test@example.com' && password === 'password123') {
//         alert('Login successful!');
//     } else {
//         errorMessage.textContent = 'Invalid email or password.';
//     }
// });

// ==================footer section===============
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  


