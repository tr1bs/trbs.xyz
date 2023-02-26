// const ethereumButton = document.querySelector('.enableEthereumButton');
// const showAccount = document.querySelector('.showAccount');

// ethereumButton.addEventListener('click', () => {
//   getAccount();
// });

// async function getAccount() {
//   const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
//   const account = accounts[0];
//   showAccount.innerHTML = account;
// }

window.onload = () => {
    fetch('http://localhost:3000/api/v1/user_info')
    .then((response) => response.json())
    .then((data) => {
        if (data.data['username']) {
            document.getElementById('ENTRY_USER').innerHTML = data.data['username']
        } else {
            document.getElementById('ENTRY_USER').innerHTML = 'not logged in'
        }

    })
} 
