function fetchAndDisplayData() {
    // Fetch Calendar Data
    fetch('/api/current-season')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#calendar-table tbody');
            tbody.innerHTML = data.map(race => `
                <tr>
                    <td>${race.round}</td>
                    <td>${race.race_name}</td>
                    <td>${race.circuit}</td>
                    <td>${race.location}</td>
                    <td>${new Date(race.date).toLocaleDateString()}</td>
                    <td>${race.time || 'TBA'}</td>
                </tr>
            `).join('');
        })
        .catch(error => console.error('Error fetching calendar:', error));

    // Fetch Drivers Data
    fetch('/api/drivers')
        .then(response => response.json())
        .then(async data => {
            const grid = document.querySelector('#drivers-grid');
            
            // Fetch driver images from OpenF1 API
            const openF1Response = await fetch('https://api.openf1.org/v1/drivers');
            const openF1Data = await openF1Response.json();
            
            grid.innerHTML = data.map(driver => {
                // Find matching driver in OpenF1 data
                const openF1Driver = openF1Data.find(d => 
                    d.driver_number === driver.driver_number || 
                    d.name_acronym?.toLowerCase() === driver.code?.toLowerCase()
                );
                
                const imageUrl = openF1Driver?.headshot_url || 'https://media.formula1.com/content/dam/fom-website/drivers/2024/driver-fallback-image.png.transform/2col/image.png';
                
                return `
                    <div class="col-md-4 mb-4">
                        <div class="card driver-card h-100">
                            <img src="${imageUrl}" 
                                 class="card-img-top driver-img" 
                                 alt="${driver.full_name}" 
                                 onerror="this.src='https://media.formula1.com/content/dam/fom-website/drivers/2024/driver-fallback-image.png.transform/2col/image.png'">
                            <div class="card-body">
                                <h5 class="card-title">${driver.full_name}</h5>
                                <p class="card-text">
                                    <strong>Number:</strong> ${driver.driver_number}<br>
                                    <strong>Code:</strong> ${driver.code}<br>
                                    <strong>Nationality:</strong> ${driver.nationality}
                                </p>
                                <a href="${driver.wiki_url}" target="_blank" class="btn btn-primary">Wiki</a>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        })
        .catch(error => console.error('Error fetching drivers:', error));

    // Fetch Constructors Data
    fetch('/api/constructors')
        .then(response => response.json())
        .then(data => {
            const constructorImages = {
                'Red Bull': 'red-bull-racing',
                'Ferrari': 'ferrari',
                'Mercedes': 'mercedes',
                'McLaren': 'mclaren',
                'Aston Martin': 'aston-martin',
                'Alpine F1 Team': 'alpine',
                'Williams': 'williams',
                'RB': 'rb',
                'Stake F1 Team': 'stake',
                'Haas F1 Team': 'haas-f1-team'
            };

            const grid = document.querySelector('#constructors-grid');
            grid.innerHTML = data.map(constructor => {
                const teamImageName = constructorImages[constructor.name] || constructor.name.toLowerCase().replace(/\s+/g, '-');
                const imageUrl = `https://media.formula1.com/content/dam/fom-website/teams/2024/${teamImageName}.png.transform/2col/image.png`;
                
                return `
                    <div class="col-md-4 mb-4">
                        <div class="card constructor-card h-100">
                            <img src="${imageUrl}" 
                                 class="card-img-top constructor-img" 
                                 alt="${constructor.name}" 
                                 onerror="this.src='https://media.formula1.com/content/dam/fom-website/teams/2024/team-logo-fallback.png.transform/2col/image.png'">
                            <div class="card-body">
                                <h5 class="card-title">${constructor.name}</h5>
                                <p class="card-text">
                                    <strong>Nationality:</strong> ${constructor.nationality}
                                </p>
                                <a href="${constructor.wiki_url}" target="_blank" class="btn btn-primary">Wiki</a>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        })
        .catch(error => console.error('Error fetching constructors:', error));

    // Fetch Historical Driver Champions
    fetch('/api/driver-standings/all-time')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#champions-table tbody');
            tbody.innerHTML = data.map(champion => `
                <tr>
                    <td>${champion.year}</td>
                    <td>${champion.driver}</td>
                    <td>${champion.constructor}</td>
                    <td>${champion.wins}</td>
                    <td>${champion.points}</td>
                </tr>
            `).join('');
        })
        .catch(error => console.error('Error fetching champions:', error));

    // Fetch Historical Constructor Champions
    fetch('/api/constructor-standings/all-time')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#constructor-champions-table tbody');
            tbody.innerHTML = data.map(champion => `
                <tr>
                    <td>${champion.year}</td>
                    <td>${champion.constructor}</td>
                    <td>${champion.nationality}</td>
                    <td>${champion.wins}</td>
                    <td>${champion.points}</td>
                </tr>
            `).join('');
        })
        .catch(error => console.error('Error fetching constructor champions:', error));
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayData();
    // Refresh data every 5 minutes
    setInterval(fetchAndDisplayData, 300000);
});