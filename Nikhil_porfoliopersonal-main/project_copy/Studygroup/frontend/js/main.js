// DOM Elements
const createRoomBtn = document.querySelector('.btn-primary');
const chatInput = document.querySelector('.chat-input input');
const sendBtn = document.querySelector('.btn-send');
const chatMessages = document.querySelector('.chat-messages');
const roomGrid = document.querySelector('.room-grid');

// Sample study rooms data (will be replaced with backend data)
const sampleRooms = [
    {
        id: 1,
        name: 'Calculus Study Group',
        participants: 4,
        topic: 'Differential Equations',
        host: 'John Doe'
    },
    {
        id: 2,
        name: 'Physics Lab Discussion',
        participants: 3,
        topic: 'Quantum Mechanics',
        host: 'Jane Smith'
    }
];

// Initialize WebRTC (placeholder for video chat functionality)
function initWebRTC() {
    // WebRTC implementation will go here
    console.log('WebRTC initialized');
}

// Create a new study room
function createStudyRoom() {
    // This will be implemented with backend integration
    console.log('Creating new study room...');
    // Show modal or redirect to room creation page
}

// Join an existing study room
function joinStudyRoom(roomId) {
    // This will be implemented with backend integration
    console.log(`Joining room ${roomId}...`);
    // Redirect to room page
}

// Display study rooms in the grid
function displayStudyRooms() {
    roomGrid.innerHTML = sampleRooms.map(room => `
        <div class="room-card" onclick="joinStudyRoom(${room.id})">
            <h3>${room.name}</h3>
            <p>Topic: ${room.topic}</p>
            <p>Host: ${room.host}</p>
            <p>Participants: ${room.participants}</p>
            <button class="btn btn-primary">Join Room</button>
        </div>
    `).join('');
}

// Handle AI chat messages
function handleChatMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = `
        <div class="message-content">
            <p>${message}</p>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message to AI tutor
function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        handleChatMessage(message);
        // Here we'll add the API call to the AI backend
        chatInput.value = '';
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    displayStudyRooms();
    initWebRTC();
});

createRoomBtn.addEventListener('click', createStudyRoom);
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Authentication functions (to be implemented)
function login() {
    // Login implementation
    console.log('Login clicked');
}

function signup() {
    // Signup implementation
    console.log('Signup clicked');
}

// Add event listeners for auth buttons
document.querySelector('.btn-login').addEventListener('click', login);
document.querySelector('.btn-signup').addEventListener('click', signup);

// Whiteboard functionality (placeholder)
function initWhiteboard() {
    // Whiteboard implementation will go here
    console.log('Whiteboard initialized');
}

// Screen sharing functionality (placeholder)
function initScreenSharing() {
    // Screen sharing implementation will go here
    console.log('Screen sharing initialized');
}

// Export functions for use in other modules
window.studySync = {
    createStudyRoom,
    joinStudyRoom,
    sendMessage,
    initWebRTC,
    initWhiteboard,
    initScreenSharing
}; 