  const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
  const wsUrl = `${wsScheme}${window.location.host}/ws/poll/${pollCode}/`;

  const ws = new WebSocket(wsUrl);

  ws.onmessage = function(event) {// maybe change this later to have number of students joined instead of showing a list of students
    console.log("Received message:", event.data);
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
      const studentsList = document.getElementById('students-list');
      const newStudent = document.createElement('li');
      newStudent.textContent = data.message;
      studentsList.appendChild(newStudent);
    }
  };