document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('searchForm');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        loading.style.display = 'block';
        results.style.display = 'none';
        
        try {
            const formData = new FormData(form);
            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Hide loading spinner
            loading.style.display = 'none';
            
            // Show results
            results.style.display = 'block';
            
            if (data.status === 'success') {
                resultsContent.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        ${data.message}
                    </div>
                    <div class="d-grid gap-2">
                        <a href="${data.download_url}" class="btn btn-success">
                            <i class="fas fa-download me-2"></i>
                            Download Excel File
                        </a>
                    </div>
                `;
            } else {
                resultsContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        ${data.message}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error:', error);
            loading.style.display = 'none';
            results.style.display = 'block';
            resultsContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    An error occurred while processing your request. Please try again.
                </div>
            `;
        }
    });
}); 