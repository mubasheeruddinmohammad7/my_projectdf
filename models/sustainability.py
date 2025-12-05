"""
Sustainability Calculator for Digital Fashion
Calculates environmental impact savings
"""

class SustainabilityCalculator:
    """Calculate environmental savings for digital fashion"""
    
    # Data source: Various environmental studies on fashion industry
    IMPACT_PER_GARMENT = {
        't-shirt': {
            'water_liters': 2700,  # 2700L for one cotton t-shirt
            'co2_kg': 10,          # 10kg CO2 emissions
            'chemicals_kg': 0.5,   # 0.5kg chemicals
            'waste_kg': 0.3        # 0.3kg textile waste
        },
        'jeans': {
            'water_liters': 7500,  # 7500L for one pair of jeans
            'co2_kg': 33,
            'chemicals_kg': 1.5,
            'waste_kg': 1.5
        },
        'dress': {
            'water_liters': 5000,
            'co2_kg': 25,
            'chemicals_kg': 0.8,
            'waste_kg': 0.8
        },
        'jacket': {
            'water_liters': 6000,
            'co2_kg': 28,
            'chemicals_kg': 1.2,
            'waste_kg': 1.2
        },
        'shoes': {
            'water_liters': 8000,
            'co2_kg': 40,
            'chemicals_kg': 2.0,
            'waste_kg': 2.0
        },
        'accessory': {
            'water_liters': 1000,
            'co2_kg': 5,
            'chemicals_kg': 0.1,
            'waste_kg': 0.1
        }
    }
    
    @classmethod
    def calculate_savings(cls, garment_type: str, quantity: int = 1):
        """Calculate savings for digital garment"""
        if garment_type not in cls.IMPACT_PER_GARMENT:
            garment_type = 't-shirt'  # Default
        
        impact = cls.IMPACT_PER_GARMENT[garment_type]
        
        return {
            'garment_type': garment_type,
            'quantity': quantity,
            'water_saved_liters': impact['water_liters'] * quantity,
            'co2_saved_kg': impact['co2_kg'] * quantity,
            'chemicals_saved_kg': impact['chemicals_kg'] * quantity,
            'waste_reduced_kg': impact['waste_kg'] * quantity,
            'real_world_equivalents': cls.get_equivalents(
                impact['water_liters'] * quantity,
                impact['co2_kg'] * quantity
            )
        }
    
    @classmethod
    def get_equivalents(cls, water_liters: float, co2_kg: float):
        """Get real-world equivalents for impact"""
        return {
            'showers': water_liters / 60,          # Average shower: 60L
            'drinking_days': water_liters / 2,     # 2L per person per day
            'car_km': co2_kg * 2.5,                # Car emits ~0.4kg CO2 per km
            'trees': co2_kg / 21.77,               # One tree absorbs 21.77kg CO2 per year
            'smartphone_charges': co2_kg * 5000    # 1kg CO2 ≈ 5000 smartphone charges
        }
    
    @classmethod
    def calculate_collection_impact(cls, items: list):
        """Calculate impact for entire collection"""
        total = {
            'water_saved_liters': 0,
            'co2_saved_kg': 0,
            'chemicals_saved_kg': 0,
            'waste_reduced_kg': 0,
            'items_count': len(items)
        }
        
        for item in items:
            savings = cls.calculate_savings(
                item.get('garment_type', 't-shirt'),
                item.get('quantity', 1)
            )
            
            total['water_saved_liters'] += savings['water_saved_liters']
            total['co2_saved_kg'] += savings['co2_saved_kg']
            total['chemicals_saved_kg'] += savings['chemicals_saved_kg']
            total['waste_reduced_kg'] += savings['waste_reduced_kg']
        
        total['equivalents'] = cls.get_equivalents(
            total['water_saved_liters'],
            total['co2_saved_kg']
        )
        
        return total
    
    @classmethod
    def get_industry_comparison(cls):
        """Get fashion industry impact statistics"""
        return {
            'annual_water_usage_liters': 9300000000000,  # 9.3 trillion liters
            'annual_co2_emissions_kg': 1200000000000,    # 1.2 billion tons
            'annual_textile_waste_kg': 92000000000,      # 92 million tons
            'percentage_global_carbon': 10,              # 10% of global emissions
            'percentage_global_wastewater': 20,          # 20% of wastewater
            'clothes_dumped_per_second_kg': 2.5          # 2.5kg per second
        }