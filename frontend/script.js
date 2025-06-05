document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const configTextarea = document.getElementById('configText');
    const loadConfigBtn = document.getElementById('loadConfig');
    const saveConfigBtn = document.getElementById('saveConfig');
    const startBatchInput = document.getElementById('startBatch');
    const endBatchInput = document.getElementById('endBatch');
    const runScraperBtn = document.getElementById('runScraper');
    const stopScraperBtn = document.getElementById('stopScraper');
    const logsContainer = document.getElementById('logsContainer');
    const configStatus = document.getElementById('configStatus');
    
    // Global variables
    let scraperRunning = false;
    let logUpdateInterval = null;
    
    // Load config when page loads
    loadConfig();
    
    // Event listeners
    loadConfigBtn.addEventListener('click', loadConfig);
    saveConfigBtn.addEventListener('click', saveConfig);
    runScraperBtn.addEventListener('click', runScraper);
    stopScraperBtn.addEventListener('click', stopScraper);
    
    // Functions
    function loadConfig() {
        addLog('Loading configuration...', 'info');
        configStatus.textContent = 'Loading configuration...';
        configStatus.className = 'status-message status-info';
        
        // Show the current URL we're trying to connect to (helpful for debugging)
        const apiUrl = '/api/config';
        addLog(`Connecting to: ${window.location.origin}${apiUrl}`, 'info');
        
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            // Make sure credentials are included for local requests
            credentials: 'same-origin'
        })
            .then(response => {
                console.log('Config response:', response);
                if (!response.ok) {
                    throw new Error(`Failed to load configuration: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(config => {
                console.log('Loaded config:', config);
                if (config.error) {
                    throw new Error(config.error);
                }
                configTextarea.value = JSON.stringify(config, null, 2);
                addLog('Configuration loaded successfully', 'success');
                configStatus.textContent = 'Configuration loaded successfully';
                configStatus.className = 'status-message status-success';
            })
            .catch(error => {
                console.error('Config load error:', error);
                addLog(`Error: ${error.message}`, 'error');
                configStatus.textContent = `Error: ${error.message}`;
                configStatus.className = 'status-message status-error';
                
                // Check if it's a connection error
                if (error.message.includes('Failed to fetch')) {
                    addLog('Connection to server failed. Make sure the server is running.', 'error');
                    configStatus.textContent = 'Server connection failed. Is the server running?';
                    const serverAddress = window.location.origin;
                    addLog(`The server should be running at: ${serverAddress}`, 'info');
                }
                
                // Provide default config if loading fails
                configTextarea.value = JSON.stringify({
                    "download_dir": "./downloads",
                    "auth_url": "https://login.openathens.net/auth/cobbcounty.org/o/72388178",
                    "library_credentials": {
                        "Cobb County Library": {
                            "username": "YOUR_LIBRARY_CARD_NUMBER",
                            "password": "YOUR_PIN"
                        }
                    },
                    "search_parameters": {
                        "state": "Georgia",
                        "include_unverified": true,
                        "include_closed": false
                    },
                    "pages_per_batch": 10,
                    "pages_to_download": "all",
                    "state_file": "reference_usa_state.json"
                }, null, 2);
            });
    }
    
    function saveConfig() {
        addLog('Saving configuration...', 'info');
        configStatus.textContent = 'Saving configuration...';
        configStatus.className = 'status-message status-info';
        
        try {
            // Validate JSON
            const configData = JSON.parse(configTextarea.value);
            
            fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(configData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to save configuration');
                }
                return response.json();
            })
            .then(result => {
                addLog('Configuration saved successfully', 'success');
                configStatus.textContent = 'Configuration saved successfully';
                configStatus.className = 'status-message status-success';
            })
            .catch(error => {
                addLog(`Error: ${error.message}`, 'error');
                configStatus.textContent = `Error: ${error.message}`;
                configStatus.className = 'status-message status-error';
            });
        } catch (error) {
            addLog(`Invalid JSON: ${error.message}`, 'error');
            configStatus.textContent = `Invalid JSON: ${error.message}`;
            configStatus.className = 'status-message status-error';
        }
    }
    
    function runScraper() {
        const startBatch = parseInt(startBatchInput.value) || 1;
        const endBatch = parseInt(endBatchInput.value) || 10;
        
        if (startBatch > endBatch) {
            addLog('Error: Start batch cannot be greater than end batch', 'error');
            return;
        }
        
        addLog(`Starting scraper (Batch ${startBatch} to ${endBatch})...`, 'info');
        
        fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ startBatch, endBatch })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to start scraper');
            }
            return response.json();
        })
        .then(result => {
            scraperRunning = true;
            updateUIForRunningState();
            startLogUpdates();
        })
        .catch(error => {
            addLog(`Error: ${error.message}`, 'error');
        });
    }
    
    function stopScraper() {
        addLog('Stopping scraper...', 'warning');
        
        fetch('/api/stop', {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to stop scraper');
            }
            return response.json();
        })
        .then(result => {
            scraperRunning = false;
            updateUIForStoppedState();
        })
        .catch(error => {
            addLog(`Error: ${error.message}`, 'error');
        });
    }
    
    function updateUIForRunningState() {
        runScraperBtn.disabled = true;
        stopScraperBtn.disabled = false;
        startBatchInput.disabled = true;
        endBatchInput.disabled = true;
        saveConfigBtn.disabled = true;
    }
    
    function updateUIForStoppedState() {
        runScraperBtn.disabled = false;
        stopScraperBtn.disabled = true;
        startBatchInput.disabled = false;
        endBatchInput.disabled = false;
        saveConfigBtn.disabled = false;
        
        if (logUpdateInterval) {
            clearInterval(logUpdateInterval);
        }
    }
    
    function startLogUpdates() {
        // Clear any existing interval
        if (logUpdateInterval) {
            clearInterval(logUpdateInterval);
        }
        
        // Start polling for log updates
        logUpdateInterval = setInterval(() => {
            fetch('/api/logs')
                .then(response => response.json())
                .then(logs => {
                    updateLogs(logs);
                    
                    // Check if the scraper is still running
                    if (!scraperRunning) {
                        updateUIForStoppedState();
                    }
                })
                .catch(error => {
                    console.error('Error fetching logs:', error);
                });
        }, 1000);
    }
    
    function updateLogs(logs) {
        // Clear existing logs
        logsContainer.innerHTML = '';
        
        // Add each log entry
        logs.forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.classList.add('log-entry', `log-${log.level}`);
            logEntry.textContent = `[${log.timestamp}] ${log.message}`;
            logsContainer.appendChild(logEntry);
        });
        
        // Scroll to bottom
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
    
    function addLog(message, type = 'info') {
        const logEntry = document.createElement('div');
        logEntry.classList.add('log-entry', `log-${type}`);
        
        const timestamp = new Date().toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        logsContainer.appendChild(logEntry);
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
});
