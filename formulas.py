# Formulas referenced from:
# "Brew by the Numbers - Add up what's in your beer" by Dr. Michael J. Hall, Zymergy, Summer 1995, vol. 18, no. 2


# Specific Gravity Formulas


def correction_factor(temp_f):
    return 1.00130346 - \
           (1.34722124e-4 * temp_f) + \
           (2.04052596e-6 * (temp_f ** 2)) - \
           (2.32820948e-9 * (temp_f ** 3))


def corrected_sg(measured_gravity, temp_f):
    '''Returns corrected specific gravity when accounting for temperature related correction factor'''
    c_factor = correction_factor(temp_f)
    return measured_gravity + (c_factor - 1)


# Extract Formulas


def extract(specific_gravity):
    '''Returns weight percent of dissolved materials in wort in degress Plato.
    Parameter: specific_gravity is measured gravity (ie 1.065)'''
    return -668.962 + \
           1262.45 * specific_gravity - \
           776.43 * specific_gravity ** 2 + \
           182.94 * specific_gravity ** 3


def attenuation_coefficient(original_gravity):
    '''Returns attenuation coefficient
    Parameter: original_gravity is measured reading before fermentation'''
    return 0.22 + 0.001 * extract(original_gravity)


def real_extract(original_gravity, final_gravity):
    '''Returns real extract in degrees Plato.
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    q = attenuation_coefficient(original_gravity)
    return (q * extract(original_gravity) + extract(final_gravity)) / (1 + q)


# Attenuation Formulas


def apparent_attenuation(original_gravity, final_gravity):
    '''Returns apparent attenuation in as a percent of sugar converted to alcohol.
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return ((extract(original_gravity) - extract(final_gravity)) / extract(original_gravity)) * 100


def real_attenuation(original_gravity, final_gravity):
    '''Returns real attenuation in as a percent of sugar converted to alcohol.
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    re = real_extract(original_gravity, final_gravity)
    return ((extract(original_gravity) - re) / extract(original_gravity)) * 100


# Alcohol Content Formulas


def alcohol_content(original_gravity, final_gravity):
    '''Returns alcohol percent by weight.
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return (extract(original_gravity) - real_extract(original_gravity, final_gravity)) / (2.0665 - 0.010665 * \
                                                                                          extract(original_gravity))


# Calorie Content Formulas


def extract_calories(original_gravity, final_gravity):
    '''Returns calories derived from residual sugars in beer
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return 3.55 * final_gravity * 3.8 * real_extract(original_gravity, final_gravity)


def alcohol_calories(original_gravity, final_gravity):
    '''Returns calories derived from converted ethanol alcohol final beer
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return 3.55 * final_gravity * 7.1 * alcohol_content(original_gravity, final_gravity)


def protein_calories(original_gravity, final_gravity):
    '''Returns calories derived from proteins produced during fermentation
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return 3.55 * final_gravity * 4.0 * 0.07 * real_extract(original_gravity, final_gravity)


def calories(original_gravity, final_gravity):
    '''Returns sum of all caloric elements of beer
    Parameters: original_gravity measured gravity reading before fermentation
                final_gravity measured gravity reading at end of fermentation'''
    return extract_calories(original_gravity, final_gravity) + alcohol_calories(original_gravity, final_gravity) + \
           protein_calories(original_gravity, final_gravity)


# Carbonation Level


def carbon_dioxide_initial(temp_f):
    '''Returns volumes of Carbon Dioxide when at equilibrium at provided temperature
    Parameter: temp_f is temperature of solution in fahrenheit'''
    return 3.0378 - 5.0062e-2 * temp_f + 2.6555e-4 * temp_f ** 2


def carbon_dioxide_generated(priming_sugar_grams, volume_beer_gallons):
    '''Returns volumes of carbon dioxide produced by a given volume of beer and given mass of priming sugar
    Parameters: priming_sugars_grams is mass of priming sugar in grams
                volume_beer_gallons is volume of beer in gallons'''
    return 6.5811e-2 * (priming_sugar_grams / volume_beer_gallons)


def carbon_dioxide(temp_f, priming_sugars_grams, volume_beer_gallons):
    '''Returns volumes of carbon dioxide in solution
    Parameters: temp_f is temperature of solution in fahrenheit
                priming_sugars_grams is mass of priming sugar in grams
                volume_beer_gallons is volume of beer in gallons'''
    return carbon_dioxide_initial(temp_f) + carbon_dioxide_generated(priming_sugars_grams, volume_beer_gallons)


def how_much_sugar(temp_f, desired_co2, volume_beer_gallons):
    '''Returns the mass of priming sugar in grams to provide to a given volume of beer to achieve a desired volume of CO2
    Parameters: temp_f is temperature of solution in fahrenheit
                desired_co2 is the desired volume of CO2 in final solution
                volume_beer_gallons is volume of beer in gallons'''
    return 15.195 * volume_beer_gallons * (desired_co2 - 3.0378 + 5.0062e-2 * temp_f - 2.6555e-4 * temp_f ** 2)