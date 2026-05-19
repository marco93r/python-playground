const API = 'http://127.0.0.1:8000';

// --- Tab Switch ---
function switchTab(tab) {
    document.getElementById('login-form').style.display = tab === 'login' ? 'flex' : 'none';
    document.getElementById('register-form').style.display = tab === 'register' ? 'flex' : 'none';
    document.querySelectorAll('.tab').forEach((t, i) => {
        t.classList.toggle('active', (i === 0 && tab === 'login') || (i === 1 && tab === 'register'));
    });
}

// --- Auth Helpers ---
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function logout() {
    localStorage.removeItem('token');
    document.getElementById('books-section').style.display = 'none';
    document.getElementById('auth-section').style.display = 'block';
}

// --- On Load ---
window.onload = () => {
    if (getToken()) {
        showBooks();
    }
};

// --- Register ---
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const msg = document.getElementById('register-message');

    const res = await fetch(`${API}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (res.ok) {
        msg.textContent = 'Registered! You can now login.';
        msg.className = 'message success';
    } else {
        const data = await res.json();
        msg.textContent = data.detail || 'Error';
        msg.className = 'message';
    }
});

// --- Login ---
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const msg = document.getElementById('login-message');

    const res = await fetch(`${API}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        showBooks();
    } else {
        msg.textContent = 'Invalid credentials';
        msg.className = 'message';
    }
});

// --- Show Books Section ---
function showBooks() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('books-section').style.display = 'block';
    loadBooks();
}

// --- Load Books ---
async function loadBooks() {
    const res = await fetch(`${API}/books`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });

    if (res.status === 401) {
        logout();
        return;
    }

    const books = await res.json();
    const list = document.getElementById('book-list');
    list.innerHTML = '';

    books.forEach(book => {
        const li = document.createElement('li');
        li.className = 'book-item';
        li.innerHTML = `
            <div class="book-info">
                <strong>${book.title}</strong>
                <span>${book.author}</span>
            </div>
            <button class="delete-btn" onclick="deleteBook(${book.id})">🗑️</button>
        `;
        list.appendChild(li);
    });
}

// --- Add Book ---
document.getElementById('add-book-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const msg = document.getElementById('book-message');

    const res = await fetch(`${API}/books`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, author })
    });

    if (res.ok) {
        document.getElementById('book-title').value = '';
        document.getElementById('book-author').value = '';
        msg.textContent = 'Book added!';
        msg.className = 'message success';
        loadBooks();
        setTimeout(() => msg.textContent = '', 2000);
    } else {
        msg.textContent = 'Error adding book';
        msg.className = 'message';
    }
});

// --- Delete Book ---
async function deleteBook(id) {
    const res = await fetch(`${API}/books/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });

    if (res.ok) {
        loadBooks();
    }
}
