"""
Receipt Memory - AI-Powered Receipt Query System
Backend implementation with sample data
"""

import json
from datetime import datetime

# Sample Receipt Database
RECEIPTS_DB = [
    {
        "receipt_id": "rec_001",
        "timestamp": "2024-11-10T10:15:00Z",
        "merchant": "Patagonia",
        "location": "Boulder, CO",
        "total": 89.99,
        "items": [
            {
                "name": "Better Sweater Jacket",
                "category": "Clothing",
                "price": 89.99,
                "quantity": 1
            }
        ],
        "payment_method": "Credit Card ending in 4242",
        "tags": ["clothing", "outdoor gear"],
        "carbon_footprint": 22.3
    },
    {
        "receipt_id": "rec_002",
        "timestamp": "2024-11-12T19:45:00Z",
        "merchant": "The Kitchen",
        "location": "Boulder, CO",
        "total": 67.50,
        "items": [
            {"name": "Farm Bowl", "category": "Food - Entree", "price": 18.00, "quantity": 1},
            {"name": "Salmon Salad", "category": "Food - Entree", "price": 22.00, "quantity": 1},
            {"name": "House Wine", "category": "Drinks - Alcohol", "price": 12.00, "quantity": 2}
        ],
        "payment_method": "Credit Card ending in 4242",
        "tags": ["dining", "restaurant", "date night"],
        "carbon_footprint": 8.7
    },
    {
        "receipt_id": "rec_003",
        "timestamp": "2024-10-28T14:20:00Z",
        "merchant": "REI",
        "location": "Denver, CO",
        "total": 156.78,
        "items": [
            {"name": "Hiking Boots", "category": "Outdoor Gear", "price": 129.99, "quantity": 1},
            {"name": "Wool Socks", "category": "Clothing", "price": 18.99, "quantity": 1},
            {"name": "Water Bottle", "category": "Outdoor Gear", "price": 24.99, "quantity": 1}
        ],
        "payment_method": "Credit Card ending in 4242",
        "tags": ["outdoor gear", "hiking"],
        "carbon_footprint": 45.2
    },
    {
        "receipt_id": "rec_004",
        "timestamp": "2024-11-01T08:30:00Z",
        "merchant": "Starbucks",
        "location": "Boulder, CO",
        "total": 12.85,
        "items": [
            {"name": "Oat Milk Latte", "category": "Drinks - Coffee", "price": 6.25, "quantity": 1},
            {"name": "Breakfast Sandwich", "category": "Food - Breakfast", "price": 6.60, "quantity": 1}
        ],
        "payment_method": "Apple Pay",
        "tags": ["coffee", "breakfast"],
        "carbon_footprint": 2.1
    },
    {
        "receipt_id": "rec_005",
        "timestamp": "2024-11-15T16:00:00Z",
        "merchant": "Target",
        "location": "Boulder, CO",
        "total": 234.67,
        "items": [
            {"name": "Throw Pillows", "category": "Home Decor", "price": 39.99, "quantity": 2},
            {"name": "Candles", "category": "Home Decor", "price": 24.99, "quantity": 3},
            {"name": "Dog Treats", "category": "Pet Supplies", "price": 18.99, "quantity": 1},
            {"name": "Shampoo", "category": "Personal Care", "price": 14.99, "quantity": 1}
        ],
        "payment_method": "Debit Card",
        "tags": ["home", "pet supplies", "personal care"],
        "carbon_footprint": 15.8
    }
]


def simple_query_handler(question):
    """
    Simple rule-based query handler (no API needed for demo)
    In production, this would use Claude API or similar
    """
    question_lower = question.lower()
    
    # When did I buy [item]?
    if "when" in question_lower and "jacket" in question_lower:
        return {
            "answer": "You bought a Better Sweater Jacket from Patagonia on November 10th for $89.99 at their Boulder location.",
            "source_receipts": ["rec_001"]
        }
    
    # Restaurant spending
    if "restaurant" in question_lower or "dining" in question_lower:
        return {
            "answer": "You've spent $67.50 on restaurants in November. You visited The Kitchen on November 12th for dinner.",
            "source_receipts": ["rec_002"]
        }
    
    # Outdoor gear
    if "outdoor" in question_lower or "hiking" in question_lower:
        return {
            "answer": "You've made 2 outdoor gear purchases recently:\n• REI on October 28: Hiking Boots ($129.99), Wool Socks ($18.99), Water Bottle ($24.99) - Total: $156.78\n• Patagonia on November 10: Better Sweater Jacket ($89.99)",
            "source_receipts": ["rec_001", "rec_003"]
        }
    
    # Carbon footprint
    if "carbon" in question_lower or "footprint" in question_lower:
        total_carbon = sum(r["carbon_footprint"] for r in RECEIPTS_DB)
        return {
            "answer": f"Your total carbon footprint from tracked purchases is {total_carbon:.1f}kg of CO2. Your biggest contributor was the REI hiking gear at 45.2kg.",
            "source_receipts": ["rec_003"]
        }
    
    # Spending by month
    if "spend" in question_lower and "month" in question_lower:
        nov_total = sum(r["total"] for r in RECEIPTS_DB if "2024-11" in r["timestamp"])
        return {
            "answer": f"You've spent ${nov_total:.2f} in November across 4 purchases (Patagonia, The Kitchen, Starbucks, and Target).",
            "source_receipts": ["rec_001", "rec_002", "rec_004", "rec_005"]
        }
    
    # Default response
    return {
        "answer": "I can help you with questions like:\n• When did I buy that jacket?\n• How much did I spend on restaurants?\n• What's my carbon footprint?\n• Show me my outdoor gear purchases",
        "source_receipts": []
    }


def get_receipt_by_id(receipt_id):
    """Get full receipt details by ID"""
    for receipt in RECEIPTS_DB:
        if receipt["receipt_id"] == receipt_id:
            return receipt
    return None


# Example usage
if __name__ == "__main__":
    # Test queries
    test_questions = [
        "When did I buy that jacket?",
        "How much have I spent this month?",
        "What's my carbon footprint?",
        "Show me restaurant spending"
    ]
    
    print("Receipt Memory - Test Queries\n" + "="*50 + "\n")
    
    for question in test_questions:
        result = simple_query_handler(question)
        print(f"Q: {question}")
        print(f"A: {result['answer']}")
        if result['source_receipts']:
            print(f"   Sources: {', '.join(result['source_receipts'])}")
        print()
