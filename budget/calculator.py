from budget.config import CITY_MULTIPLIERS, SF_BASELINES, CITY_BASELINES

class BudgetCalculator:
    def __init__(self):
        self.city_multipliers = CITY_MULTIPLIERS
        self.sf_baselines = SF_BASELINES
        self.city_baselines = CITY_BASELINES

    def calculate_recommendations(self, user_data):
        """Calculate budget recommendations based on user inputs"""
        # Calculate total income and deductions
        total_income = user_data['income']['work_study'] + user_data['income']['external']
        savings_amount = total_income * (user_data['savings_goal'] / 100)
        fixed_expenses = sum(user_data['fixed_expenses'].values())
        
        # Verify we don't exceed total income
        if savings_amount + fixed_expenses > total_income:
            savings_amount = total_income - fixed_expenses
            if savings_amount < 0:
                savings_amount = 0
                fixed_expenses = total_income

        # Calculate available money for flexible spending
        available_money = total_income - savings_amount - fixed_expenses
        
        if available_money <= 0:
            return {
                'fixed_expenses': fixed_expenses,
                'savings': savings_amount,
                'food': 0,
                'transportation': 0,
                'entertainment': 0,
                'personal': 0,
                'gym': 0
            }

        # Get city adjustment
        city = user_data['location']
        city_multiplier = self.city_multipliers[city]
        
        # Use city-specific baselines when available, otherwise use SF baselines with multiplier
        baselines = self.city_baselines.get(city, self.sf_baselines)
        use_multiplier = city not in self.city_baselines
        
        # Calculate allocations
        allocations = {}
        total_weighted_preference = 0
        weights = {}
        
        # Calculate weights based on user preferences
        for category, ranges in baselines.items():
            preference = user_data['spending_preferences'].get(category, 2)
            
            if preference == 1:
                base_percent = ranges['min']
            elif preference == 3:
                base_percent = ranges['max']
            else:
                base_percent = ranges['base']
                
            # Apply city multiplier if using SF baselines
            if use_multiplier:
                adjusted_percent = base_percent * city_multiplier
            else:
                adjusted_percent = base_percent
                
            # Store weight for each category
            weights[category] = adjusted_percent
            total_weighted_preference += adjusted_percent
        
        # Normalize weights to ensure they sum to 1.0
        for category, weight in weights.items():
            normalized_weight = weight / total_weighted_preference if total_weighted_preference > 0 else 0
            amount = available_money * normalized_weight
            allocations[category] = amount
        
        # Add fixed expenses and savings
        allocations['fixed_expenses'] = fixed_expenses
        allocations['savings'] = savings_amount
        
        # Final verification to ensure we're not exceeding the total income
        total = sum(allocations.values())
        if abs(total - total_income) > 0.01:
            # Adjust savings slightly to account for any rounding errors
            allocations['savings'] += (total_income - total)

        return {k: round(v, 2) for k, v in allocations.items()}