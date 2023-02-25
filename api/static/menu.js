window.onload = () => {
    fetch('http://localhost:3000/user_info')
    .then((response) => response.json())
    .then((data) => {
        if (data.data['username']) {
            document.getElementById('ENTRY_USER').innerHTML = data.data['username']
        } else {
            document.getElementById('ENTRY_USER').innerHTML = 'not logged in'
        }

    })    
} 
