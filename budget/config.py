CITY_MULTIPLIERS = {
    'San Francisco': 1.0,  # Base city
    'Berlin': 0.8,
    'Taipei': 0.7,
    'Hyderabad': 0.5,
    'Seoul': 0.9,
    'Buenos Aires': 0.6
}

SF_BASELINES = {
    'food': {'min': 0.30, 'base': 0.35, 'max': 0.60},
    'transportation': {'min': 0.05, 'base': 0.07, 'max': 0.10},
    'entertainment': {'min': 0.00, 'base': 0.15, 'max': 0.30},
    'personal': {'min': 0.05, 'base': 0.07, 'max': 0.10},
    'gym': {'min': 0.00, 'base': 0.05, 'max': 0.15}
}


CITY_BASELINES = {
    'Taipei': {
        'food': {'min': 0.20, 'base': 0.275, 'max': 0.35},
        'transportation': {'min': 0.05, 'base': 0.10, 'max': 0.15},
        'entertainment': {'min': 0.10, 'base': 0.15, 'max': 0.20},
        'personal': {'min': 0.10, 'base': 0.10, 'max': 0.10},
        'gym': {'min': 0.05, 'base': 0.05, 'max': 0.05},
    },
    'Seoul': {
        'food': {'min': 0.30, 'base': 0.35, 'max': 0.40},
        'transportation': {'min': 0.10, 'base': 0.15, 'max': 0.20},
        'entertainment': {'min': 0.20, 'base': 0.20, 'max': 0.20},
        'personal': {'min': 0.15, 'base': 0.15, 'max': 0.15},
        'gym': {'min': 0.15, 'base': 0.15, 'max': 0.15},
    },
    'Buenos Aires': {
        'food': {'min': 0.20, 'base': 0.30, 'max': 0.40},
        'transportation': {'min': 0.15, 'base': 0.15, 'max': 0.15},
        'entertainment': {'min': 0.10, 'base': 0.20, 'max': 0.30},
        'personal': {'min': 0.15, 'base': 0.20, 'max': 0.25},
        'gym': {'min': 0.00, 'base': 0.03, 'max': 0.06},
    },
    'Berlin': {
        'food': {'min': 0.30, 'base': 0.35, 'max': 0.40},
        'transportation': {'min': 0.15, 'base': 0.15, 'max': 0.15},
        'entertainment': {'min': 0.20, 'base': 0.20, 'max': 0.20},
        'personal': {'min': 0.10, 'base': 0.125, 'max': 0.15},
        'gym': {'min': 0.15, 'base': 0.15, 'max': 0.15},
    }
}
