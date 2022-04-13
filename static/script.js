const serverPath = '/output/data';
const btn = document.querySelector('.btn');
const content = document.querySelector('.content');
console.log('skrypt działa');

btn.addEventListener('click', () => {
  console.log('naciśnięto button');
  fetch(serverPath, {
    method: 'POST'
  }).then(response => response.text()).then(data => {
    console.log(data);
    content.textContent = data;
  }).catch(error => {
    console.log('error occured');
  });