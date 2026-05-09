  document.addEventListener('DOMContentLoaded', () => {
          
            const micButton = document.getElementById('mic-button');
            const themeToggle = document.getElementById('themeToggle');
            const body = document.body;
            const interactiveElements = document.querySelectorAll('.card, .sidebar-item'); // Elements for liquid effect
            let isActive = false;
            let backend = null;
            

        const API_KEY = "062e667ab318764cf35b5bccf2b24128"; 
        const API_URL = "https://api.openweathermap.org/data/2.5/weather";

        // Get DOM elements
        //const cityInput = document.getElementById('city-input');
        //const searchBtn = document.getElementById('search-btn');
        //const errorMsg = document.getElementById('error-message');
        //const weatherDisplay = document.getElementById('weather-display');
        const cityName = document.getElementById('city');
        //const weatherDescription = document.getElementById('weather-description');
        const temperature = document.getElementById('temperature');
        const humidity = document.getElementById('humidity');
        const windSpeed = document.getElementById('wind-speed');
        const feelsLike = document.getElementById('feels-like');
        //const weatherIconImg = document.getElementById('weather-icon-img');

        const initialContent = document.getElementById('initial-content');
        const activeContent = document.getElementById('active-content');
        const micIconInitial = document.getElementById('mic-icon-initial');
        const micIconActive = document.getElementById('mic-icon-active');
        

        const myJsVariable = "The secret message is 'Hello world!'";

                // This function returns the value of the variable.
                function getVariableValue() {
                    return myJsVariable;
                }
            // Get DOM elements

if (typeof qt !== 'undefined' && qt.webChannelTransport) {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            backend = channel.objects.backend;
            if (backend) {
                console.log("Successfully connected to Python backend.");

                //noted remove
            // --- Theme Toggle Logic ---
            const savedTheme = localStorage.getItem('theme');
            //const micStatus = localStorage.getItem('mic-status')

            // Set initial theme based on localStorage or default to dark
            if (savedTheme) {
                body.classList.add(savedTheme);
                updateThemeToggleIcon(savedTheme);
            } else {
                // Default to dark theme if no preference is found
                body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark-theme');
                updateThemeToggleIcon('dark-theme');
            }

            themeToggle.addEventListener('click', () => {
                  let newTheme;
                    if (body.classList.contains('light-theme')) {
                        body.classList.remove('light-theme');
                        body.classList.add('dark-theme');
                        newTheme = 'dark-theme';
                    } else {
                        body.classList.remove('dark-theme');
                        body.classList.add('light-theme');
                        newTheme = 'light-theme';
                    }
                    localStorage.setItem('theme', newTheme);
                    updateThemeToggleIcon(newTheme);
                    
                    
                    if (backend) {
                        backend.setTheme(newTheme);
                    }
            });
            function updateThemeToggleIcon(theme) {
                if (theme === 'light-theme') {
                    themeToggle.innerHTML = '<i class="fas fa-moon"></i>'; // Show moon to switch to dark
                    micworkButtonApplyStyles('light-theme')

                } else {
                    themeToggle.innerHTML = '<i class="fas fa-sun"></i>'; // Show sun to switch to light
                    micworkButtonApplyStyles('dark-theme')
                }
               
               
            }
            function micButtonApplyStyles(currentTheme) {
                micButton.classList.remove(
                    'mic-button-initial', 
                    'liquid-glass-effect-active', 
                    'shadow-md', 'shadow-xl', /* Ensure both shadows are removed */
                    'w-20', 'h-20', 'rounded-full', /* Initial state size/shape */
                    'w-[300px]', 'h-16'            /* Active state size/shape */
                ); 
                micButton.style.background = ''; // Clear inline background
                micButton.style.border = ''; // Clear inline border

                if (!isActive) { 
                    micButton.classList.add('w-20', 'h-20', 'rounded-full', 'mic-button-initial'); 
                    
                    initialContent.classList.remove('hidden', 'opacity-0');
                    initialContent.classList.add('opacity-100');
                    activeContent.classList.add('hidden', 'opacity-0');
                   
                } else { 
                    micButton.classList.add('w-[300px]', 'h-16', 'rounded-full', 'liquid-glass-effect-active'); 

                    if (currentTheme === 'light-theme') {
                        // Matching the image's subtle transparent gradient (pinkish-blue to greenish-blue)
                        micButton.style.background = 'linear-gradient(to right, rgba(245, 165, 178, 0.23), rgba(149, 213, 235, 0.27), rgba(144, 238, 144, 0.36))'; /* Soft pink, light blue, light green */
                    } else {
                        // Matching the image's subtle transparent gradient (pinkish-purple to light blue/green)
                        micButton.style.background = 'linear-gradient(to right, rgba(146, 2, 146, 0.1), rgba(0, 191, 255, 0.46))'; /* Purple to deep sky blue with transparency */
                    }
                    
                    initialContent.classList.add('hidden', 'opacity-0');
                    activeContent.classList.remove('hidden', 'opacity-0');
                    activeContent.classList.add('opacity-100');
                }
            }

            // --- Theme Toggle Logic ---
            function updateThemeToggleIcon(theme) {
                if (theme === 'light-theme') {
                    themeToggle.innerHTML = '<i class="fas fa-moon"></i>'; 
                } else {
                    themeToggle.innerHTML = '<i class="fas fa-sun"></i>'; 
                }
                micButtonApplyStyles(theme); // Update mic button styles when theme changes
            }

            // Load saved theme or default to dark
           
            // --- End Theme Toggle Logic ---


            micButton.addEventListener('click', () => {
                const currentTheme = body.classList.contains('light-theme') ? 'light-theme' : 'dark-theme';
                
                if (isActive) {
                    console.log("Button already active. Ignoring click.");
                    return; 
                }

                isActive = true; 
                micButtonApplyStyles(currentTheme); 

                console.log("Microphone: Recording started...");
                setTimeout(() => {
                    isActive = false; 
                    micButtonApplyStyles(currentTheme); 
                    if (backend) {
                        backend.micMode(true);
                    }
                    console.log("Microphone: Recording stopped (simulated).");
                }, 3000); 
            });

            // Initial application of mic button styles based on the determined theme
            micButtonApplyStyles(savedTheme || 'dark-theme'); 
            }});
        

                //micworkButton(savedTheme);

            function updateLiveTime(){
                const now = new Date();
                const timeString =now.toLocaleTimeString();
                document.getElementById('live-time').textContent = timeString;
            }
    
            updateLiveTime();
            setInterval(updateLiveTime, 1000)

            function updateLiveTime02(){
                const now = new Date();
                const timeString =now.toLocaleTimeString();
                document.getElementById('live-time02').textContent = timeString;
            }
    
            updateLiveTime02();
            setInterval(updateLiveTime02, 1000)
            

            function updateDate() {
            // Create a new Date object
            const now = new Date();

            // Format the date as a readable string
            const formattedDate = now.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });

            // Get the HTML element by its ID
            const dateElement = document.getElementById('live-date');

            // Update the element's content with the formatted date
            dateElement.innerHTML = formattedDate;
        }

        // Call the function once to display the date immediately
        updateDate();



        //weather

      
        
        // This function handles the API call and updates the UI
        async function fetchWeather(city) {
            // Clear previous error message and hide weather info
            //errorMsg.textContent = '';
            //weatherDisplay.classList.add('tempature');

            // Basic input validation
            /*if (city.trim() === '') {
                errorMsg.textContent = 'Please enter a city name.';
                return;
            }*/

            // Construct the full API URL
            const url = `${API_URL}?q=${city}&appid=${API_KEY}&units=metric`;

            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data)

                // Handle API error response (e.g., city not found)
               /* if (data.cod !== 200) {
                    errorMsg.textContent = data.message;
                    return;
                }*/

                // Update the UI with the fetched data
                cityName.innerHTML = `${data.name}, ${data.sys.country}`;
                //weatherDescription.textContent = data.weather[0].description;
                temperature.innerHTML = `${Math.round(data.main.temp)}°C`;
                
                humidity.innerHTML = `${data.main.humidity}%`;
                windSpeed.innerHTML = `WIND ${data.wind.speed} m/s`;
                feelsLike.innerHTML = `${Math.round(data.main.feels_like)}°C`;

                // Update the weather icon using an image from the API
                //updateWeatherIcon(data.weather[0].icon);

                // Update the background based on the weather condition
                //setDynamicBackground(data.weather[0].main);

                // Show the weather display section
                //weatherDisplay.classList.remove('hidden');

            } catch (error) {
                // Handle network errors
                errorMsg.textContent = 'Failed to fetch weather data. Please try again.';
                console.error('Error fetching weather data:', error);
            }
        }

        fetchWeather('Colombo')

        // This function dynamically generates the image URL based on the weather icon code
        /*function updateWeatherIcon(iconCode) {
            // Construct the image URL using the OpenWeatherMap icon library
            const iconUrl = `https://openweathermap.org/img/wn/${iconCode}@4x.png`;
            weatherIconImg.src = iconUrl;
        }*/
        
        // Function to set dynamic background based on weather condition
        /*function setDynamicBackground(weatherCondition) {
            let bgImage;
            switch(weatherCondition.toLowerCase()) {
                case 'clear':
                    bgImage = 'https://images.unsplash.com/photo-1558414441-2a6234b6b668?q=80&w=2670&auto=format&fit=crop';
                    break;
                case 'clouds':
                    bgImage = 'https://images.unsplash.com/photo-1534015694200-a54826b5d92d?q=80&w=2670&auto=format&fit=crop';
                    break;
                case 'rain':
                case 'drizzle':
                    bgImage = 'https://images.unsplash.com/photo-1549419163-5494d402324f?q=80&w=2670&auto=format&fit=crop';
                    break;
                case 'thunderstorm':
                    bgImage = 'https://images.unsplash.com/photo-1596765798933-728b9d62863b?q=80&w=2670&auto=format&fit=crop';
                    break;
                case 'snow':
                    bgImage = 'https://images.unsplash.com/photo-1612711018868-b3917417e47f?q=80&w=2670&auto=format&fit=crop';
                    break;
                case 'mist':
                case 'smoke':
                case 'haze':
                case 'dust':
                case 'fog':
                case 'sand':
                case 'ash':
                case 'squall':
                case 'tornado':
                    bgImage = 'https://images.unsplash.com/photo-1510255381664-53c89c898b96?q=80&w=2670&auto=format&fit=crop';
                    break;
                default:
                    bgImage = 'https://images.unsplash.com/photo-1502484088998-636952479f61?q=80&w=2670&auto=format&fit=crop';
                    break;
            }

        }*/

        // Add event listener to the search button
        //searchBtn.addEventListener('click', () => {
            //fetchWeather(cityInput.value);
        //});

        // Allow pressing Enter in the input field to trigger the search
        /*cityInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                searchBtn.click();
            }
        });
        
        // Initial fetch for a default city on page load
        window.addEventListener('load', () => {
            fetchWeather('Colombo');
        });*/


            

            // --- Liquid Feeling Effect (Mousemove Tilt/Blur) ---
            interactiveElements.forEach(element => {
                element.addEventListener('mousemove', (e) => {
                    const rect = element.getBoundingClientRect();
                    const x = e.clientX - rect.left; // X position relative to the element
                    const y = e.clientY - rect.top;  // Y position relative to the element

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    // Calculate rotation angles
                    const rotateY = ((x - centerX) / centerX) * 5; // Max 5 degrees Y rotation
                    const rotateX = ((centerY - y) / centerY) * 5; // Max 5 degrees X rotation (inverted Y for natural tilt)

                    // Calculate blur (optional, subtle)
                    const distanceFromCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
                    const maxDistance = Math.sqrt(Math.pow(centerX, 2) + Math.pow(centerY, 2));
                    const blurAmount = (distanceFromCenter / maxDistance) * 0.5; // Max 0.5px blur at edges

                    element.style.setProperty('--rotateX', `${rotateX}deg`);
                    element.style.setProperty('--rotateY', `${rotateY}deg`);
                    element.style.setProperty('--blur-radius', `${blurAmount}px`);
                });

                element.addEventListener('mouseleave', () => {
                    // Reset properties on mouse leave
                    element.style.setProperty('--rotateX', '0deg');
                    element.style.setProperty('--rotateY', '0deg');
                    element.style.setProperty('--blur-radius', '0px');
                });
            });
            //noted remove
         /*   } else {
                console.error("Python backend object 'backend' not found in QWebChannel.");
            }
        });
    } else {
        console.warn("QWebChannel not found. Ensure the script tag is present.");
    }


            

            
       */


}});


