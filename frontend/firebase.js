// Import Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Your Firebase config
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Login function
document.getElementById('loginButton').addEventListener('click', async () => {
  try {
    await signInWithPopup(auth, provider);
    console.log("Logged in");
  } catch (error) {
    console.error(error.message);
  }
});

// Logout function
document.getElementById('logoutButton').addEventListener('click', async () => {
  try {
    await signOut(auth);
    console.log("Logged out");
  } catch (error) {
    console.error(error.message);
  }
});
