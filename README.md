# Brew Numbers API
Source code for Brew Numbers API, which conducts calculations for beer brewing as prescribed by Dr. Michael L. Hall.  API implements python Flask microframework to serve JSON objects to support brewing applications.

---

Until a domain name is secured, Brew Number API can be reached at [http://18.216.248.93](http://18.216.248.93)

---

## Usage
Brew Numbers API endpoints are reached through URL routing. URL routing is based on category of calculation, followed by parameters described in the following documentation. All calculations are accurate with Temperature readings between 32 and 200 Fahrenheit.

`http://18.216.248.93/::Category::/::Parameter::/::Parameter::`

---

## Project TODO:
- [ ] Secure Domain Name
- [ ] Include Celsius Conversion
- [ ] Update return headers, include status codes
- [ ] Error handling
- [ ] Invalid url redirect

---
---

## Endpoints

### All Data - No Temperature Correction

Provided the initial gravity reading and final gravity readings, brewing API returns alcohol content, attenuation, and calories in solution.

#### Parameters

Initial Gravity Reading [float]
Final Gravity Reading [float]

#### Example Call
`http://18.216.248.93/all/no_correction/1.065/1.014`

#### Example Return
`{
  "provided": {
    "original_gravity": 1.065,
    "final_gravity": 1.014
  },
    "alcohol_content": 5.251,
    "attenuation": 62.719,
    "calories": 221.173
}`

---

### All Data - Temperature Corrected

Provided the initial gravity reading, final gravity readings, and associated temperature readings, Brew Numbers API returns alcohol content, attenuation, and calories in solution.

#### Parameters

Initial Gravity Reading [float]
Initial Temp Reading [integer]
Final Gravity Reading [float]
Final Temp Reading [integer]

#### Example Call
`http://18.216.248.93/all/temp_corrected/1.065/75/1.014/53`

#### Example Return
`{
  "provided": {
    "original_gravity": 1.065,
    "original_temp": 75,
    "final_gravity": 1.014,
    "final_temp": 53
  },
  "corrected_original_gravity": 1.067,
  "corrected_final_gravity": 1.014,
  "alcohol_content": 5.46,
  "attenuation": 62.719,
  "calories": 221.173
}`

---

### Specific Gravity Temperature Correction

Provided the gravity reading and the temperature at time of reading, Brew Math API returns the corrected gravity

#### Parameters

Specific Gravity Reading [float]
Temperature in Fahrenheit [integer]

#### Example Call
`http://18.216.248.93/temp_correction/1.065/76/`

#### Example Return
`{
  "provided": {
    "measured_gravity": 1.065,
    "temperature": 76
  },
  "corrected_gravity": 1.067
}`

---

### Priming Sugar Requirement

Provided the fermentation temperature in fahrenheit, desired volume of CO2, and volume of batch in gallons, Brew Numbers API Returns the required amount of priming sugar in grams.

#### Parameters

Temperature in Fahrenheit [integer]
Desired Volumes of CO2 [float]
Volume of Beer in Gallons [float]

#### Example Call
`http://18.216.248.93/carbonation/howmuchsugar/65/33.0/10.0`

#### Example Return
`{
  "provided": {
    "temp_in_f": 65,
    "desired_co2": 33.0,
    "volume_beer_gallons": 10.0
  },
  "req_gramms_priming_sugar": 4876.726035937499
}`

---

### CO2 in Solution

Provided the fermentation temperature in fahrenheit, mass of priming sugar in grams, and volume of batch in gallons, Brew Numbers API returns the volumes of CO2 in solution.

#### Parameters

Temperature in Fahrenheit [integer]
Mass of Priming Sugar in grams [float]
Volume of Beer in Gallons [float]

#### Example Call
`http://18.216.248.93/carbonation/howmuchco2/65/3.5/10.0`

#### Example Return
`{
  "provided": {
    "temp_in_f": 62,
    "priming_sugar_grams": 3.5,
    "volume_beer_gallons": 10.0
  },
  "req_gramms_priming_sugar": 0.98
}`
