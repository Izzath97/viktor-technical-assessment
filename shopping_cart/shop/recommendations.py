from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Any


def analyze_product_sequences(carts: List[Any]) -> Dict[str, Tuple[str, int]]:
    # Track what products are added after each product
    product_followers = defaultdict(list)
    
    for cart in carts:
        # Get items ordered by when they were added
        items = list(cart.items.all().order_by('added_at'))
        
        # Analyze sequences
        for i in range(len(items) - 1):
            current_product_id = str(items[i].object_id)
            next_product_id = str(items[i + 1].object_id)
            product_followers[current_product_id].append(next_product_id)
    
    # Find most common follower for each product
    result = {}
    for product_id, followers in product_followers.items():
        if followers:
            counter = Counter(followers)
            most_common = counter.most_common(1)[0]
            result[product_id] = (most_common[0], most_common[1])
    
    return result


def get_product_recommendations(
    product_id: str,
    carts: List[Any],
    limit: int = 5
) -> List[Tuple[str, int]]:
    
    product_followers = []
    
    for cart in carts:
        items = list(cart.items.all().order_by('added_at'))
        
        for i in range(len(items) - 1):
            if str(items[i].object_id) == product_id:
                product_followers.append(str(items[i + 1].object_id))
    
    if not product_followers:
        return []
    
    counter = Counter(product_followers)
    return counter.most_common(limit)


def get_cart_similarity_score(cart1: Any, cart2: Any) -> float:
    items1 = set(str(item.object_id) for item in cart1.items.all())
    items2 = set(str(item.object_id) for item in cart2.items.all())
    
    if not items1 and not items2:
        return 0.0
    
    intersection = len(items1 & items2)
    union = len(items1 | items2)
    
    return intersection / union if union > 0 else 0.0


def find_frequently_bought_together(
    carts: List[Any],
    min_frequency: int = 2
) -> List[Tuple[Tuple[str, ...], int]]:
    product_combinations = defaultdict(int)
    
    for cart in carts:
        product_ids = sorted([
            str(item.object_id) for item in cart.items.all()
        ])
        
        # Generate all pairs of products in this cart
        for i in range(len(product_ids)):
            for j in range(i + 1, len(product_ids)):
                pair = (product_ids[i], product_ids[j])
                product_combinations[pair] += 1
    
    # Filter by minimum frequency and sort
    result = [
        (pair, count)
        for pair, count in product_combinations.items()
        if count >= min_frequency
    ]
    
    return sorted(result, key=lambda x: x[1], reverse=True)
