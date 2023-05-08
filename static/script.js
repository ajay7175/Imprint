// Get input file element and result container element
const inputFile = document.getElementById('input-file');
const resultContainer = document.getElementById('result-container');

// Listen for change event on input file element
inputFile.addEventListener('change', () => {
  // Get file object from input file element
  const file = inputFile.files[0];

  // Create a FormData object and append file to it
  const formData = new FormData();
  formData.append('file', file);

  // Send AJAX request to server to upload file
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Display the output image in the result container
    resultContainer.innerHTML = `
      <h2>Result</h2>
      <img src="${data.result_image}" alt="result">
      <p><a href="${data.result_image}" download>Download</a></p>
    `;
  })
  .catch(error => console.error(error));
});
