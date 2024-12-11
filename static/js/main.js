document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('image-input');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    
    if (!fileInput.files[0]) {
        alert('Please select an image');
        return;
    }
    
    formData.append('file', fileInput.files[0]);
    
    try {
        // When upload starts
        loadingDiv.style.display = 'block';
        resultDiv.style.display = 'none';
        
        // Send to server
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        // Check the response
        if (!response.ok) {
            throw new Error('Server error: ' + response.status);
        }

        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Show results
        document.getElementById('preview').src = data.image_path;
        document.getElementById('prediction').textContent = data.class;
        document.getElementById('confidence').textContent = 
         `Trust: ${(data.confidence * 100).toFixed(2)}%`; // Added "Trust:" expression
        
        // Fetch information from Wikipedia
        try {
            const wikiResponse = await fetch("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=" + encodeURIComponent(data.class) + "&format=json&origin=*");
            const wikiData = await wikiResponse.json();
        
            // Check the response
            console.log('Wiki Data:', wikiData);
            if (!wikiData.query || !wikiData.query.pages) {
                throw new Error("Response is in an unexpected format.");
            }
        
            // Show Wikipedia information
            const wikiInfoDiv = document.getElementById('wiki-info');
            const pages = wikiData.query.pages;
        
            // Check if the page was not found
            if (pages[-1]) {
                console.log(`The searched title: ${data.class} was not found on Wikipedia.`);
                wikiInfoDiv.innerHTML = `<p>No information found about this fruit.</p>`;
            } else {
                const page = Object.values(pages)[0]; // Get the first page
                console.log('Page:', page);
        
                if (page.extract) {
                    wikiInfoDiv.innerHTML = `
                        <h3>${page.title}</h3>
                        <p>${page.extract}</p>
                        <a href="https://en.wikipedia.org/wiki/${encodeURIComponent(page.title)}" target="_blank">Click here for more information</a>
                    `;
                } else {
                    wikiInfoDiv.innerHTML = `<p>No information found about this fruit.</p>`;
                }
            }
            // Make the wiki-info div visible
            wikiInfoDiv.style.display = 'block';
        } catch (error) {
            console.error('Wikipedia Error:', error);
            alert('An error occurred while fetching Wikipedia information: ' + error.message);
        }
        
        // Make the result div visible
        resultDiv.style.display = 'block';
        
    } catch (error) {
        console.error('General Error:', error);
        alert('An error occurred: ' + error.message);
    } finally {
        loadingDiv.style.display = 'none';
    }
});
