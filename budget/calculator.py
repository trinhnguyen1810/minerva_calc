from .config import CITY_MULTIPLIERS, SF_BASELINES

class BudgetCalculator:
    def __init__(self):
        self.city_multipliers = CITY_MULTIPLIERS
        self.sf_baselines = SF_BASELINES

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
        
        # Calculate allocations
        allocations = {}
        total_allocated = 0
        
        for category, ranges in self.sf_baselines.items():
            preference = user_data['spending_preferences'].get(category, 2)
            
            if preference == 1:
                adjusted_percent = ranges['min']
            elif preference == 3:
                adjusted_percent = ranges['max']
            else:
                adjusted_percent = ranges['base']
                
            adjusted_percent *= city_multiplier
            amount = available_money * adjusted_percent
            allocations[category] = amount
            total_allocated += amount

        # Normalize to available money
        if total_allocated > available_money:
            ratio = available_money / total_allocated
            allocations = {k: v * ratio for k, v in allocations.items()}
        
        # Add fixed expenses and savings
        allocations['fixed_expenses'] = fixed_expenses
        allocations['savings'] = savings_amount
        
        # Final verification
        total = sum(allocations.values())
        if abs(total - total_income) > 0.01:
            allocations['savings'] += (total_income - total)

        return {k: round(v, 2) for k, v in allocations.items()}