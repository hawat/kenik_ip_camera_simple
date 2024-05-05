fetch('/getcameras')
  .then(response => response.json())
  .then(imageData => {
    const imageContainer = document.getElementById('image-container');
    imageData.forEach(imageUrl => {
      const image = document.createElement('img');
      image.src = imageUrl;
      imageContainer.appendChild(image);
    });
  })
  .catch(error => console.error('Error fetching images:', error));
