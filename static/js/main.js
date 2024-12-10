document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('image-input');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    
    if (!fileInput.files[0]) {
        alert('Lütfen bir görüntü seçin');
        return;
    }
    
    formData.append('file', fileInput.files[0]);
    
    try {
        // Yükleme başladığında
        loadingDiv.style.display = 'block';
        resultDiv.style.display = 'none';
        
        // Sunucuya gönder
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        // Yanıtı kontrol et
        if (!response.ok) {
            throw new Error('Sunucu hatası: ' + response.status);
        }

        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Sonuçları göster
        document.getElementById('preview').src = data.image_path;
        document.getElementById('prediction').textContent = data.class;
        document.getElementById('confidence').textContent = 
         `Trust: ${(data.confidence * 100).toFixed(2)}%`; // "Trust:" ifadesini ekledik
        
        // Wikipedia'dan bilgi çek
        try {
            const wikiResponse = await fetch("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=" + encodeURIComponent(data.class) + "&format=json&origin=*");
            const wikiData = await wikiResponse.json();
        
            // Yanıtı kontrol et
            console.log('Wiki Data:', wikiData);
            if (!wikiData.query || !wikiData.query.pages) {
                throw new Error("Yanıt beklenmedik bir formatta.");
            }
        
            // Wikipedia bilgilerini göster
            const wikiInfoDiv = document.getElementById('wiki-info');
            const pages = wikiData.query.pages;
        
            // Sayfa bulunamadı kontrolü
            if (pages[-1]) {
                console.log(`Aranan başlık: ${data.class} Wikipedia'da bulunamadı.`);
                wikiInfoDiv.innerHTML = `<p>Bu meyve hakkında bilgi bulunamadı.</p>`;
            } else {
                const page = Object.values(pages)[0]; // İlk sayfayı al
                console.log('Page:', page);
        
                if (page.extract) {
                    wikiInfoDiv.innerHTML = `
                        <h3>${page.title}</h3>
                        <p>${page.extract}</p>
                        <a href="https://en.wikipedia.org/wiki/${encodeURIComponent(page.title)}" target="_blank">Daha fazla bilgi için tıklayın</a>
                    `;
                } else {
                    wikiInfoDiv.innerHTML = `<p>Bu meyve hakkında bilgi bulunamadı.</p>`;
                }
            }

            // wiki-info div'ini görünür hale getir
            wikiInfoDiv.style.display = 'block';
        } catch (error) {
            console.error('Wikipedia Hatası:', error);
            alert('Wikipedia bilgileri çekilirken bir hata oluştu: ' + error.message);
        }
        
        // Sonuç div'ini görünür hale getir
        resultDiv.style.display = 'block';
        
    } catch (error) {
        console.error('Genel Hata:', error);
        alert('Bir hata oluştu: ' + error.message);
    } finally {
        loadingDiv.style.display = 'none';
    }
});
